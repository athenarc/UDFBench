
-- U46. Logistic Regression UDF recursive

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'logistic_regression_result') THEN
        CREATE TYPE logistic_regression_result AS (
            weight FLOAT,
            bias FLOAT
        );
    END IF;
END $$;

CREATE OR REPLACE FUNCTION logistic_regression_recursive_train(
    subquery TEXT,  
    author_pair_column TEXT,  
    date_column TEXT,  
    max_iterations INT DEFAULT 100,  
    tolerance FLOAT DEFAULT 1e-4
) RETURNS SETOF logistic_regression_result
AS $$
    import pandas as pd
    import plpy
    import numpy as np

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def compute_loss(X, y, weights, bias):
        m = len(y)
        predictions = sigmoid(np.dot(X, weights) + bias)
        loss = - (1/m) * np.sum(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        return loss

    def recursive_gradient_descent(X, y, weights, bias, learning_rate=0.01, iteration=0, max_iterations=100, tolerance=1e-4):
        if iteration >= max_iterations:
            return weights, bias

        m = len(y)
        predictions = sigmoid(np.dot(X, weights) + bias)
        loss = compute_loss(X, y, weights, bias)

        # Compute gradients
        dw = (1/m) * np.dot(X.T, predictions - y)
        db = (1/m) * np.sum(predictions - y)

        # Update weights and bias
        weights -= learning_rate * dw
        bias -= learning_rate * db

        # Check for convergence
        if np.linalg.norm(dw) < tolerance and np.abs(db) < tolerance:
            return weights, bias

        # Recursive call for next iteration
        return recursive_gradient_descent(X, y, weights, bias, learning_rate, iteration + 1, max_iterations, tolerance)

    def train_logistic_regression(df, author_pair_column, date_column, max_iterations, tolerance):
        # Remove empty author pairs
        df = df[~df[author_pair_column].astype(str).isin(["['\"\"', '\"\"']"])]

        # Create target variable (whether the author pair will collaborate again)
        df = df.sort_values(by=[author_pair_column, date_column])
        df['will_collaborate_again'] = df.groupby(author_pair_column)[date_column].shift(-1).notnull().astype(int)

        # Drop NaN values in features
        df = df.dropna(subset=[date_column, 'will_collaborate_again'])

        # Feature engineering: Convert date to numerical format
        df[date_column] = pd.to_datetime(df[date_column])
        df['date_numeric'] = (df[date_column] - df[date_column].min()).dt.days

        # Define X (features) and y (target)
        X = df[['date_numeric']].values
        y = df['will_collaborate_again'].values

        # Initialize weights and bias
        weights = np.zeros(X.shape[1])
        bias = 0

        # Perform recursive gradient descent
        weights, bias = recursive_gradient_descent(X, y, weights, bias, max_iterations=max_iterations, tolerance=tolerance)

        return weights, bias

    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)

        # Train logistic regression
        weights, bias = train_logistic_regression(df, author_pair_column, date_column, max_iterations, tolerance)

        # Return the trained weights and bias
        result = []
        for weight in weights:
            result.append((weight, bias))

        # Return results as a set of logistic_regression_result
        for res in result:
            yield res

    except Exception as e:
        plpy.error(f"Error in logistic_regression_recursive_train: {str(e)}")
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


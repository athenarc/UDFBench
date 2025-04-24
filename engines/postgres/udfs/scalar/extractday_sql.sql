CREATE OR REPLACE FUNCTION extractday_sql(input_date text)
RETURNS INT
LANGUAGE plpgsql
AS $$
BEGIN

    IF trim(both '0123456789-' FROM input_date) = '' THEN
        RETURN NULLIF(split_part(input_date, '-', 3), ''); 
    ELSE
        RETURN NULL;  
    END IF;
END;
$$  IMMUTABLE STRICT PARALLEL SAFE;

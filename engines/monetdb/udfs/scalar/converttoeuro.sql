-- U4.	Converttoeuro: : Converts currency to euro, returns a float

CREATE or replace FUNCTION converttoeuro(input1 float, input2 string)
RETURNS float
LANGUAGE PYTHON
{
    euro_equals ={
        'EUR':1.00,
        '':1.00,
        'NOK':11.59,
        'AUD':1.63,
        'CAD':1.44,
        '$':1.09,
        'USD':1.09,
        'GBP':0.85,
        'CHF':0.98,
        'ZAR':20.41,
        'SGD':1.47,
        'INR':89.61,

        }
    def convert_toeuro(x,y):

        try:
            return float(x)/euro_equals[y]
        except:
            return None

    if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
        return numpy.array([convert_toeuro(arg1,arg2) if (arg1 and arg2 is not None and arg2 !='-') else None for arg1,arg2 in zip(input1,input2)], dtype=numpy.float64)
    else:
        return numpy.array( [convert_toeuro(input1,input2) if input1 and input2  is not None and input2!='-' else None],dtype=numpy.float64)

};

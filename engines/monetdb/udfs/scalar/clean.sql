-- U2. Performs a simple data cleaning task on the string tokens of a json list

CREATE OR REPLACE FUNCTION clean(input STRING)
RETURNS STRING
LANGUAGE PYTHON
{
    import json
    def removeshortwords(name):
        return " ".join([word for word in name.split(' ') if len(word) > 2])

    def sortname(name):
        return " ".join(sorted(name.split(' ')))

    def cleanpy(val):
        try:
            name_list = json.loads(val)
            name_list = [name.lower() for name in name_list]
            name_list = [removeshortwords(name) for name in name_list]
            name_list = [sortname(name) for name in name_list]
            return json.dumps(sorted(name_list))
        except:
            return '[]'

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([cleanpy(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [cleanpy(input) if input is not None  and input!='-' else numpy.nan],dtype=object)

};

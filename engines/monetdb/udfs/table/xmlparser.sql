
-- U38.	Xmlparser :  Parses xml input and returns a table 

CREATE OR REPLACE FUNCTION xmlparser(subquery STRING,root_name STRING) 
RETURNS TABLE (record STRING)
LANGUAGE PYTHON {

    import xml.etree.ElementTree as ET
    import json
    import pandas as pd

    result_text = ''
    result_text = '\n'.join([str(row) for row in subquery])
    rows =[]

    try:
        root = ET.fromstring(result_text)

        for elem in root.iter(root_name[0]):
            record = {}
            for item in elem:
                record[item.tag] = item.text

            rows.append(json.dumps(record),)
        
        return pd.DataFrame(rows)

    except:
        return pd.DataFrame({'record':[]})
};

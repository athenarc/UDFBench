

-- U38.	Xmlparser :  Parses xml input and returns a table 

CREATE OR REPLACE FUNCTION xmlparser(subquery text,root_name text,column_name text) 
RETURNS SETOF RECORD AS $$
    import xml.etree.ElementTree as ET
    import plpy
    import json
    import re
    
    result_text = ''
    result_text = '\n'.join([str(row[column_name]) for row in plpy.execute(subquery)])

    try:
        root = ET.fromstring(result_text)

        for elem in root.iter(root_name):
            record = {}
            for item in elem:
                record[item.tag] = item.text
            yield (json.dumps(record),)

    except Exception as e:
        plpy.error(f"Error parsing XML: {str(e)}")
        return None
$$ LANGUAGE 'plpython3u'IMMUTABLE STRICT PARALLEL SAFE;


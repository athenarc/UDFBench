


-- U42.	Output: Exports the results of a subquery to local storage in various formats and returns a True in success 


CREATE OR REPLACE FUNCTION output(
    subquery text,
    output_format text,
    output_path text
)
RETURNS TABLE(res boolean)
LANGUAGE plpython3u
AS $$
    import csv
    import json
    import xml.etree.ElementTree as ET

    def execute_subquery(subquery):
        result = plpy.execute(subquery)
        return result

    def export_to_csv(result, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(result[0].keys())
            for row in result:
                csv_writer.writerow(row.values())
        return True

    def export_to_json(result, output_path):
        with open(output_path, 'w') as jsonfile:
            json.dump(list(result), jsonfile, indent=2)
        return True

    def export_to_xml(result, output_path):
        root = ET.Element('root')
        for row in list(result):
            result_element = ET.SubElement(root, 'publication')
            for key, value in row.items():
                ET.SubElement(result_element, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(output_path)
        return True

    try:
        result = execute_subquery(subquery)

        if output_format.lower() == 'csv':
            yield export_to_csv(result, output_path)
        elif output_format.lower() == 'json':
            yield export_to_json(result, output_path)
        elif output_format.lower() == 'xml':
            yield export_to_xml(result, output_path)
        else:
            plpy.error('Unsupported output format')
            yield False

    except Exception as e:
        plpy.error(str(e))
        yield False
$$ IMMUTABLE STRICT PARALLEL SAFE;


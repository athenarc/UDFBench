-- U42.	Output: Exports the results of a subquery to local storage in various formats and returns a True in success 

CREATE OR REPLACE FUNCTION output(
    doi string,
    amount string,
    numofpubs string,
    sdate string,
    output_path string,
    output_format string
)
RETURNS table (val boolean)
LANGUAGE PYTHON
{

    import csv
    import json
    import xml.etree.ElementTree as ET


    def export_to_csv(result, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(result.keys())
            
            # Write data
            for row in zip(*result.values()):
                writer.writerow(row)
        return True

    def export_to_json(result, output_path):
        with open(output_path, 'w') as jsonfile:
            json.dump(list(result), jsonfile, indent=2)
        return True

    def export_to_xml(result, output_path):
        root = ET.Element('root')
        for row in list(result):
            result_element = ET.SubElement(root, 'publications')
            for key, value in row.items():
                ET.SubElement(result_element, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(output_path)
        return True

        
    if type(doi)==numpy.ndarray or type(doi)==numpy.ma.core.MaskedArray:

        
        result = {'doi':doi,'amount':amount,'numofpubs': numofpubs,'sdate':sdate}

        if output_format[0].lower() == 'csv':
            return export_to_csv(result, output_path[0])
        elif output_format[0].lower() == 'json':
            return export_to_json(result, output_path[0])
        elif output_format[0].lower() == 'xml':
            return export_to_xml(result, output_path[0])
        else:
            return False

      
    else:
        return False
 
    
};

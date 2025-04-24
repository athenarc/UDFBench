
output 'output.csv' 'csv' select * from file('arxiv.xml','xml') union all select * from file('query2json.txt','json'); 

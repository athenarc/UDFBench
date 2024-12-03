
outputs 'output.csv' 'csv' select * from fileparse('arxiv.xml','xml') union all select * from fileparse('query2json.txt','json'); 

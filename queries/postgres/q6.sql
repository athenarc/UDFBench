explain (analyse,buffers)
select * from output('select * from file(''arxiv.xml'',''xml'') 
f(doi text, amount float, totalpubs int, sdate text) union all 
select * from file(''query2json.txt'',''json'')  
ff(doi text, amount float, totalpubs int, sdate text)','csv','output.csv'); 

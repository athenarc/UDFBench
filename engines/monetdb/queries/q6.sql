select * from output((select column1,column2,column3,column4,'output.csv','csv'  from
(select * from (select * from file_q6('query2json.txt','json')
union all select * from file_q6('arxiv.xml','xml')) as xx) as xxx));
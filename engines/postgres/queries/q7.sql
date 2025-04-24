explain (analyse,buffers)
 select aggregate_avg(jsoncount(citations)),aggregate_avg(jsoncount(authors)) 
 from file('pubmed_q7.txt','json') f(id text, citations text,authors text) ;
 

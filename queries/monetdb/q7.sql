select aggregate_avg(jsoncount(column2)),aggregate_avg(jsoncount(column3)) from file_q7('pubmed_q7.txt','json');

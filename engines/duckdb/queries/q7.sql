select aggregate_avg('select jsoncount(t.citations) as citations from(
    select unnest(file_q7(''pubmed_q7.txt'',''json'')) as t)','citations') as avg_cit,
     aggregate_avg('select jsoncount(t.authors) as authors from(
    select unnest(file_q7(''pubmed_q7.txt'',''json'')) as t)','authors') as avg_auth;
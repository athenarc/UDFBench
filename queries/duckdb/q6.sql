select output('select a.doi,a.amount,a.totalpubs,a.sdate
        from (select unnest(file(''query2json.txt'',''json''),recursive:=true)::STRUCT(amount DOUBLE,doi VARCHAR,sdate VARCHAR,totalpubs BIGINT ) as a)
        union all select b.doi,b.amount,b.totalpubs,b.sdate from 
        (select unnest(file(''arxiv.xml'',''xml''),recursive:=true)::STRUCT(amount DOUBLE,doi VARCHAR,sdate VARCHAR,totalpubs BIGINT ) as b)','output.csv','csv') as result;

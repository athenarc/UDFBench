CREATE EXTENSION plpython3u;

\i '../../udfs/aggregate/postgres/postgres_aggregate.sql'
\i '../../udfs/table/postgres/postgres_table.sql'
\i '../../udfs/scalar/postgres/postgres_scalar.sql'
\i '../../udfs/scalar/postgres/postgres_scalar_sql.sql'
\i '../../udfs/scalar/postgres/postgres_scalar_c.sql'


create unique index artifact_authorlistsidx on artifact_authorlists(md5(authorlist),artifactid)  where jsoncount(authorlist)<7;
create unique index artifact_authorlistsidx2 on artifact_authorlists(md5(authorlist),artifactid)  where jsoncount(authorlist)<=50;

explain (analyse,buffers)
select aggregate_avg(jsoncount(target)), aggregate_avg(jsoncount(authorlist))
from artifact_citations,artifact_authorlists where artifact_citations.artifactid=artifact_authorlists.artifactid;

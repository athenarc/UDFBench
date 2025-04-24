select aggregate_avg('Select jsoncount(target) as target
from artifact_citations,artifact_authorlists where artifact_citations.artifactid=artifact_authorlists.artifactid','target') as avg_cit,
     aggregate_avg('Select jsoncount(authorlist) as authorlist
from artifact_citations,artifact_authorlists where artifact_citations.artifactid=artifact_authorlists.artifactid','authorlist') as avg_auth;

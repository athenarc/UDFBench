
udfbench_schema = {
    "artifacts": [
                    "id", "title", "publisher", "journal", "date",
                    "year", "access_mode", "embargo_end_date", "delayed",
                    "authors", "source", "abstract", "type",
                    "peer_reviewed", "green", "gold"
                ],
    
    "projects": [
                    "id","acronym","title","funder","fundingstring",
                    "funding_lvl0","funding_lvl1","funding_lvl2","ec39", 
                    "type", "startdate", "enddate", "start_year",
                    "end_year", "duration", "haspubs","numpubs",
                    "daysforlastpub","delayedpubs","callidentifier",
                    "code","totalcost","fundedamount","currency"],

    "projects_artifacts": ["projectid","artifactid","provenance"],
    "artifact_authorlists": ["artifactid","authorlist"],
    "artifact_citations": ["artifactid","target","citcount"],
    "artifact_abstracts": ["artifactid","abstract"],
    "artifact_authors": ["artifactid","affiliation","fullname","name",
                            "surname","rank","authorid"],
    "views_stats": ["date","artifactid","source","repository_id","count"],
}
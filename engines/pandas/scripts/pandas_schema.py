class Artifacts:
    id = '0'
    title = '1'
    publisher = '2'
    journal = '3'
    date = '4'
    year = '5'
    access_mode = '6'
    embargo_end_date = '7'
    delayed = '8'
    authors = '9'
    source = '10'
    abstract = '11'
    type = '12'
    peer_reviewed = '13'
    green = '14'
    gold = '15'

class ArtifactCitations:
    artifactid = '0'
    target = '1'
    citcount = '2'

class ArtifactAuthorlists:
    artifactid = '0'
    authorlist = '1'

class ViewsStats:
    date = '0'
    artifactid = '1'
    source = '2'
    repository_id = '3'
    count = '4'

class ArtifactAuthors:
    artifactid = '0'
    affiliation = '1'
    fullname = '2'
    name = '3'
    surname = '4'
    rank = '5'
    authorid = '6'

class Projects:
    id = '0'
    acronym = '1'
    title = '2'
    funder = '3'
    fundingstring = '4'
    funding_lvl0 = '5'
    funding_lvl1 = '6'
    funding_lvl2 = '7'
    ec39 = '8'
    type = '9'
    startdate = '10'
    enddate = '11'
    start_year = '12'
    end_year = '13'
    duration = '14'
    haspubs = '15'
    numpubs = '16'
    daysforlastpub = '17'
    delayedpubs = '18'
    callidentifier = '19'
    code = '20'
    totalcost = '21'
    fundedamount = '22'
    currency = '23'

class ProjectsArtifacts:
    projectid = '0'
    artifactid = '1'
    provenance = '2'
    
class ArtifactAbstracts:
    artifactid = '0'
    abstract = '1'
    
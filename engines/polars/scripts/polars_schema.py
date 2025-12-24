from ordered_set import OrderedSet

Artifacts = OrderedSet((
    'id',
    'title',
    'publisher',
    'journal',
    'date',
    'year',
    'access_mode',
    'embargo_end_date',
    'delayed',
    'authors',
    'source',
    'abstract',
    'type',
    'peer_reviewed',
    'green',
    'gold',
))
ArtifactCitations = OrderedSet((
    'artifactid',
    'target',
    'citcount',
))
ArtifactAuthorlists = OrderedSet((
    'artifactid',
    'authorlist',
))
ViewsStats = OrderedSet((
    'date',
    'artifactid',
    'source',
    'repository_id',
    'count',
))
ArtifactAuthors = OrderedSet((
    'artifactid',
    'affiliation',
    'fullname',
    'name',
    'surname',
    'rank',
    'authorid',
))
Projects = OrderedSet((
    'id',
    'acronym',
    'title',
    'funder',
    'fundingstring',
    'funding_lvl0',
    'funding_lvl1',
    'funding_lvl2',
    'ec39',
    'type',
    'startdate',
    'enddate',
    'start_year',
    'end_year',
    'duration',
    'haspubs',
    'numpubs',
    'daysforlastpub',
    'delayedpubs',
    'callidentifier',
    'code',
    'totalcost',
    'fundedamount',
    'currency',
))
ProjectsArtifacts = OrderedSet((
    'projectid',
    'artifactid',
    'provenance',
))  
ArtifactAbstracts = OrderedSet((
    'artifactid',
    'abstract',
))

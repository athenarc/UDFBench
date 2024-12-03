
explain (analyse,buffers) select * from aggregate_top('SELECT arxivid, 
             pubmedid, 
             JACCARD(arxivterms, 
                           pmcterms) 
             AS similarity from (select * from (SELECT pubmed_df as arxivid,
                    JPACK(
                    FREQUENTTERMS(
                    STEM(
                    FILTERSTOPWORDS(
                    KEYWORDS(
                    abstract
                    ))), 10)) 
                    AS arxivterms
             FROM file(''arxiv.csv'', ''csv'') f1(pubmed_df text, abstract text) ),
              (SELECT pubmedid, 
                   JPACK(
                   FREQUENTTERMS(
                   STEM(
                   FILTERSTOPWORDS(
                   KEYWORDS(
                   abstract
                   ))), 10)) 
                   AS pmcterms
             FROM file(''pubmed.txt'', ''json'') f2(pubmedid text, abstract text)))',
             5,'arxivid','similarity') f3(arxivid text,pubmedid text,similarity float);


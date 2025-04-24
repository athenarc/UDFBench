-- U14.	Frequentterms: Returns a space separated text containing the most N% frequent tokens 


CREATE or replace FUNCTION frequentterms(input1 string, input2 integer)
RETURNS string
LANGUAGE PYTHON
{
    import heapq
    from collections import Counter
    
    def frequent_term(words,N):
        try:
            words_list = words.split()
            word_counts = Counter(word.lower() for word in words_list)
            frequent_terms = heapq.nlargest(N, word_counts, key=word_counts.get)
            return ' '.join([word for word in frequent_terms])
        except:
            return ''


    if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
        return numpy.array([frequent_term(arg1,input2)  if arg1 is not None and arg1!='-' else numpy.nan for arg1 in input1], dtype=object)
    else:
        return numpy.array([frequent_term(input1,input2)  if input1 is not None and input1!='-' else numpy.nan], dtype=object)

};


-- U14.	Frequentterms: Returns a space separated text containing the most N% frequent tokens 

CREATE or replace FUNCTION frequentterms(input1 text, input2 integer)
    RETURNS text
AS $$

    import heapq
    from collections import Counter

    def frequent_term(words,N):
        words_list = words.split()
        word_counts = Counter(word.lower() for word in words_list)
        frequent_terms = heapq.nlargest(N, word_counts, key=word_counts.get)
        return ' '.join([word for word in frequent_terms])
    try:
        return frequent_term(input1,input2)
    except:
        return ''

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
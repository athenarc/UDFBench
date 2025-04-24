

import heapq

from collections import Counter


def frequentterms(input1, input2):
    def frequent_term(words,N):
        words_list = words.split()
        word_counts = Counter(word.lower() for word in words_list)
        frequent_terms = heapq.nlargest(N, word_counts, key=word_counts.get)
        return ' '.join([word for word in frequent_terms])
    if input1:
        try:
            return frequent_term(input1,input2)
        except:
            return ''
    else:
        return None

frequentterms.registered = True

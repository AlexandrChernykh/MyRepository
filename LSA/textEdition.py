import re
import numpy as np


def tokens_to_freq(tokens):
    words, count = np.unique(tokens, return_counts=True)
    return [words, count]


def tokenize(line, stopwords):
    result = line.split(" ")
    if not stopwords:
        return result
    filtered_result = []
    for token in result:
        if token not in stopwords and token != '':
            filtered_result.append(token)
    return filtered_result


def combine_token_sets(tokens_array):
    res = []
    for tokens in tokens_array:
        for token in tokens:
            res.append(token)
    return res


def tokens_freq_to_matrix(tokens_freq,documents_array):
    names=np.unique(combine_token_sets([x[0] for x in tokens_freq]))
    documents=[]
    for k in range(0, len(tokens_freq)):
        if documents_array:
            documents.append(documents_array[k])
        else:
            documents.append("Unnamed№"+str(k+1))
    tokens=[]
    summary=[]
    for i in range(0, len(names)):
        word_line = []
        summary_line = 0
        for k in range(0, len(tokens_freq)):
            if names[i] in tokens_freq[k][0]:
                freq = tokens_freq[k][1][np.where(tokens_freq[k][0] == names[i])[0]][0]
                word_line.append(freq)
                summary_line += freq
            else:
                word_line.append(0)
        tokens.append(word_line)
        summary.append(summary_line)
    return [names, documents, tokens, summary]


def clear_matrix(tokens_matr):
    names = []
    documents = tokens_matr[1]
    tokens = []
    summary = []
    for i in range(0, len(tokens_matr[0])):
        if tokens_matr[3][i] > 1:
            names.append(tokens_matr[0][i])
            tokens.append(tokens_matr[2][i])
            summary.append(tokens_matr[3][i])
    return [names, documents, tokens, summary]


def remove_punctuations(line):
    first_pass = re.sub("([,.!?+\-*/=()\[\]<>@#№\"$;%:^•«»\n„“—–])", "", line)
    return re.sub("(  )", " ", first_pass)




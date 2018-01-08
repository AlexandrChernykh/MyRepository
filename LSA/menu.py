import fileloader as fl
import StemmerPorter as sp
import textEdition as te
from sklearn.feature_extraction.text import TfidfTransformer
import numpy.linalg as linalg
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

draw_words = False
draw_words_names = False

draw_article_names = False

swords = []
file = open("stopwords.txt", "r", encoding='utf-8')
for line in file:
    swords.append(line[:len(line)-1])
file.close()

# colors=['#FF0000', '#00FF00', '#0000FF', '#957400', '#9574d1', '#fd0dfd']
colors = ListedColormap(['#FF0000', '#FF00FF', '#0000FF', '#00E6FF', '#00FF3C', '#E6FF00', '#FF9100', '#DCAFAF'])

tfidf = TfidfTransformer(smooth_idf=True)
documents_color = []
documents_names = []
counts = []
for dir_id in range(0,fl.get_groups_amount()):
    files, groupName = fl.get_group(dir_id, True)
    print("Group "+groupName+" processing!")
    for fileName in files:
        file = open(fileName[0], "r", encoding='utf-8')
        tokens = []
        for line in file:
            tokens = te.combine_token_sets(
                [tokens,
                 te.tokenize(te.remove_punctuations(line), swords)]
            )
        file.close()
        tokens = [sp.stem(x) for x in tokens]
        counts.append(te.tokens_to_freq(tokens))
        documents_color.append(dir_id)
        documents_names.append(fileName[1])
    print("Done!")
    print("-----------------------------------------")
print("Calculating")
res = te.tokens_freq_to_matrix(counts, documents_names)
res = te.clear_matrix(res)
matrix = res[2]
# matrix = tfidf.fit_transform(matrix).toarray()
u, _, v = linalg.svd(matrix)
print("Done!")
print("-----------------------------------------")

print("Drawing")
fig = plt.figure()
ax = fig.add_subplot(111)

if draw_words:
    if draw_words_names:
        for i in range(0,len(u)):
            ax.text(-u[i][0], u[i][1], res[0][i], fontsize=10)
    ax.plot([-x[0] for x in u], [x[1] for x in u], 'bs')
ax.scatter([-x for x in v[0]], [x for x in v[1]], c=documents_color, cmap=colors)
if draw_article_names:
    for i in range(0, len(v[0])):
        ax.text(-v[0][i], v[1][i], res[1][i], fontsize=10)
#ax.ylim([-0.1, 0.1])
#ax.xlim([-0.05, 0.05])
plt.show()


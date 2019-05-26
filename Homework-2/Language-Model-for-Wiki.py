
#%%
import pandas as pd
import glob
import re
import jieba
import collections
from functools import reduce

#%% [markdown]
# Language Model for Wikipedia data
# 
# * Load Wikipedia Dataset
# * Remove the characters that are non-word or non-digital
# * Build language model based on 2-gram
# * Test


#%% [markdown]
# ### Load Wikipedia Data
#%%
home = '/home/yikang/Desktop/TextData/wikiarticles'
all_articles = glob.glob(home + '/*/*')

#%%
def token(string):
    """
    @string: `string`
    @return: `string`, string after cleaning the non-words/non-digits characters
    """
    return ' '.join(re.findall('[\w|\d]+', string))

def merge2(gen):
    """
    merget adjacent words in the `generator`
    @gen: `generator(string)`, a generator of string containing words
    @return: `generator(string)`, a generator of string
    """
    for i in gen:
        nex = next(gen)
        yield i + nex

# %%
# load articles(partial)
TEXT = ""
for file in all_articles[:50]:
    print(file, "complete")
    TEXT += token(open(file, 'r').read())

#%% [markdown]
# ### Clean and build word Counter.
#%%
# build corpus
Text_seg_1 = jieba.cut(TEXT)                    # segment Text to 1-grams
vocabulary = collections.Counter(Text_seg_1)    # frequencies for 1-grams
Text_seg_2 = merge2(jieba.cut(TEXT))            # segement Text to 2-grams
vocabulary_2 = collections.Counter(Text_seg_2)  # frequencies for 2-grams

# compute the sum of frequencies
_gram_1 = sum(vocabulary.values())
_gram_2 = sum(vocabulary_2.values())

# %% [markdown]
# ### Build Language Model
# %%
# 1-gram probablity
def get_prob(word):
    """
    fetch the estimated probability of an 1-gram
    @word: `string`
    @return: `float`
    """
    esp = 1 / _gram_1
    if word in vocabulary:
        return vocabulary[word] / _gram_1
    else:
        return esp

# 2-gram probability
def get_combination_prob(word1, word2):
    """
    return the joint probability of word1 and word2,
    @word1, word2: `string`
    @return: `float`, estimated joint probability of w1 and w2 (2-gram)
    """
    if word1 + word2 in vocabulary_2:
        return vocabulary_2[word1 + word2] / _gram_2
    else:
        return 1 / _gram_2

def get_prob_2gram(w1, w2):
    """
    @w1, w2: `sttring`.
    @return: `float`, conditional probability of w1 and w2 (2-gram/1-gram)
    """
    return get_combination_prob(w1, w2) / get_prob(w1)

# language model
def language_model_of_2gram(sentence):
    """
    return the joint probability of a sequence of words
    @sentence: `string`, sequence of words
    @return: `float`, the estimated joint probability
    """
    sentence_prob = 1
    words = list(jieba.cut(sentence))
    for i, word in enumerate(words):
        if i == 0:
            prob = get_prob(word)
        else:
            prev = words[i-1]
            prob = get_prob_2gram(prev, word)
        sentence_prob *= prob
    return sentence_prob

# compare sentence pair
def compare_(sent1, sent2):
    p1, p2 = language_model_of_2gram(sent1), language_model_of_2gram(sent2)
    return sent1 if p1 >= p2 else sent2

#%%
# test
print(language_model_of_2gram("明天去北京"))
print(language_model_of_2gram("看没看新闻"))


need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "我去吃火锅，今晚 今晚我去吃火锅"
]
for i in need_compared:
    for j in need_compared:
        if i == j:
            continue
        else:
            print(compare_(i, j))


# %% [markdown]
# ### Applications 
# * Voice Recognization
# * Sogou pinyin input
#   * 通过输入的首字母序列，从左到右用rolling window的形式来从数据库中搜寻最大可能的词语段。
# * Auto correction in search engine
#   * 将输入的句子分割成片段，计算各个片段的再词库中的概率，对片段概率低的进行修改。
# * Abnormal Detection
#   * 针对不同用户的行为数据/用词顺序建模，记录习惯，当该用户多次进行违反行为习惯的操作时，即行为顺序的估计概率很低。说明存在非正常操作。
#%%
!pwd
!ls

#%%
import pandas as pd
import os

database = "./sqlResult_1558435.csv"
dataframe = pd.read_csv(database, encoding='gb18030')
dataframe.head(6)

#%%
all_articles = [str(a) for a in dataframe['content'].tolist()]
all_articles[:3]    


#%% 
import re
def token(string):
    """
    segement sentences to pieces.
    @string: `string`
    @return: `string`
    """
    return ' '.join(re.findall('[\w|\d]+', string))

#%%
string = '***&& %%## this is a BIGGGGGGGGG thing BI and BIGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg'

#%% 
text = ''
for a in all_articles:
    text += a
print('Length of text: {}'.format(len(text)))

#%%
from functools import reduce
txt_from_reduce = reduce(lambda a1, a2: a1 + a2, all_articles[:10])
txt_from_reduce


#%% [markdown]
# ## Regular Expression

#%%
pattern = '\w+'
re.findall(pattern, string)

#%% 
import requests
url = 'http://movie.douban.com/'
response = requests.get(url)
url_pattern = re.compile('http://movie.douban.com/subject/\d+/\?/from=showing')
image_pattern = re.compile('https://img3.doubanio.com/view/photo/s_ratio_poster/public/\w\d+.\w+')
html_content = response.text
original_string = 'href="https://movie.douban.com/subject/26213252/?from=showing">'

#%%
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

set(image_pattern.findall(html_content))
urls = image_pattern.findall(html_content)

f = requests.get(urls[0])
a = Image.open(BytesIO(f.content))
plt.imshow(a)
plt.show()

#%% [markdown]
# ## Get all tokens

#%%
import jieba
def cut(string):
    return list(jieba.cut(string))
cut("这是一个测试")

#%%
ALL_TOKENS = cut(text)

#%%
valid_tokens = [t for t in ALL_TOKENS if t.strip() and t!= 'n']

#%%
len(valid_tokens)
valid_tokens[:20]

#%% [markdown]
# ## Get the frequences of works

#%%
from collections import Counter
Counter([1, 1, 2, 2, 2, 3, 1, 0])

#%%
words_count = Counter(valid_tokens)
words_count.most_common(10)

#%%
frequences = [f for w, f in words_count.most_common(100)]
x = [i for i in range(len(frequences[:100]))]
len(frequences)

#%%
plt.plot(x, frequences)

#%%
import numpy as np
plt.plot(x, np.log(frequences))

#%%
frequences_all = [f for w, f in words_count.most_common()]
frequences_sum = sum(frequences_all)
frequences_sum

#%%
1 / frequences_sum

#%%
def get_prob(word):
    """
    The estimated probability for word in vocabulary, assume 1 occurence for OOV by default
    @word: `string`, token
    @return `float`, probability
    """
    esp = 1 / frequences_sum
    if word in words_count:
        return words_count[word] / frequences_sum
    else:
        return esp
#%%
get_prob('我们')

#%%
def product(numbers):
    return reduce(lambda x1, x2: x1* x2, numbers)
product([1, 2, 3, 4, 10])

#%% 
def language_model_one_gram(string):
    words = cut(string)
    return product([get_prob(w) for w in words])

#%%
language_model_one_gram('广交会下个月举办')
language_model_one_gram('长征火箭下周发射')
language_model_one_gram('一个掉在了民房上')


#%%
need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "我去吃火锅，今晚 今晚我去吃火锅"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_one_gram(s1), language_model_one_gram(s2)
    
    better = s1 if p1 > p2 else s2
    
    print('{} is more possible'.format(better))
    print('-'*4 + ' {} with probility {}'.format(s1, p1))
    print('-'*4 + ' {} with probility {}'.format(s2, p2))

#%% [markdown]
# ## 2-gram

#%%
valid_tokens = [str(t) for t in valid_tokens]
all_2gram_words = [''.join(valid_tokens[i:i+2]) for i in range(len(valid_tokens[:-2]))]

#%%
_2_gram_sum = len(all_2gram_words)
_2_gram_counter = Counter(all_2gram_words)

def get_combination_prob(w1, w2):
    if w1 + w2 in _2_gram_counter: 
        return _2_gram_counter[w1 + w2] / _2_gram_sum
    else: 
        return 1 / _2_gram_sum

#%% 
get_combination_prob('去', '北京')
#%%
get_combination_prob('波音', '飞机')

#%%
get_combination_prob('苹果', '手机')

#%%
def get_prob_2_gram(w1, w2):
    return get_combination_prob(w1, w2) / get_prob(w1)

#%%
get_prob_2_gram('去', '沈阳')
get_prob_2_gram('去', '北京')

#%%
def language_model_of_2_gram(sentence):
    """
    @sentence: `string`, sequence of words.
    @return: `float`, joint probability of words
    """
    sentence_prob = 1
    words = cut(sentence)

    for i, word in enumerate(words):
        if i == 0:
            prob = get_prob(word)
        else:
            previous = words[i-1]
            prob = get_prob_2_gram(previous, word)
        sentence_prob *= prob
    return sentence_prob

#%%
print(language_model_of_2_gram("小明今天抽奖抽到一台苹果手机"))
print(language_model_of_2_gram("小明今天抽奖抽到一台波音飞机"))

##% [markdown]
# ## Review the problem using 2-gram

#%%

need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_of_2_gram(s1), language_model_of_2_gram(s2)
    
    better = s1 if p1 > p2 else s2
    
    print('{} is more possible'.format(better))
    print('-'*4 + ' {} with probility {}'.format(s1, p1))
    print('-'*4 + ' {} with probility {}'.format(s2, p2))

#%%
import random
grammar = """
sentence => noun_phrase verb_phrase 
noun_phrase => Article Adj* noun belong 
belong => de property
de => 的
property => 眼睛 | 裙子 | 胳膊 | 尾巴
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""

def parse_grammar(grammar_str, sep='=>'):
    """
    @grammar_str: `string`, grammer rules separated by `sep`
    @sep: `sep`
    @return, `dict`, a map from target to rules
    """
    grammar = {}
    for line in grammar_str.split('\n'):
        line = line.strip()
        if not line: continue
        
        target, rules = line.split()
        grammar[target.strip()] = [r.split() for r in rules.split('|')]
    return grammar


def gene(grammar_parsed, target='sentence'):
    """
    @grammer_parsed: `dict`, a map from target to rules
    @target: `string`, which will be the key in `grammar_parsed`
    """
    if target not in grammar_parsed: return target
    
    rule = random.choice(grammar_parsed[target])
    return ''.join(gene(grammar_parsed, target=r) for r in rule if r!='null')

g = parse_grammar(grammar)
random_generated = [gene(g) for _ in range(100)]

#%%
s1 = {1, 2, 3}
s2 = {4, 5, 2}
s1 | s2

#%%
sorted(random_generated, key=langauge_model_of_2_gram, reverse=True)
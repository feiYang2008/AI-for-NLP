#%% 
import pandas as pd
import os
import sklearn
import re
import pickle
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import jieba

#%%
print(os.listdir())

#%% [markdown]
# ## Load Data into Python from Json


#%%
fp = open('Homework-8-9/news.json', 'r', encoding='utf-8')
da = pd.read_json('Homework-8-9/news.json', encoding='utf-8')
da.head(10)

#%% [markdown]
# ## Pre-process data
# 1. Remove characters "新华社"
# 2. Create labels according to the source

#%%
da['label'] = da['source'].str.contains('新华').astype('int')
da.head(10)

#%%
pattern = re.compile('^新华社')
da['content'].fillna('')
da['text'] = da['content'].apply(lambda x: re.sub(pattern, '', x.strip()))
da[da['label'] == 1].head(100)

#%% [markdown]
# ### Cut the sentence into words (using jieba)

#%%
def cut(string):
    return ' '.join(jieba.cut(string))
da['text'] = da['text'].apply(cut)

#%% [markdown]
# ### Convert sentence into TFIDF sequence

#%%
# vectorizer = TfidfVectorizer(max_features=30000)
# x_text = vectorizer.fit_transform(da['text'])
vectorizer = pickle.load(open('Homework-8-9/vectorizer', 'rb'))
x_text = vectorizer.transform(da['text'])

#%%
print(x_text.shape)

#%% [markdown]
# ### Train test split

#%%
x_train, x_test, y_train, y_test = train_test_split(x_text, da['label'], test_size=0.3) 
print(x_train.shape)
print(x_test.shape)

#%% [markdown]
# ### Build Model

#%%
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
def get_performance(model, X_, y_):
    y_hat = model.predict(X_)
    y_prob = model.predict_proba(X_)
    print('percision is: {}'.format(precision_score(y_, y_hat)))
    print('recall is: {}'.format(recall_score(y_, y_hat)))
    print('roc_auc is: {}'.format(roc_auc_score(y_, y_hat)))
    print('confusion matrix: \n{}'.format(confusion_matrix(y_, y_hat, labels=[0, 1])))

#%% [markdown]
# ### Logistic Regression
#%%
lr_model = LogisticRegression()
lr_model.fit(x_train, y_train)
get_performance(lr_model, x_test.toarray(), y_test)

#%%
y_hat = lr_model.predict(x_test)
print(y_hat)
y_score = lr_model.predict_proba(x_test)[:,1]
print(roc_auc_score(y_test, y_score))
get_performance(lr_model, x_test.toarray(), y_test)

#%% 
# save model
import pickle
with open('vectorizer', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('lr_model', 'wb') as f:
    pickle.dump(lr_model, f)

#%% [markdown]
# ### Decision Tree model
tree_model = DecisionTreeClassifier(class_weight={0:5, 1:4}, criterion='entropy',
    max_features=5000)
tree_model.fit(x_train, y_train)
get_performance(tree_model, x_test, y_test)

#%%
pickle.dump(tree_model, open('tree_model', 'wb'))

#%% [markdown]
# ### Naive Bayes

#%%
# nb_model = GaussianNB()
# nb_model.fit(x_train.toarray(), y_train)
# get_performance(nb_model, x_test.toarray(), y_test)

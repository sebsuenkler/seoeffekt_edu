# Decision Tree Classification Learner

#include libs

import sys
sys.path.insert(0, '..')
from include import *

# ### 1. Data Preparation

# In[ ]:


# loading dataset
df = pd.read_csv('all_res.csv', encoding='latin-1', low_memory=False)

#df = df[:2000]

# removing duplicates (ignoring first 3 columns)
df.drop_duplicates(subset=df.columns.to_list()[3:], inplace=True)

# converting columns names to lowercase
df.rename(columns=lambda x: x.lower(), inplace=True)



# adding new column url_length
#df['url length'] = df['url'].str.len() - df['main'].str.len()

# removing columns that can't be used in ml
# it removes categorical columns as well as columns like id, query_id, etc.
id_cols = ['study', 'id', 'hash', 'query_id', 'query', 'rules', 'decision_tree', 'position', 'tools social', 'tools caching']
non_numeric_cols = df.select_dtypes('object').columns.to_list()
combined = [*id_cols, *non_numeric_cols]
to_drop = list(dict.fromkeys(combined))
df.drop(columns=to_drop, inplace=True)


# set all error encoded speed values to -1
df.loc[df['speed'] < 0, 'speed'] = -1

# replace missing value codes with -1
df.replace(-100, -1, inplace=True)
df.fillna(-1, inplace=True)

# apply classification rules to dataset
# create new column and assign -1 to all rows
df['seo class'] = -1

# 0: nicht optimiert
df['seo class'] = np.where(df['source not optimized'] == 1, 0, df['seo class'])

# 3: höchstwahrscheinlich optimiert
df['seo class'] = np.where((df['seo class'] != 0) & (
    (df['tools seo count'] > 0) |
    (df['source known'] == 1) |
    (df['source news'] == 1) |
    (df['source ads'] == 1) |
    (df['micros counter'] > 0)),
                           3,
                           df['seo class'])

# 2: wahrscheinlich optimiert
df['seo class'] = np.where((df['seo class'] == -1) & (
    (df['tools analytics count'] > 0) |
    (df['source shop'] == 1) |
    (df['source company'] == 1) |
    (df['check https'] == 1) |
    (df['check og'] == 1) |
    (df['check viewport'] == 1) |
    (df['robots_txt'] == 1) |
    (df['check sitemap'] == 1) |
    (df['check nofollow'] > 0) |
    (df['check canonical'] > 0) |
    ((df['speed'] > 0) & (df['speed'] < 3))),
                           2,
                           df['seo class'])

# 1: wahrscheinlich nicht optimiert
df['seo class'] = np.where((df['seo class'] == -1) & (
    (df['check title'] != 1) |
    (df['check description'] != 1) |
    (df['check identical title'] == 1) |
    (df['speed'] > 60) |
    (df['check og'] != 1),
                           1,
                           df['seo class'])

# save cleaned dataset // uncomment if it needs to be saved
#df.to_csv('data/data_prepared.csv', index=False)


# ### 2. Classification

# In[ ]:




from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate, StratifiedShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from imblearn.over_sampling import RandomOverSampler

# load dataset // uncomment if previous block wasn't run
#df = pd.read_csv('data/data_prepared.csv')

# remove missing values
df = df[~df.lt(0).any(1)]

# splitting X and y (predictor and target)
X = df.drop(columns=['seo class'])
y = df['seo class']

# oversample to balance classes
sampler = RandomOverSampler(random_state=42)
X, y = sampler.fit_resample(X, y)

# creating list of metrics to assess
metrics = ['accuracy',
           'precision_macro',
           'recall_macro',
           'f1_macro']

# creating a stratified shuffle split for cross validation
split = StratifiedShuffleSplit(n_splits=5, test_size=0.66, random_state=22)

# setting classifier to decision tree algorithm
clf = DecisionTreeClassifier()

#fit data before saving
clf.fit(X, y)

# train/test algorithm with 5-fold cross validation
cv = cross_validate(clf, X, y, scoring=metrics, cv=split)


# In[ ]:

# prints metrics
for k, v in cv.items():
    print(k, v.mean())


# ### 3. Exporting Model

# In[ ]:


# saves trained model as joblib file
from joblib import dump
dump(clf, 'dt_classifier.joblib')

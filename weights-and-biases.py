#%%
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
data = sns.load_dataset('penguins')
data = data.dropna()
X = data[['bill_depth_mm', 'bill_length_mm']].values
y = data['species'].values
X.shape, y.shape

#%%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
clf = LogisticRegression()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
y_probas = clf.predict_proba(X_test)

#%%
import numpy as np
labels = np.unique(y)
labels


#%%
import wandb
wandb.init(project='visualize-penguin-logistic')


#%%
# Log classifier visualizations
wandb.sklearn.plot_classifier(clf, X_train, X_test, y_train, y_test,
    y_pred, y_probas, labels, model_name='Logistic', feature_names=None)
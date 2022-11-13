from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load Iris dataset
iris = datasets.load_iris()
X = iris.data
print(type(X))
y = iris.target

x1 = X[:1, :]
print(x1)
# Standardize
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)
# print(X)

x1 = scaler.transform(x1)
print(x1)

# PCA
np_ = 2
pca = PCA(n_components=np_)
pca.fit(X)
print('pca.explained_variance_ratio_')
sg = pca.explained_variance_ratio_.reshape(np_, 1)
print(sg)
isg = np.eye(np_)
for i in range(np_):
    isg[i, i] = sg[i]
print(isg)
print('pca.components_')
print(pca.components_)
X = pca.transform(X)
# print(X)
# print(X.dot(pca.components_))
x1 = pca.transform(x1)
print(x1)


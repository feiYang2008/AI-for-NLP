from sklearn.datasets import load_boston
import numpy as np
from sklearn.utils import shuffle, resample
from mini_flow import *

data = load_boston()

losses = []

X_ = data['data']
y_ = data['target']

# normalize data
X_ = (X_ - np.mean(X_, axis=0)) / np.std(X_, axis=0)
n_features = X_.shape[1]
n_hidden = 10

W1_ = np.random.randn(n_features, n_hidden)
b1_ = np.zeros(n_hidden)
W2_ = np.random.randn(n_hidden, 1)
b2_ = np.zeros(1)

# Neural network
X, y = Input(), Input()
W1, b1 = Input(), Input()
W2, b2 = Input(), Input()

l1 = Linear(X, W1, b1)
s1 = Sigmoid(l1)
l2 = Linear(s1, W2, b2)
cost = MSE(y, l2)

# define feed_dict

feed_dict = {
    X: X_, 
    y: y_,
    W1: W1_,
    b1: b1_,
    W2: W2_,
    b2: b2_
}

epochs = 5000

# Total number of examples
m = X_.shape[0]
batch_size = 16
steps_per_epoch = m // batch_size

graph = topological_sort(feed_dict)
trainables = [W1, b1, W2, b2]

print("Total number of examples = {}".format(m))

# training 
for i in range(epochs):
    loss = 0
    for j in range(steps_per_epoch):
        X_batch, y_batch = resample(X_, y_, n_samples=batch_size)

        # Reset value of X and y Inputs
        X.value = X_batch
        y.value = y_batch

        _ = None
        forward_and_backward(graph)

        rate = 1e-2
        sgd_update(trainables, rate)

        loss += graph[-1].value
    
    if i % 100 == 0:
        print("Epoch: {}, Loss: {:.3f}".format(i+1, loss / steps_per_epoch))
        losses.append(loss)
    

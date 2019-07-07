import numpy as np

class Node:
    def __init__(self, inputs=[]):
        self.inputs = inputs
        self.outputs = []

        for n in self.inputs:
            n.outputs.append(self)
        
        self.value = None

        self.gradients = {
            # keys: inputs to this node
            # values: partials of this node with respect to that input
            # \partial{node}{input_i}
        }

    def forward(self):
        """
        Forward propagation.
        Compute the output values based on 'inbound_nodes' and store the 
        result in self.value.
        """

        return NotImplemented
    
    def backward(self):
        return NotImplemented


class Input(Node):
    def __init__(self):
        """
        An Input node has no inbound nodes.
        So no need to pass anything to the Node Instantiation
        """
        Node.__init__(self)
    
    def forward(self, value=None):
        """
        input-node is the node where the value may be passed
        as an argument to forward().
        All other node implementations should get the value of the 
        previous node from self.inbound_nodes
        
        Example: 
        val0: self.inbound_nodes[0].value
        """
        if value is not None:
            self.value = value
        
        # It's is input node, when need to forward, this node initiate self's value.

        # Input subclass just holds a value, such as a data feature or a model parameter(weight/bias)

    def backward(self):
        self.gradients = {self: 0}
        for n in self.outputs:
            grad_cost = n.gradients[self]
            self.gradients[self] = grad_cost * 1
        
        # input N --> N1, N2
        # \partial L / \partial N
        # ==> \partial L / \partial N1 * \partial N1 / \partial N
    

class Add(Node):
    def __init__(self, *nodes):
        Node.__init__(self, nodes)
    
    def forward(self):
        self.value = sum(map(lambda n: n.value, self.inputs))


class Linear(Node):
    def __init__(self, nodes, weights, bias):
        Node.__init__(self, [nodes, weights, bias])
    
    def forward(self):
        inputs = self.inputs[0].value
        weights = self.inputs[1].value
        bias = self.inputs[2].value
        self.value = np.dot(inputs, weights) + bias
    
    def backward(self):
        """
        initiate a partial for each of the inbound-nodes
        """
        self.gradients = {n: np.zeros_like(n.value) for n in self.inputs}

        for n in self.outputs:
            # Get the partial of the cost w.r.t this node
            grad_cost = n.gradients[self]
            self.gradients[self.inputs[0]] = np.dot(grad_cost, self.inputs[1].value.T)
            self.gradients[self.inputs[1]] = np.dot(self.inputs[0].value.T, grad_cost)
            self.gradients[self.inputs[2]] = np.sum(grad_cost, axis=0, keepdims=False)
    

class Sigmoid(Node):
    def __init__(self, inputs):
        Node.__init__(self, [inputs])
    
    def _sigmoid(self, x):
        return 1. / (1 + np.exp(-1 * x))
    
    def forward(self):
        self.x = self.inputs[0].value
        self.value = self._sigmoid(self.x)
    
    def backward(self):
        self.partial = self._sigmoid(self.x) * (1 - self._sigmoid(self.x))

        for n in self.outputs:
            # get the partial of the cost w.r.t to 
            grad_cost = n.gradients[self]

            self.gradients[self.inputs[0]] = grad_cost * self.partial


class MSE(Node):
    def __init__(self, y, a):
        Node.__init__(self, [y, a])

    def forward(self):
        y = self.inputs[0].value.reshape(-1, 1)
        a = self.inputs[1].value.reshape(-1, 1)
        assert (y.shape == a.shape)

        self.m = self.inputs[0].value.shape[0]
        self.diff = y - a
        self.value = np.mean(self.diff ** 2)

    def backward(self):
        self.gradients[self.inputs[0]] = (2 / self.m) * self.diff
        self.gradients[self.inputs[1]] = (-2 / self.m) * self.diff


def forward_and_backward(graph):
    """
    execute all the forward method of sorted_nodes
    """
    for n in graph:
        n.forward()
    
    for n in graph[::-1]:
        n.backward()

    # return outputnode.value

def topological_sort(feed_dict):
    """
    feed_dict: dictionary where the key is a `input` node 
        and the values is the respective `values` fed to the node
    return: a list of sorted_nodes
    """
    input_nodes = [n for n in feed_dict.keys()]

    G = {}
    nodes = [n for n in input_nodes]
    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in G:
            G[n] = {'in' : set(), 'out': set()}
        for m in n.outputs:
            if m not in G:
                G[m] = {'in': set(), 'out': set()}
            G[n]['out'].add(m)
            G[m]['in'].add(n)
            nodes.append(m)
    
    L = []
    S = set(input_nodes)

    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Input):
            n.value = feed_dict[n]

        L.append(n)
        for m in n.outputs:
            G[n]['out'].remove(m)
            G[m]['in'].remove(n)
            if len(G[m]['in']) == 0:
                S.add(m)        
    return L


def sgd_update(trainables, learning_rate=1e-2):
    for t in trainables:
        t.value += -1 * learning_rate * t.gradients[t]

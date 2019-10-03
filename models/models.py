import numpy as np
from loss import get_loss


class Model:

    def __init__(self, layers=None, optimizer='glorot', loss='mse', lr=0.001):
        self.layers = list() if layers is None else layers
        self._train = True
        self.add_loss(loss)
        self.add_optim(optimizer)
        self.add_learning_rate(lr)

    def __call__(self, x):
        return self.predict(x)

    def add_loss(self, loss_name):
        self._loss_func = get_loss(loss_name)

    def add_layer(self, layer):
        self.layers.append(layer)

    def add_optim(self, optimizer):
        self._optimizer = optimizer
        for layer in self.layers:
            layer.add_optim(optimizer)

    def add_learning_rate(self, lr):
        self._lr = lr

    def forward_pass(self, input):
        output = input
        for layer in self.layers:
            output = layer.forward_pass(output)
        output = self._loss_func.pred(output)
        return output

    def predict(self, input):
        return self.forward_pass(input)

    def backward_pass(self, true_value, pred_value):
        assert self._train, 'Network not set to train!'

        self._loss_func.calc(true_value, pred_value)
        dL_dy = self._loss_func.derivative(true_value)
        for layer in reversed(self.layers):
            dL_dy = layer.backward_pass(dL_dy)

    def set_train(self):
        self._train = True
        for layer in self.layers:
            layer.set_train()
    
    def set_eval(self):
        self._train = False
        for layer in self.layers:
            layer.set_eval()

    def train(self, data):
        for idx, (x, y) in enumerate(data):
            # TODO: Minibatches and shuffling, etc....
            pred = self.forward_pass(x)
            self.backward_pass(y, pred)


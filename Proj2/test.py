from Linear import *
from MSELoss import *
from ReLU import *
from Sequential import *
from Tanh import *
from math import pi, sqrt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch # à corriger

def generate_disc_set(nb=1000):
    train_set = torch.empty(nb, 2).uniform_()
    train_target = train_set - torch.empty(1).fill_(0.5)
    train_target = (train_target.pow(2).sum(1) < 1/sqrt(2*pi)) # Outside the circle is actually quite rare (about 2.4% of the samples)
    train_target = torch.Tensor([int(x) for x in train_target]) # à corriger
    return train_set, train_target

def create_model(nb_layers=3, layer_size=16):
    fc1 = Linear(2, layer_size)
    relu = ReLU()
    tanh = Tanh()
    layers_list = []
    for i in range(nb_layers):
        fc = Linear(layer_size, layer_size)
        layers_list.append(fc)
        layers_list.append(relu)
    fc2 = Linear(layer_size, 2)
    
    sequence = [fc1, relu] + layers_list + [fc2, tanh]
        
    return Sequential(sequence)


def compute_nb_errors(model, data_input, data_target, batch_size = 100):
    nb_errors = 0
    for b in range(0, data_input.size(0), batch_size):
        target = data_target[b:b+batch_size]
        output = model.forward(data_input[b:b+batch_size], no_grad=True).argmax(1)
        nb_errors += (target != output).sum()
    return nb_errors


def train_model(model, train_input, train_target, test_input, test_target,
                nb_epochs = 200, mini_batch_size = 100, lr = 5e-2,
               create_plot=False, title="error using mean-squares loss"):
    # still need to add the figure
    
    model.reset()
    
    if create_plot:
        train_errors, test_errors = [], []
    
    for e in range(nb_epochs):
        
        for b in range(0, train_input.size(0), mini_batch_size):
            output = model.forward((train_input.narrow(0, b, mini_batch_size))).argmax(1)
            mse = MSELoss() #create an instance of MSELoss
            loss = mse.forward(train_target.narrow(0, b, mini_batch_size), output)
            grdwrtoutput = mse.backward()
            model.zero_grad()
            model.backward(grdwrtoutput)
            model.optimization_step(lr)

        if create_plot:
            train_error = compute_nb_errors(model, train_input, train_target, batch_size=mini_batch_size)/train_input.size(0)
            test_error = compute_nb_errors(model, test_input, test_target, batch_size=mini_batch_size)/test_input.size(0)
            train_errors.append(train_error)
            test_errors.append(test_error)
            
    if create_plot:
        plt.plot(np.arange(nb_epochs), test_errors)
        plt.plot(np.arange(nb_epochs), train_errors)
        plt.xlabel("nb of epochs")
        plt.ylabel("train and test errors")
        plt.title(title)
        plt.show()    

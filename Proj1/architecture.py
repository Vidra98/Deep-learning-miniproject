import torch
import torch.nn as nn
import torch.nn.functional as F


class Naive_net(nn.Module):

    def __init__(self):
        super().__init__()
        self.sequence = nn.Sequential(
            nn.Conv2d(2, 16, kernel_size=3),
            nn.MaxPool2d(kernel_size=(2,2),stride=(2,2)),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 32, 3),
            nn.MaxPool2d(kernel_size=(2,2),stride=(2,2)),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Flatten(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64,2)
        )
        self.target_type = ["target0"]
        self.weights_loss = [1]

    def forward(self,input):
        output = self.sequence(input)
        return output


class MnistCNN(nn.Module):

    def __init__(self):
        super().__init__()
        self.sequence = nn.Sequential(
            nn.Conv2d(1,64,kernel_size=(3,3)),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(64,128,kernel_size=(3,3)),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(128,128,kernel_size=(3,3)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2,2),stride=(2,2)),
            nn.BatchNorm2d(128),
            nn.Conv2d(128,128,kernel_size=(3,3)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2,2),stride=(2,2)),
            nn.BatchNorm2d(128),
            nn.Flatten(),
            nn.Linear(128,64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64,10)
        )

    def forward(self,input):
        output = self.sequence(input)
        return output

class Simple_Net(nn.Module):
	
    def __init__(self):
        super().__init__()
        self.sequence = nn.Sequential(
            #simpleNet inspired implementation :https://github.com/Coderx7/SimpleNet
            #Conv1
            nn.Conv2d(1,64,kernel_size=(3,3)),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            
            nn.Conv2d(64,128,kernel_size=(3,3)), 
            nn.BatchNorm2d(128),
            nn.MaxPool2d(kernel_size=(2,2),stride=(2,2)),
            nn.ReLU(),
            
            nn.Conv2d(128,128,kernel_size=(3,3)), 
            nn.BatchNorm2d(128),
            nn.ReLU(),

            nn.Conv2d(128,128,kernel_size=(1,1)), 
            nn.BatchNorm2d(128),
            nn.ReLU(),

            nn.Conv2d(128,128,kernel_size=(3,3)), 
            
            nn.Flatten(),
            nn.Linear(128,64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64,10)
        )

    def forward(self,input):
        output = self.sequence(input)
        return output

class CrossArchitecture(nn.Module):

    def __init__(self):
        super().__init__()
        self.MnistNet = MnistCNN()
        self.NaiveNet = Naive_net()
        self.SimpleNet = Simple_Net()
        #target 1 is the class and target 0 is the comparison (??)
        self.target_type = ["target0","target1"]
        self.Linear1 = nn.Linear(22,11)
        self.Linear2 = nn.Linear(11,2)
        self.weights_loss = [0.5,0.5]
    
    def forward(self,input):
        """MnistCNN outputs a prediction for both digits, NaiveNet outputs the predicted comparison.
        No weights shared up to that point. Then, two linear layers take these predictions as input (size N*22).
        Output: predicted comparison of the two digits."""
        num1 = input[:,[0],:,:]
        num2 = input[:,[1],:,:]
        output_naive = self.NaiveNet(input) # shape = (N,2)
        output_num1 = self.MnistNet(num1).view(num1.shape[0],-1,1) # shape = (N,10,1)
        output_num2 = self.MnistNet(num2).view(num2.shape[0],-1,1) # shape = (N,10,1)
        output2 = torch.cat((output_num1,output_num2),dim=2) # shape = (N,10,2)
        output_num1 = output_num1.view(num1.shape[0],-1) # shape = (N,10)
        output_num2 = output_num2.view(num2.shape[0],-1) # shape = (N,10)
        output1 = torch.cat((output_num1,output_num2,output_naive),dim=1) # shape = (N,22)
        output1 = self.Linear1(output1)
        output1 = self.Linear2(output1) # shape = (N,2)
        return output1, output2

class oO_Net(nn.module):
    
    def __init__(self):
        super().__init__()
        self.Mnist_part = MnistCNN().sequence[:?]
        self.Naive_part = Naive_net().sequence[:?]
        self.target_type = ["target0","target1"]
        self.weights_loss = [0.5,0.5]
        # fc_{i,j} = jth fully-connected of the upper part if i=1, the lower part if i=2
        self.fc11 = nn.Linear(?,10)
        self.fc21 = nn.Linear(?,2)
        self.fc22 = nn.Linear(22,11)
        self.fc23 = nn.Linear(11,2)
        
    def forward(self,input):
        num1 = input[:,[0],:,:]
        num2 = input[:,[1],:,:]
        lower_output = self.Naive_part(input) # shape = (N,?)
        upper_output1 = self.Mnist_part(num1).view(num1.shape[0],-1,1)
        upper_output2 = self.Mnist_part(num2).view(num2.shape[0],-1,1)
        upper_output = torch.cat((upper_output1,upper_output2),dim=2) # shape = (N,?,2)
        # TODO: somehow sum both outputs after making them shape-compatible
        # TODO: then take upper and lower parts to self.fc_i
        pass
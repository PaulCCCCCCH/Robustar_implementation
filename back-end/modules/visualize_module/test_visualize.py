import torchvision,torch
from demo import *
model = torchvision.models.resnet50() 
visualize(model,'./0_3.jpg',32)
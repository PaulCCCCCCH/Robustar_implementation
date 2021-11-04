from torch.utils.tensorboard import SummaryWriter 
import torchvision
import numpy as np
model=torchvision.models.resnet18()
writer = SummaryWriter('.log')

#writer = SummaryWriter()
for i in range(10):
    x = np.random.random(1000)
    writer.add_histogram('distribution centers', x + i, i)
writer.close()
import os
import numpy as np
import torch
import json
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.optim as optim


def classify():
    train_on_gpu = torch.cuda.is_available()
    if not train_on_gpu:
        print('CUDA is not available.  Training on CPU ...')
    else:
        print('CUDA is available!  Training on GPU ...')
    train_dir = '../input/animals141/dataset/dataset'
    data_transform = transforms.Compose([transforms.RandomResizedCrop(224), transforms.ToTensor()])
    train_data = datasets.ImageFolder(train_dir, transform=data_transform)
    print('Num training images: ', len(train_data))

    batch_size = 20
    num_workers=0
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, 
                                            num_workers=num_workers, shuffle=True)
    with open('../input/animals141/translation.json') as file:
        content = json.load(file)
    classes = list(content.keys())
    vgg16 = models.vgg16(pretrained=True)

    for param in vgg16.features.parameters():
        param.requires_grad = False
    
    print(vgg16.classifier[6].in_features) 
    print(vgg16.classifier[6].out_features)

    vgg16.classifier[6] = nn.Linear(in_features=4096, out_features=151, bias=True)

    if train_on_gpu:
        vgg16.cuda()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(vgg16.classifier.parameters(), lr=0.001)
    n_epochs = 2
    for epoch in range(1, n_epochs+1):
        train_loss = 0.0
        for batch_i, (data, target) in enumerate(train_loader):
            if train_on_gpu:
                data, target = data.cuda(), target.cuda()
            optimizer.zero_grad()
            output = vgg16(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
            if batch_i % 20 == 19:
                print('Epoch %d, Batch %d loss: %.16f' %
                    (epoch, batch_i + 1, train_loss / 20))
                train_loss = 0.0
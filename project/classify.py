import os
import numpy as np
import torch
import json
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.optim as optim
from pandas.api.types import is_numeric_dtype

import statistics
class BatchNorm(nn.Block):
    # `num_features`: the number of outputs for a fully-connected layer
    # or the number of output channels for a convolutional layer. `num_dims`:
    # 2 for a fully-connected layer and 4 for a convolutional layer
    def __init__(self, num_features, num_dims, **kwargs):
        super().__init__(**kwargs)
        if num_dims == 2:
            shape = (1, num_features)
        else:
            shape = (1, num_features, 1, 1)
        # The scale parameter and the shift parameter (model parameters) are
        # initialized to 1 and 0, respectively
        self.gamma = self.params.get('gamma', shape=shape, init=init.One())
        self.beta = self.params.get('beta', shape=shape, init=init.Zero())
        # The variables that are not model parameters are initialized to 0 and 1
        self.moving_mean = np.zeros(shape)
        self.moving_var = np.ones(shape)

    def forward(self, X):
        # If `X` is not on the main memory, copy `moving_mean` and
        # `moving_var` to the device where `X` is located
        if self.moving_mean.ctx != X.ctx:
            self.moving_mean = self.moving_mean.copyto(X.ctx)
            self.moving_var = self.moving_var.copyto(X.ctx)
        # Save the updated `moving_mean` and `moving_var`
        Y, self.moving_mean, self.moving_var = batch_norm(
            X, self.gamma.data(), self.beta.data(), self.moving_mean,
            self.moving_var, eps=1e-12, momentum=0.9)
        return Y




    def train_test_split(data, train_size):
        train = data[:train_size]
        test = data[train_size:]
        num_classes = np.max(y_train) + 1
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        model = models.Sequential()
        model.add(layers.Dense(512, input_shape=(max_words,)))
        model.add(layers.Activation('relu'))
        # model.add(layers.Dropout(drop_ratio))
        model.add(layers.Dense(num_classes))
        model.add(layers.Activation('softmax'))

        return train, test

  
    def predict_text(my_text):
        text_labels = encoder.classes_
        text_example = [my_text]
        new_tokenize = keras.preprocessing.text.Tokenizer(num_words=max_words, char_level=False)
        new_tokenize.fit_on_texts(train_text)
        vector_text = new_tokenize.texts_to_matrix(text_example)[0]
        prediction = model.predict(np.array([vector_text]))
        predicted_label = text_labels[np.argmax(prediction)]
        return predicted_label

    def classify():
        if object.reource == "image":
            #train_on_gpu = torch.cuda.is_available()

            train_dir = '../input/animals141/dataset/dataset'
            data_transform = transforms.Compose([transforms.RandomResizedCrop(224), transforms.ToTensor()])
            train_data = datasets.ImageFolder(train_dir, transform=data_transform)
            print('Num training images: ', len(train_data))

        elif object.resource == "text":
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
                        print((epoch, batch_i + 1, train_loss / 20))
                        train_loss = 0.
                        


        for col in data.columns:
            if is_numeric_dtype(data[col]):
                print('%s:' % (col))
                print( data[col].mean())
                print(data[col].std())
                print( data[col].min())
                print(data[col].max())
                results=[]
                if len(results) == 4:

                    data2 = [int(results[0]), int(results[1])] 
                    data1 = [str(results[2]),'object']
                else:
                    data2 = [int(results[0]), int(results[1])] 
                    data1 = [str(results[-3]),'object']

            plt.bar(data1, data2) 


            plt.savefig('./static/images/barchart2.png')
            std = statistics.stdev(data2)
            median = statistics.median(data2)
            mean = statistics.mean(data2)
            variance = statistics.variance(data2)
            print(std,median,mean,variance)
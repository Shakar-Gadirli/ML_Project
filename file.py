from matplotlib import pyplot as plt 

plt.rcParams["figure.figsize"] = [7.00, 3.50] 
plt.rcParams["figure.autolayout"] = True 

data2 = [0, 1, 3, 2, 1] 
data1 = ['cat', 'tree', 'car', 'dog', 'human']

plt.bar(data1, data2) 

#plt.show()

plt.savefig('barchart2.png')


 # ~~~ Standard deviation ~~~

import statistics
std = statistics.stdev(data2)
median = statistics.median(data2)
mean = statistics.mean(data2)
variance = statistics.variance(data2)
print(std)
print(median)
print(mean)
print(variance)

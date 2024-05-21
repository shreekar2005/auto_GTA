import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data_x = list(np.load('training_data_x.npy'))
train_data_y= list(np.load('training_data_y.npy'))

df= pd.DataFrame(
    {
        0:train_data_x,
        1:train_data_y
    },
    #index=[0, 1, 2, 3],
)
print(df)
train_data=df.to_numpy()
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []
neutrals = []

#shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if np.all(choice == [1,0,0]):
        lefts.append([img,choice])
    elif np.all(choice == [0,1,0]):
        forwards.append([img,choice])
    elif np.all(choice == [0,0,1]):
        rights.append([img,choice])
    elif np.all(choice == [0,0,0]):
        neutrals.append([img,choice])
    else:
        print('no matches')


forwards = forwards[:len(lefts)][:len(rights)]#[:len(neutrals)]  #no need to balance neutral conditions
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]
neutrals = neutrals[:len(forwards)]
final_data = forwards + lefts + rights + neutrals
shuffle(final_data)

final_data_x=[]
final_data_y=[]
for data in final_data:
    final_data_x.append(data[0])
    final_data_y.append(data[1])

np.save('training_data_v2_x.npy', final_data_x)
np.save('training_data_v2_y.npy', final_data_y)

train_data_x = list(np.load('training_data_v2_x.npy'))
train_data_y= list(np.load('training_data_v2_y.npy'))

df= pd.DataFrame(
    {
        0:train_data_x,
        1:train_data_y
    },
    #index=[0, 1, 2, 3],
)
#print(df)
train_data=df.to_numpy()
print(Counter(df[1].apply(str)))
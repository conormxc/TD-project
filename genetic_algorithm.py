import tensorflow as tf
import numpy as np


def create_models(n):

    lst = [0]*n
    for i in range(n):
        lst[i] = tf.keras.models.Sequential([
            tf.keras.layers.InputLayer(input_shape=(41,)),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(144*3, activation='sigmoid')
        ])
    return lst



def network_to_tower(network,r,prev):

    input = np.zeros([41])
    input[r] = 1
    input = np.expand_dims(input, axis=0)
    print(np.size(input))
    vals = np.array(network(input))
    print(np.size(vals))

    for i in prev:
        vals[i] = 0
    v = vals.argmax()
    print(vals[0,v])

    for i in range(1,4):
        if i*144 > v:
            tower = i
            p = (i*144) - v
            a = np.floor(p/12)
            b = ((p/12 - a)*12)
            position = np.round(np.array([(a*50)+60,(b*50)+60]))
            print(tower,position)
            prev.append(v)
            return tower, position , prev
                      

a = create_models(10)
b,c,d = network_to_tower(a[1],0,[])

network = a[1]
input = np.zeros([41])
input[0] = 1
input = np.expand_dims(input, axis=0)
vals = np.array(network(input))
print(vals[0,d[0]])






import numpy as np



def text_to_array(file_path):

    Enemy_info = np.int32(np.loadtxt(file_path, delimiter=','))

    c = 0
    k = 0
    max_units = 0

    for i in range(len(Enemy_info)):
        c += 1
        v = Enemy_info[i,:]
        if v[0] == 0:
            max_units = max(c,max_units)
            k += 1
            c = 0

    combined_info = np.zeros([max_units,2,k])

    c = 0
    k = 0
    for i in range(len(Enemy_info)):
        v = Enemy_info[i,:]
        combined_info[c,:,k] = v
        c += 1
        if v[0] == 0:
            k += 1
            c = 0
    
    return np.int32(combined_info)



        


            

        

# -*- coding: utf-8 -*-


def find_num(text):
    return int([text[3:] for c in text if c.isdigit()][0])

def High_num(Direction_Staions):
    return max([find_num(i) for i in Direction_Staions if i != 'ref'])

def Low_num(Direction_Staions):
    return min([find_num(i) for i in Direction_Staions if i != 'ref'])

def Get_angles(data,Direction_Staions):
    save    = []
    count   = 0
    set_del = set()
    for i in range(len(data)):
        for j in range(len(data)):
            data[i][1]
            if data[i] == data[j] or data[i][1] == 'ref' or data[j][1] == 'ref' or data[i][0] != data[j][0] :
                continue
            key   = data[i][:2] + data[j][:2]
            key   = str(sorted(key))
            if key in set_del:
                continue
            set_del.add(key)
            num_i = find_num(data[i][1])
            num_j = find_num(data[j][1])
            if abs(num_i - num_j) == 1 or (find_num(data[j][1]) == High_num(Direction_Staions) and find_num(data[i][1]) == Low_num(Direction_Staions)):
                diff  = abs(data[i][2] - data[j][2])
                save.append ([data[i][1],data[i][0],data[j][1],diff])
                count +=1

    return save


data              = [['AJA1', 'AJA2', 6.207152777777786], ['AJA1', 'AJA3', 61.60729166666666], ['AJA1', 'AJA4', 84.46309027777778], ['AJA2', 'ref', 0.0], ['AJA2', 'AJA1', 112.44135416666667], ['AJA2', 'AJA3', 12.58305555555554], ['AJA2', 'AJA4', 35.50527777777777], ['AJA3', 'ref', 0.0], ['AJA3', 'AJA1', 108.30538194444443], ['AJA3', 'AJA2', 133.06618055555555], ['AJA3', 'AJA4', 31.699618055555554], ['AJA4', 'AJA1', 263.08556204099608], ['AJA4', 'AJA2', 287.90665047985226], ['AJA4', 'AJA3', 343.62705141054658]]
Direction_Staions = ["ref","AJA1","AJA2","AJA3","AJA4"]


angels = Get_angles(data,Direction_Staions)

print (angels)
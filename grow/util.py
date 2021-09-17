def simple_moving_average(seq, n):
    average = 0
    c = 0

    for i in range(len(seq),max(len(seq)-n,0),-1):
        # print(i)
        average += seq[i-1]
        c+=1
    
    average = average / c
    return average

class StateTable(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value
import graphs_part_b as graphs
import math
import random
import matplotlib.pyplot as plt

def Stimulated_Annealing(max_or_min,x_limit, y_limit):
    #defing/initilizing the contraints we need (temp and iter) 
    #taking a random start
    #a + (b-a) * random.random()
    temp = 30
    iter = 50
    #random start
    x = round(x_limit[0] + (x_limit[1]-x_limit[0]) * random.random())
    y = round(y_limit[0] + (y_limit[1]-y_limit[0]) * random.random())
    
    # the third funtion given
    func = ((((x**2)+(y**2))/4000) - (math.cos(x) * math.cos(y/math.sqrt(2))) + 1)
    
    #making the list of x, y and func values so that we can traverse...
    all_x_axis = [] 
    all_x_axis.append(x) 

    all_y_axis = []
    all_y_axis.append(y)

    func_values = []
    func_values.append(func)
    factor = 0.8

    for i in range(1, temp):
        temp = round(temp, 5)
        for j in range(1, iter):
            #trial = choose a random number
            updated_x = random.randint(x_limit[0], x_limit[1])
            updated_y = random.randint(y_limit[0], y_limit[1])
            trial = ((((updated_x**2)+(updated_y**2))/4000) - (math.cos(updated_x) * math.cos(updated_y/math.sqrt(2))) + 1)
            # delta = f(trial) = f(current)
            delta = trial - func

            if (temp == 0):
                break

            if max_or_min  == 'max':
                #forgetting the maximum the differnece 
                if delta > 0:
                    func = trial
                    func_values.append(func)
                    x , y = updated_x , updated_y
                    all_x_axis.append(updated_x)
                    all_y_axis.append(updated_y)                    
                else:
                    m = math.exp(delta/temp)
                    p = random.uniform(0, 1)
                    if p < m:
                        #current = trial
                        func = trial
                        func_values.append(func)
                        x , y = updated_x , updated_y
                        all_x_axis.append(updated_x)
                        all_y_axis.append(updated_y)
            else:
                #for getting the minimum the differnece 
                if delta < 0:
                    func = trial
                    func_values.append(func)
                    x , y = updated_x , updated_y
                    all_x_axis.append(updated_x)
                    all_y_axis.append(updated_y)                
                else:
                    m = math.exp(-delta/temp)
                    p = random.uniform(0, 1)
                    if p < m:
                        func = trial
                        func_values.append(func)
                        x , y = updated_x , updated_y
                        all_x_axis.append(updated_x)
                        all_y_axis.append(updated_y)
            #increment i for the loop to go on
            i = i + 1
        # temperature = factor * temperature       
        temp = factor * temp
    result = []
    result.append(func)
    result.append(func_values)
    result.append(all_x_axis)
    result.append(all_y_axis)
    
    return result  



# print(Stimulated_Annealing('max',[-20, 20], [-20, 20])
results =  Stimulated_Annealing('max',[-20, 20], [-20, 20])
# results =  Stimulated_Annealing('min',[-10, 10], [-10, 10])

last_value = results[0]
print(last_value)
function = results[1]
# print(func)
x_lst = results[2]
# print(x)
y_lst = results[3]
# print(y)


graphs.plotting_graphs(function, x_lst, y_lst)
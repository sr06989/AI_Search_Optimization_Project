import matplotlib.pyplot as plt

def plotting_graphs(function_values, x_lst, y_lst):
    fig = plt.figure(1)
    ax = fig.subplots(2)
    # ax = fig.subplots(hspace=2 )
    plt.subplots_adjust(hspace=0.3)
    
    ax[0].set_xlabel('x-axis')
    fig.align_xlabels()
    ax[0].set_ylabel('y-axis')
    fig.align_ylabels()
    ax[0].plot(function_values, color ='red', label= "Objective")
    leg = ax[0].legend(loc ="upper right")

    ax[1].set_xlabel('x-axis')
    fig.align_xlabels()
    ax[1].set_ylabel('y-axis')
    fig.align_ylabels()
    ax[1].plot(x_lst, color='blue', label="X")
    ax[1].plot(y_lst, color='green', linestyle='dashed', label="Y")
    leg = ax[1].legend(loc ="upper right")

    plt.show()
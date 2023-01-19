import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
import sys

def plot():
    plt.rcParams["font.family"] = "Times New Roman"

    fig, ax1 = plt.subplots(figsize=(10, 5))
    fontsize = 25

    y = [i*20 for i in range(7)]

    y_max = 0
    patterns =  [ 'o','.','D','x','s','_','x','s','x','go-']
    colors = ['indianred','mediumseagreen','royalblue']
    i = 0
    with open('./output/data-fails.csv', 'r') as f:
        for line in f:
            tokens = line.strip().split(',')
            alg_data = [float(tokens[i]) for i in range(1, len(tokens)-1)]
            if y_max < max(alg_data):
                y_max=max(alg_data)
            ax1.plot(y,alg_data, c= colors[i],marker = patterns[i],label=tokens[0])
            i = i+1
    plt.xlim([0, 120])
    plt.legend(loc='upper left',fontsize=fontsize-7,ncol=1)
    ax1.set_ylabel('Number of violations',size = fontsize)
    ax1.set_xlabel('Time(min)',size = fontsize)

    matplotlib.pyplot.yticks(fontsize=fontsize)
    matplotlib.pyplot.xticks(fontsize=fontsize)

    fig.savefig('output/img/efficiency.pdf',bbox_inches='tight', dpi=300)

if __name__ == '__main__':

    plot()
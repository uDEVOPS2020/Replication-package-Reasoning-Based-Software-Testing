from email import header
from collections import OrderedDict
from re import X
from tkinter import Y
from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
from matplotlib.lines import Line2D
import seaborn as sns
import matplotlib.patches as mpatches



if __name__ == "__main__":
    plt.rcParams["font.family"] = "Times New Roman"
    techniques = ["RBST","SBST-ML","ART"]
    fontsize = 25
    input_file = "./data_for_scripts/_csv/combined_all.csv"

    df = pd.read_csv(input_file)

    df_temp = df.copy()
    df_temp = df_temp.drop(df_temp.loc[df_temp['min_dist_with_other_vehicles']==1000].index)
    max = df_temp["min_dist_with_other_vehicles"].max()

    df = df.replace(1000,max)

    df_TOT = df[['technique','min_dist_with_other_vehicles']]
    df_all_TOT = pd.DataFrame()

    for t in techniques:
        df_temp = df_TOT.loc[df_TOT['technique'] == t]
        df_all_TOT[t] = df_temp['min_dist_with_other_vehicles'].reset_index(drop=True)




    fig, ax = plt.subplots(figsize=(9, 5))
    my_pal = {"RBST": (0.804, 0.361, 0.361, 0.1), "SBST-ML":(0.235, 0.702, 0.443, 0.1), "ART": (0.255, 0.412, 0.882, 0.1)}
    
    boxprops = {'edgecolor': 'k', 'linewidth': 2,"alpha": 0.7}
    lineprops = {'color': 'k', 'linewidth': 2}

    boxplot_kwargs = {'boxprops': boxprops, 'medianprops': lineprops,
                    'whiskerprops': lineprops, 'capprops': lineprops,
                    'width': 0.3, 'palette': my_pal}
    red = mpatches.Patch(color='indianred', label='RBST')
    green = mpatches.Patch(color='mediumseagreen', label='SBST-ML')
    blue = mpatches.Patch(color='royalblue', label='ART')
    rect = [red,green,blue]

    stripplot_kwargs = {'linewidth': 0.6, 'size': 6, 'alpha': 0.7,
                        'palette': my_pal}
    
    violin = sns.violinplot(data=df_all_TOT,orient='h', palette=my_pal,lw=5,inner=None,zorder=0)
    violin.collections[0].set_edgecolor((0, 0, 0, 1))
    violin.collections[0].set_facecolor((0.804, 0.361, 0.361, 0.3))
    violin.collections[1].set_edgecolor((0, 0, 0, 1))
    violin.collections[1].set_facecolor((0.235, 0.702, 0.443, 0.3))
    violin.collections[2].set_edgecolor((0, 0, 0, 1))
    violin.collections[2].set_facecolor((0.255, 0.412, 0.882, 0.3))
    sns.stripplot(data=df_all_TOT,orient='h', split=True, jitter=0.2, **stripplot_kwargs, zorder=1)
    ax.grid(axis='x') 

    plt.scatter(y=range(3),x=df_all_TOT.mean(),c="white",zorder=2,s=200,marker='>',edgecolors='k',linewidths=2)
    plt.scatter(y=range(3),x=df_all_TOT.median(),c='k',zorder=2,s=3000,marker='|',linewidths=2)

    plt.legend(handles=rect,loc='center',fontsize=fontsize-1,bbox_to_anchor=(0.5, 1.12),ncol=3,handletextpad=0.2,columnspacing=0.6)
    
    ax.set_yticks([])
    matplotlib.pyplot.xticks(fontsize=fontsize)
    plt.xlabel('Distance from vehicle (m)',fontsize=fontsize)
    plt.ylabel(None)
    plt.xlim(-5,45)
    plt.tight_layout()
    plt.show()

    fig.savefig('output/img/distances.pdf',bbox_inches='tight', dpi=300)
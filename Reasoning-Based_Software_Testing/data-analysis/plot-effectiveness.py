from inspect import indentsize
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

sns.set(style="ticks")


if __name__ == '__main__':
    plt.rcParams["font.family"] = "Times New Roman"
    df = pd.read_csv("output/output-cfails.csv",index_col=None)

    df_violin = pd.read_csv("output/output-cfails.csv",index_col=None) 
    techniques = ["RBST","SBST-ML","ART"]
    
    fontsize = 25

    # CSV
    df_means = df.groupby("technique").mean()
    df_means = df_means.drop(['repetition'], axis=1)

    df_means.to_csv("./output/_fails/RQ3_fail_means.csv")

    
    df_TOT = df_violin[['technique','count_TOT']]
    df_all_TOT = pd.DataFrame()

    for t in techniques:
        df_temp = df_TOT.loc[df_TOT['technique'] == t]
        df_all_TOT[t] = df_temp['count_TOT'].reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(9, 5))

    my_pal = {"RBST": (0.804, 0.361, 0.361, 0.1), "SBST-ML": (0.235, 0.702, 0.443, 0.1),"ART": (0.255, 0.412, 0.882, 0.1)}
    boxprops = {'edgecolor': 'k', 'linewidth': 2,"alpha": 0.6}
    lineprops = {'color': 'k', 'linewidth': 2}
    custom_lines_2 = [Line2D([0], [0], color='indianred', lw=8),
                Line2D([0], [0], color='mediumseagreen', lw=8),
                 Line2D([0], [0], color='royalblue', lw=8)]
    red = mpatches.Patch(color='indianred', label='RBST')
    green = mpatches.Patch(color='mediumseagreen', label='SBST-ML')
    blue = mpatches.Patch(color='royalblue', label='ART')
    rect = [red,green,blue]

    boxplot_kwargs = {'boxprops': boxprops, 'medianprops': lineprops,
                    'whiskerprops': lineprops, 'capprops': lineprops,
                    'width': 0.5, 'palette': my_pal}

    stripplot_kwargs = {'linewidth': 0.6, 'size': 6, 'alpha': 1,
                        'palette': my_pal}

    violin = sns.violinplot(data=df_all_TOT,orient='h', palette=my_pal,lw=5,inner=None,zorder=0)
    violin.collections[0].set_edgecolor((0, 0, 0, 1))
    violin.collections[0].set_facecolor((0.804, 0.361, 0.361, 0.3))
    violin.collections[1].set_edgecolor((0, 0, 0, 1))
    violin.collections[1].set_facecolor((0.235, 0.702, 0.443, 0.3))
    violin.collections[2].set_edgecolor((0, 0, 0, 1))
    violin.collections[2].set_facecolor((0.255, 0.412, 0.882, 0.3))
    sns.stripplot(data=df_all_TOT,orient='h', split=True, jitter=0.2, **stripplot_kwargs, zorder=1)

    
    plt.scatter(y=range(3),x=df_all_TOT.mean(),c="white",zorder=2,s=200,marker='>',edgecolors='k',linewidths=2)
    plt.scatter(y=range(3),x=df_all_TOT.median(),c='k',zorder=2,s=3000,marker='|',linewidths=2)
    ax.grid(axis='x') 

    plt.legend(handles=rect,loc='center',fontsize=fontsize-1,bbox_to_anchor=(0.5, 1.12),ncol=3,handletextpad=0.2,columnspacing=0.6)
    
    ax.set_yticks([])
    matplotlib.pyplot.xticks(fontsize=fontsize)
    plt.xlabel('Violations',fontsize=fontsize)
    plt.ylabel(None)
    plt.xlim(0)
    plt.tight_layout()
    plt.show()

    fig.savefig('output/img/effectiveness.pdf',bbox_inches='tight', dpi=300)
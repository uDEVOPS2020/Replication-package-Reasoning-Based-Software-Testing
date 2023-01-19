import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches


sns.set(style="ticks")

if __name__ == '__main__':
    plt.rcParams["font.family"] = "Times New Roman"
    fontsize = 25

    techniques = ["RBST","SBST-ML","ART"]

    df = pd.read_csv("./output/_diversity/combined_all.csv")

    df_in = df[['technique','input_d']]
    df_all_in = pd.DataFrame()

    for t in techniques:
        df_temp = df_in.loc[df_in['technique'] == t]
        df_all_in[t] = df_temp['input_d'].reset_index(drop=True)    

    fig, ax = plt.subplots(figsize=(9, 5))
    
    my_pal = {"RBST": (0.804, 0.361, 0.361, 0.1), "SBST-ML": (0.235, 0.702, 0.443, 0.1), "ART":(0.255, 0.412, 0.882, 0.1)}
    
    boxprops = {'edgecolor': 'k', 'linewidth': 2,"alpha": 0.6}
    lineprops = {'color': 'k', 'linewidth': 2}

    boxplot_kwargs = {'boxprops': boxprops, 'medianprops': lineprops,
                    'whiskerprops': lineprops, 'capprops': lineprops,
                    'width': 0.5, 'palette': my_pal}
    red = mpatches.Patch(color='indianred', label='RBST')
    green = mpatches.Patch(color='mediumseagreen', label='SBST-ML')
    blue = mpatches.Patch(color='royalblue', label='ART')
    rect = [red,green,blue]

    stripplot_kwargs = {'linewidth': 0.6, 'size': 6, 'alpha': 1,
                        'palette': my_pal}

    violin = sns.violinplot(data=df_all_in,orient='h', palette=my_pal,lw=5,inner=None,zorder=0)
    violin.collections[0].set_edgecolor((0, 0, 0, 1))
    violin.collections[0].set_facecolor((0.804, 0.361, 0.361, 0.3))
    violin.collections[1].set_edgecolor((0, 0, 0, 1))
    violin.collections[1].set_facecolor((0.235, 0.702, 0.443, 0.3))
    violin.collections[2].set_edgecolor((0, 0, 0, 1))
    violin.collections[2].set_facecolor((0.255, 0.412, 0.882, 0.3))
    sns.stripplot(data=df_all_in,orient='h', split=True, jitter=0.2, **stripplot_kwargs,zorder=0)
    ax.grid(axis='x') 

    plt.scatter(y=range(3),x=df_all_in.mean(),c="white",zorder=2,s=200,marker='>',edgecolors='k',linewidths=2)
    plt.scatter(y=range(3),x=df_all_in.median(),c='k',zorder=2,s=3000,marker='|',linewidths=2)

    plt.legend(handles=rect,loc='center',fontsize=fontsize-1,bbox_to_anchor=(0.5, 1.12),ncol=3,handletextpad=0.2,columnspacing=0.6)
    
    ax.set_yticks([])
    matplotlib.pyplot.xticks(fontsize=fontsize)
    plt.xlabel('Test Set Diameter',fontsize=fontsize)
    plt.ylabel(None)
    plt.tight_layout()
    plt.show()
    fig.savefig('output/img/diversity_input.pdf',bbox_inches='tight', dpi=300)
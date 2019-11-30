# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')


#%%
''' load the datasets
'''
tv_spot_data = pd.read_csv('tv_spot_data.csv', sep=",")

'''looking through the dataset
'''
tv_spot_data.head()
tv_spot_data.set_index('row')


#%%

'''# the number of contacts is decimal and has six digits after the decimal 
so that the unit of contacts is per million.
Two problems have been found:
1. It is abnormal that the value of visits is negative
2. It is weird that the number of visits is positive, whilst the number of contacts is equal to zero. 
In other words, people did not see the spots when they visit Trivago website.
To attempt to reveal reasons which cause this problem
'''

tv_spot_data['visits_check'] = tv_spot_data['visits'].apply(lambda x: 'true'
                                                            if x >= 0 else 'false')
v_c = tv_spot_data.loc[tv_spot_data['visits_check'] == 'false']
v_c.sort_values(by=['spot'])
v_c


#%%
'''# I cannot find any reasonable explanation
# The negative visits distribute in a variety of spots over time.
# I only can assume that there is a glitch through data transition. 
# During the data transition, the number of visits somehow became negative.
# So I manually correct the number of visits
'''

tv_spot_data['visits_correct'] = tv_spot_data['visits'].apply(lambda x: abs(x))


#%%
'''# In terms of the second problem, this is not any reasonable interpretation, either
So, I have to remove the row, in which the number of contacts is zero.
'''

tv_spot_data.drop(tv_spot_data[tv_spot_data['contacts'] == 0]. index, inplace=True)
tv_spot_data.shape


#%%
'''# The distribution of numerical columns
'''
tv_spot_data.describe()


#%%
'''
#check the structure
'''
tv_spot_data.info()

'''#Based on the information, the quality of data is good 
#In other words, there is no empty cell (NA) in the dataset#
'''

#%%
'''to convert column, date_time, into timestamp and to create new columns
    including weekday, month and hour
'''
tv_spot_data['date_time'] = pd.to_datetime(tv_spot_data['date_time'], 
                                           format='%Y-%m-%d %H:%M:%S', errors='ignore')


tv_spot_data['weekday'] = tv_spot_data['date_time'].dt.day_name()
tv_spot_data['month'] = tv_spot_data['date_time'].dt.month_name()
tv_spot_data['time'] = tv_spot_data['date_time'].dt.time
tv_spot_data['hour'] = tv_spot_data['date_time'].dt.hour

tv_spot_data.info()

#%%
'''split the column, spot, into 4 different columns including spot_id, 
    spot_name, spot_length, and spot_campaign
'''

new = tv_spot_data["spot"].str.split("_", n=4, expand=True)
tv_spot_data["spot_id"] = new[0]
tv_spot_data["spot_name"] = new[1]
tv_spot_data["spot_length"] = new[2]
tv_spot_data["spot_campaign"] = new[3]
tv_spot_data["spot_length"] = tv_spot_data['spot_length'].astype(int)
tv_spot_data.info()


#%%
'''To check the categorical columns
'''
tv_spot_data["weekday"].describe()

tv_spot_data["spot_length"] = tv_spot_data['spot_length'].astype(str)
tv_spot_data["spot_length"].describe()

tv_spot_data["channel"].describe()

tv_spot_data["month"].describe()


#%%
''' To check the dimention
tv_spot_data.shape

'''
#%%

'''Calulating metrics
   Visits per million contacts

'''
tv_spot_data['VPMC'] = tv_spot_data['visits_correct']/tv_spot_data['contacts']

''' Costs per visit CPV

'''
tv_spot_data['CPV'] = tv_spot_data['cost']/tv_spot_data['visits_correct']
#%%
''' I have found that in terms of cost per visit (CPV),
    there are outliers and will dig deeply
'''

tv_spot_data['CPV_check'] = tv_spot_data['visits'].apply(lambda x: 'true' if x == 0 else 'false')
CPV_c = tv_spot_data.loc[tv_spot_data['CPV_check'] == 'true']
CPV_c.sort_values(by=['CPV'])
CPV_c.info()

#%%
'''
There are 11 outliers in terms of cost per visit (CPV)
10 out of the 11 outliers results from the number of visits is zero, 
And one outlier is the result of that both the number of visits and the number of costs are equal to zero.
I will build up a new dataset, CPV_clear, in which the outliers have been removed.
The new dataset, CPV_clear, primarily focuses on the research regarding CPV.
I continue to apply the dataset, tv_spot_data when I study the visit per million contacts.

'''

CPV_clear = tv_spot_data.loc[tv_spot_data['CPV_check'] == 'false']
CPV_clear.sort_values(['CPV'])
CPV_clear.info()





#%%


'''
# Which were the spots aired - channel, month, weekday, the time of day?
# Def functions, whereby charts would be drawn, equips me to analyze the data
# The first one is to draw a chart
# The third one is to draw a chart with value on the bar
# The fourth one is to draw a couple of charts
# The fifth one is to draw a couple of charts with value on the bar

'''


def chart(a, b, c):
    '''describe the distribution of different channels, monthes and weekday
    '''

    d = sns.catplot(x=a, kind="count", palette="pastel", data=tv_spot_data, height=5)
    plt.title(b)
    d.set_xticklabels(rotation=c)
    d.savefig(str(d)+".png")
    return(d)


def chart_n(a, b, c):
    '''describe the cost of different channels, monthes and weekday
    '''
    gp = tv_spot_data.groupby(a).count()
    gp = gp.reset_index()
    g = sns.barplot(x=a, y='cost', data=gp, palette="pastel")

    for index, row in gp.iterrows():
        g.axes.text(row.name, row['cost'], round(row['cost'], 2), color='black', ha="center")
    plt.title(b)
    for item in g.get_xticklabels():
        item.set_rotation(c)
    g.figure.set_size_inches(7, 8)
    g.figure.savefig(str(g)+".png")
    return(g)

def chart_n_t(a, b, c):
    gp = tv_spot_data.groupby(a).count()
    gp = gp.reset_index()
    gp[a] = pd.to_datetime(gp[a], errors='ignore')
    g = sns.barplot(x=a, y='cost', data=gp, palette="pastel")
    for index, row in gp.iterrows():
        g.axes.text(row.name, row['cost'], round(row['cost'], 2), color='black', ha="center")
    plt.title(b)
    for item in g.get_xticklabels():
        item.set_rotation(c)
    g.figure.savefig(str(g)+".png")
    return(g)
    

def chart_m(a, b, c, d):
    e = sns.catplot(x=a, hue=b, kind="count", palette="pastel", data=tv_spot_data, height=3)
    plt.title(c)
    e.set_xticklabels(rotation=d)
    e.savefig(str(e)+".png")
    return(e)


def chart_m2(a, b, c):
    e = sns.catplot(x=a, kind="count", palette="pastel",
                    data=tv_spot_data, col=b, col_wrap=3, height=10)
    e.set_xticklabels(rotation=c)
    e.savefig(str(e)+".png")
    return(e)


#%%
chart_n('channel', 'Channels whereby spots were aired', 0)


#%%
# The channels that spots were aired
chart("channel", "Channels whereby spots were aired", 0)


#%%
'''The performance regarding VPMC and CPV
    Def functions, whereby charts would be drawn, equips me to analyze the data
'''


def chart2(a, b, c, f):
    d = sns.catplot(x=a, y=b, kind="bar", palette="pastel",
                    ci=None, data=tv_spot_data, height=5)
    plt.title(c)
    d.set_xticklabels(rotation=f)
    d.savefig(str(d)+".png")
    return(e)


def chart2c(a, b, c, f):
    d = sns.catplot(x=a, y=b, kind="bar", palette="pastel",
                    data=CPV_clear, ci=None, height=5)
    plt.title(c)
    d.set_xticklabels(rotation=f)
    d.savefig(str(d)+".png")
    return(e)


def chart2_n(a, b, c):
    gp = tv_spot_data.groupby(a).mean()
    gp = gp.reset_index()
    g = sns.barplot(x=a, y='VPMC', data=gp, palette="pastel")
    for index, row in gp.iterrows():
        g.axes.text(row.name, row['VPMC'], round(row['VPMC'], 4), color='black', ha="center")
    plt.title(b)
    for item in g.get_xticklabels():
        item.set_rotation(c)
    g.figure.savefig(str(g)+".png")
    return(g)


def chart2c_n(a, b, c):
    gp = CPV_clear.groupby(a).mean()
    gp = gp.reset_index()
    g = sns.barplot(x=a, y='CPV', data=gp, palette="pastel")
    for index, row in gp.iterrows():
        g.axes.text(row.name, row['CPV'], round(row['CPV'], 2), color='black', ha="center")
    plt.title(b) 
    for item in g.get_xticklabels():
        item.set_rotation(c)
    g.figure.savefig(str(g)+".png")
    return(g)


def chart_c(a, b, c, d, e, g):
    h_c = a.groupby(d).mean().sort_values(by=[b], ascending=g)
    x = h_c[b]
    y = h_c.index.astype(object)
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(y=y, x=x)
    ax.set_xlabel(xlabel=c, fontsize=16)
    ax.set_ylabel(ylabel=d, fontsize=16)
    ax.set_title(label=e, fontsize=20)
    f = plt.show()
    ax.figure.savefig(str(ax)+".png")
    return(f)


def chart_c_n(a, b, c, d, e, g):
    h_c = a.groupby(d).mean().sort_values(by=[b], ascending=g)
    x = h_c[b]
    y = h_c.index.astype(object)
    f, ax = plt.subplots(figsize=(12, 8))
    ax = sns.barplot(y=y, x=x)
    ax.set_xlabel(xlabel=c, fontsize=16)
    ax.set_ylabel(ylabel=d, fontsize=16)
    ax.set_title(label=e, fontsize=20)
    for p in ax.patches:
        width = p.get_width()
        ax.text(width-1.5, p.get_y()+p.get_height()/2.+ 0.2, '{:1.2f}'.format(width), ha="center")
    h = plt.show()
    ax.figure.savefig(str(ax)+".png")
    return(h)


#%%
chart2_n("spot_campaign", "Visits per million contacts in spot campaigns", 0)
#%%
chart_c_n(CPV_clear,"CPV", "CPV", "spot_name",
          "spots'names by cost per visit", True)
#%%
#Which Channels perform best
chart_c(tv_spot_data, "VPMC", "VPMC", "channel", "channels by visits per million contacts", False)


#%%


def c_c(mon, title, name):
    fb = CPV_clear.loc[CPV_clear['month'] == mon]

    gp = fb.groupby(['spot_campaign', 'spot_length']).mean().reset_index(level='spot_campaign', col_level=1).reset_index()
    fig, ax = plt.subplots()

    ax = sns.barplot(x='spot_campaign', y='CPV', hue='spot_length', data=gp, palette="pastel")
    ax.set_ylim(0, 50)
    for p in ax.patches:
        ax.annotate("%.0f" % p.get_height(), (p.get_x()+p.get_width()/2., p.get_height()-2), ha='center', va='center', rotation=0, xytext=(0, 20), textcoords='offset points') #vertical bars

    plt.title(title)
    plt.legend(loc='upper left')
    fig.set_size_inches(7, 8)
    fig.savefig(name+".png")
    return()

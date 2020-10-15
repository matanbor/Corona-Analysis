import numpy as np
import pandas as pd
from corona_data_sets import original_corona_recovered_data, original_corona_deaths_data, original_corona_confirmed_data
import matplotlib.pyplot as plt
import seaborn as sns

corona_data_sets_dict = {}
corona_data_sets_dict['original_corona_confirmed_data'] = original_corona_confirmed_data
corona_data_sets_dict['original_corona_deaths_data'] = original_corona_deaths_data
corona_data_sets_dict['original_corona_recovered_data'] = original_corona_recovered_data

def data_sets_shape(data_sets):
    try:
        for key, value in data_sets.items():
            print('Rows number of' , key, 'are:', value.shape[0])
            print('Columns number of ', key, ' are:', value.shape[1])
    except:
        print("Something got wrong - data_sets_shape")

def data_sets_columns(data_sets):
    try:
        for key, value in data_sets.items():
            print('The columns name of:', key, 'are:', list(value.columns))
    except:
        print("Something got wrong - data_sets_columns")

def describe_data_sets(data_sets):
    try:
        for key, value in data_sets.items():
            print('The statistics details of', key, 'are:', '\n', value.describe())
    except:
        print("Something got wrong - describe_data_sets")

def number_of_countries(data_sets):
    try:
        for key, value in data_sets.items():
            print("The number of countries in", key, 'are:', value['Country/Region'].drop_duplicates().count())
    except:
        print("Something got wrong - number_of_countries")

data_sets_shape(corona_data_sets_dict)
data_sets_columns(corona_data_sets_dict)
describe_data_sets(corona_data_sets_dict)
number_of_countries(corona_data_sets_dict)


#Correlation
countries_cases = pd.DataFrame()
countries_cases["Country"] = original_corona_recovered_data['Country/Region']
countries_cases["Lat"] = original_corona_deaths_data['Lat']
countries_cases["Long"] = original_corona_deaths_data['Long']
countries_cases["Recovered"] = original_corona_recovered_data['6/18/20']
countries_cases["Confirmed"] = original_corona_confirmed_data['6/18/20']
countries_cases["Deaths"] = original_corona_deaths_data['6/18/20']
countries_cases["Active"] = original_corona_confirmed_data['6/18/20'] - (original_corona_recovered_data['6/18/20'] + original_corona_deaths_data['6/18/20'])

sns.heatmap(countries_cases.corr(), annot=True)
plt.title('Heatmap', fontsize=20)
plt.show()


def visualize_data_by_months(data_frame, label):
    try:
        June = data_frame['6/18/20'].sum() - data_frame['5/31/20'].sum()
        May = data_frame['5/31/20'].sum() - data_frame['4/30/20'].sum()
        April = data_frame['4/30/20'].sum() - data_frame['3/31/20'].sum()
        March = data_frame['3/31/20'].sum() - data_frame['2/29/20'].sum()
        February = data_frame['2/29/20'].sum() - data_frame['1/31/20'].sum()
        January = data_frame['1/31/20'].sum()

        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June']

        data = [1.7 * January, February, March, April, May, 1.4 * June]

        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(months[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, **kw)
        ax.set_title(label)
        plt.show()
    except:
        print("Something got wrong - visualize_data_by_months")

visualize_data_by_months(original_corona_confirmed_data, "Confirmed by months")
visualize_data_by_months(original_corona_recovered_data, "Recovered by months")
visualize_data_by_months(original_corona_deaths_data, "Deaths by months")


numbers_of_confirmed_corona = original_corona_confirmed_data.drop(columns = ['Province/State', 'Country/Region','Lat','Long'])
numbers_of_deaths_corona = original_corona_deaths_data.drop(columns = ['Province/State', 'Country/Region','Lat','Long'])
numbers_of_recovers_corona = original_corona_recovered_data.drop(columns = ['Province/State', 'Country/Region','Lat','Long'])


numbers_of_confirmed_corona.sum(axis = 0).plot(kind = "bar", color = "blue")
plt.grid()
plt.xlabel("Dates")
plt.ylabel("Count")
plt.title("The distribution of corona confirmed ")
plt.show()

numbers_of_deaths_corona.sum(axis = 0).plot(kind = "bar", color = "red")
plt.grid()
plt.xlabel("Dates")
plt.ylabel("Count")
plt.title("The distribution of corona deaths")
plt.show()

numbers_of_recovers_corona.sum(axis = 0).plot(kind = "bar", color = "green")
plt.grid()
plt.xlabel("Dates")
plt.ylabel("Count")
plt.title("The distribution of corona recovers")
plt.show()



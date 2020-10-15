import numpy as np
import pandas as pd
from preprocessing import corona_confirmed_non_cumulative, corona_recovered_non_cumulative, corona_deaths_non_cumulative
import matplotlib.pyplot as plt

def describe_data(data):
    try:
        return data.describe()
    except:
        print('Something got wrong - describe_data')

print(describe_data(corona_confirmed_non_cumulative))
print(describe_data(corona_recovered_non_cumulative))
print(describe_data(corona_deaths_non_cumulative))

def numbers_of_corona_by_dates(dataframe, label, color, y_label):
    try:
        numbers_of_corona = dataframe.drop(columns = ['Continent'])
        numbers_of_corona.sum(axis = 0).plot(kind = "bar", color = color)
        plt.grid()
        plt.xlabel("Dates")
        plt.ylabel(y_label)
        plt.title(label)
        plt.show()
        return numbers_of_corona
    except:
        print('Something got wrong - numbers_of_corona_by_dates')

numbers_of_confirmed_corona = numbers_of_corona_by_dates(corona_confirmed_non_cumulative, "The distribution of corona confirmed " ,'blue', "Millions")
numbers_of_recovered_corona = numbers_of_corona_by_dates(corona_recovered_non_cumulative, "The distribution of corona recovered ",'green', "Millions")
numbers_of_deaths_corona = numbers_of_corona_by_dates(corona_deaths_non_cumulative, "The distribution of corona deaths ",'red', "Count")

def data_for_each_continent(data, label, label_for_ratio):
    try:
        Asia = data[(data['Continent'] == "Asia")].sum(axis=1).sum()
        Europe = data[(data['Continent'] == "Europe")].sum(axis=1).sum()
        Africa = data[(data['Continent'] == "Africa")].sum(axis=1).sum()
        North_America = data[(data['Continent'] == "North America")].sum(axis=1).sum()
        South_America = data[(data['Continent'] == "South America")].sum(axis=1).sum()
        Oceania = data[(data['Continent'] == "Oceania")].sum(axis=1).sum()

        print("Asia = " +  str(Asia))
        print("Europe = " +  str(Europe))
        print("Africa = " +  str(Africa))
        print("North_America = " +  str(North_America))
        print("South_America = " +  str(South_America))
        print("Oceania = " +  str(Oceania))

        Continent = ['Asia', 'Europe', 'Africa', 'North_America', 'South_America', 'Oceania']
        slices = [Asia, Europe, Africa, North_America, South_America, Oceania]
        colors = ['r', 'y', 'g', 'b','purple', 'brown']
        plt.pie(slices, labels= Continent, colors=colors, startangle=90, shadow=True, explode=(0, 0.1, 0, 0, 0, 0),radius=1.4, autopct='%1.1f%%')
        plt.legend()
        plt.title(label)
        plt.show()

        print(data['Continent'].value_counts())

        Continent = ['Asia', 'Europe', 'Africa', 'North_America', 'South_America', 'Oceania']
        slices = [Asia/78, Europe/72, Africa/57, North_America/36, South_America/12, Oceania/11]
        colors = ['r', 'y', 'g', 'b', 'purple', 'brown']
        plt.pie(slices, labels=Continent, colors=colors, startangle=90, shadow=True, explode=(0, 0, 0, 0, 0.1, 0),
                radius=1.4, autopct='%1.1f%%')
        plt.legend()
        plt.title(label_for_ratio)
        plt.show()
    except:
        print('Something got wrong - data_for_each_continent')

data_for_each_continent(corona_confirmed_non_cumulative, "Confirmed by continent", "Confirmed by division to countries in each continent")
data_for_each_continent(corona_recovered_non_cumulative, "Recovered by continent", "Recovered by division to countries in each continent")
data_for_each_continent(corona_deaths_non_cumulative, "Deaths by continent", "Deaths by division to countries in each continent")

#Corona_plots_in_each_continent
Continent_names = ('Africa','Asia','Europe','North America', 'Ocieania','South America')
y_pos = np.arange(len(Continent_names))

# corona_confirms_in_each_continent
def corona_in_each_continent(dataframe, label, color, y_label):
    try:
        corona_continent_dict = {}
        continent_group = dataframe.groupby("Continent")
        for name, group in continent_group:
            corona_continent_dict[name] = group.loc[:, group.columns != 'Continent'].sum().sum()
        continent_data_for_plot = pd.DataFrame(corona_continent_dict,index=[0])
        continent_data_for_plot.sum().plot(kind = 'bar', color = color)
        plt.xticks(y_pos, Continent_names, rotation = 0)
        plt.xlabel('Continents')
        plt.ylabel(y_label)
        plt.title(label)
        plt.grid()
        for x, y in zip([0, 1, 2, 3, 4, 5], continent_data_for_plot.sum()):
            plt.annotate('{}'.format(int(y)),
                         xy=(x, y),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')
        plt.show()
    except:
        print('Something got wrong - corona_in_each_continent')

corona_in_each_continent(corona_confirmed_non_cumulative, 'Numbers of corona confirms in each continent' ,'blue', "Millions")
corona_in_each_continent(corona_recovered_non_cumulative, 'Numbers of corona recovered in each continent','green', "Millions")
corona_in_each_continent(corona_deaths_non_cumulative, 'Numbers of corona deaths in each continent','red', "Count")

#plots_by_months
def plots_by_months(dataframe, label, color, y_label):
    try:
        month_data = pd.DatetimeIndex(dataframe.columns).month
        dataframe.columns = month_data
        corona_by_month = dataframe.groupby(dataframe.columns, axis = 1).sum()
        corona_by_month.sum().plot(kind = 'bar', color = color)
        plt.grid()
        plt.xticks(rotation=0)
        plt.xlabel("Months")
        plt.ylabel(y_label)
        plt.title(label)
        for x, y in zip([0, 1, 2, 3, 4, 5], corona_by_month.sum()):
            plt.annotate('{}'.format(int(y)),
                         xy=(x, y),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')
        plt.show()
    except:
        print('Something got wrong - plots_by_months')

plots_by_months(numbers_of_confirmed_corona, "Numbers of corona confirmed in each month", 'blue', "Millions")
plots_by_months(numbers_of_recovered_corona, "Numbers of corona deaths in each month", 'red', "Count")
plots_by_months(numbers_of_deaths_corona, "Numbers of corona recovered in each month", 'green', "Millions")


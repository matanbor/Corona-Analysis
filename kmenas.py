from preprocessing import corona_confirmed_for_unsupervised, corona_deaths_for_unsupervised, corona_recovered_for_unsupervised
from preprocessing import corona_confirmed_non_cumulative, corona_deaths_non_cumulative, corona_recovered_non_cumulative
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import numpy as np

def number_of_clusters(data_frame):
    try:
        sum_squared = []
        silhouette = []
        for i in range(2, 11):
            kmeans = KMeans(n_clusters=i, init='k-means++')
            kmeans.fit(data_frame)
            sum_squared.append(kmeans.inertia_)
            silhouette.append(silhouette_score(data_frame, kmeans.labels_))
        x1 = (range(2, 11))
        x2 = (range(2, 11))
        y1 = sum_squared
        y2 = silhouette
        plt.subplot(2, 1, 1)
        plt.plot(x1, y1)
        plt.title(r'Sum of Squred Error ${R_2}$', fontsize=15)
        plt.grid()
        plt.ylabel(r'${R_2}$')
        plt.subplot(2, 1, 2)
        plt.plot(x2, y2)
        plt.title('Silhouette', fontsize=15)
        plt.xlabel('No. of Clusters')
        plt.ylabel('Silhouette')
        plt.grid()
        plt.show()
    except:
        print("Something got wrong - number_of_clusters")

def create_kmeans_calssifier(k):
    try:
        return KMeans(n_clusters=k, init='k-means++')
    except:
        print("Something got wrong - create_kmeans_calssifier")

def clusters_information(data_frame):
    try:
        clusters = data_frame.groupby("label")
        for name, group in clusters:
            print(name)
            print(group)
            print(data_frame[data_frame["label"] == name].describe())
    except:
        print("Something got wrong - clusters_information")

#corona_confirm
number_of_clusters(corona_confirmed_for_unsupervised)
kmeans = create_kmeans_calssifier(3)
kmeans.fit(corona_confirmed_for_unsupervised)
print(silhouette_score(corona_confirmed_for_unsupervised, kmeans.labels_))
corona_confirmed_for_unsupervised["label"] = pd.Series(kmeans.labels_)
clusters_information(corona_confirmed_for_unsupervised)

#confirmed_sum_plot_for_each_cluster
corona_confirmed_dict_for_unsupervised = {}
corona_confirmed_dict_for_unsupervised['USA'] = corona_confirmed_non_cumulative[(corona_confirmed_non_cumulative.index == 225)].sum(axis=1, numeric_only=True).sum()
corona_confirmed_dict_for_unsupervised['Brazil, India, Russia'] = corona_confirmed_non_cumulative[(corona_confirmed_non_cumulative.index == 28) | (corona_confirmed_non_cumulative.index == 131) | (corona_confirmed_non_cumulative.index == 187)].sum(axis=1,numeric_only=True).sum()
corona_confirmed_dict_for_unsupervised['The rest of the world'] = corona_confirmed_non_cumulative[(corona_confirmed_non_cumulative.index != 225) & (corona_confirmed_non_cumulative.index != 28) & (corona_confirmed_non_cumulative.index != 131) & (corona_confirmed_non_cumulative.index != 187)].sum(axis=1,numeric_only=True).sum()
corona_confirmed_data_frame_for_plot= pd.DataFrame(corona_confirmed_dict_for_unsupervised, index=[0])
Clusters_names = ('USA', 'Brazil, India, Russia', 'The rest of the world')
y_pos = np.arange(len(Clusters_names))
corona_confirmed_data_frame_for_plot.sum().plot(kind = 'bar', color='blue')
plt.xticks(y_pos, Clusters_names, rotation=0,color='orange')
plt.yticks(color='orange')
plt.grid()
plt.xlabel('Clusters')
plt.ylabel('Numbers of corona confirmed')
plt.title('Sum of corona confirmed in each cluster in millions')
plt.show()


#corona_deaths
number_of_clusters(corona_deaths_for_unsupervised)
kmeans = create_kmeans_calssifier(4)
kmeans.fit(corona_deaths_for_unsupervised)
print(silhouette_score(corona_deaths_for_unsupervised, kmeans.labels_))
corona_deaths_for_unsupervised["label"] = pd.Series(kmeans.labels_)
clusters_information(corona_deaths_for_unsupervised)

#corona_deaths_plot
corona_europe_deaths_dict = {}
corona_europe_deaths_dict['France','Italy','Spain','UK'] = corona_deaths_non_cumulative[corona_deaths_non_cumulative['Continent'] == 'Europe'].sum(axis=1, numeric_only=True).nlargest(4).sum()
corona_europe_deaths_dict['The rest of europe'] = corona_deaths_non_cumulative[(corona_deaths_non_cumulative['Continent'] == 'Europe')
                                   & (corona_deaths_non_cumulative.index != 116)
                                   & (corona_deaths_non_cumulative.index != 137)
                                   & (corona_deaths_non_cumulative.index != 201)
                                   & (corona_deaths_non_cumulative.index != 223)].sum(axis=1, numeric_only=True).sum()
corona_europe_deaths_data_frame_for_plot = pd.DataFrame(corona_europe_deaths_dict, index=[0])
bar_name = ('France,Italy,Spain,UK','The rest of europe')
y_pos = np.arange(len(bar_name))
corona_europe_deaths_data_frame_for_plot.sum().plot(kind = 'bar', color='red')
plt.xticks(y_pos, bar_name, rotation=0, color='purple')
plt.yticks(color='purple')
plt.grid()
plt.xlabel('Europe countries')
plt.ylabel('Numbers of corona deaths')
plt.title('Sum of corona deaths in europe')
plt.show()

#corona_recoverd
number_of_clusters(corona_recovered_for_unsupervised)
kmeans = create_kmeans_calssifier(4)
kmeans.fit(corona_recovered_for_unsupervised)
print(silhouette_score(corona_recovered_for_unsupervised, kmeans.labels_))

corona_recovered_for_unsupervised["label"] = pd.Series(kmeans.labels_)
clusters_information(corona_recovered_for_unsupervised)

#corona_recoverd_plot
corona_recovered_dict = {}
corona_recovered_dict["USA"] = corona_recovered_non_cumulative[corona_recovered_non_cumulative.index == 225].sum(axis=1, numeric_only=True).sum()
corona_recovered_dict["Brazil"] = corona_recovered_non_cumulative[corona_recovered_non_cumulative.index == 29].sum(axis=1, numeric_only=True).sum()
corona_recovered_dict["Chile, India, Russia"] = corona_recovered_non_cumulative[(corona_recovered_non_cumulative.index == 39)
                                                | (corona_recovered_non_cumulative.index == 184)
                                                | (corona_recovered_non_cumulative.index == 125)].sum(axis=1, numeric_only=True).sum()
corona_recovered_dict["The rest of the world"] = corona_recovered_non_cumulative[(corona_recovered_non_cumulative.index != 225)
                                                & (corona_recovered_non_cumulative.index != 29)
                                                & (corona_recovered_non_cumulative.index != 39)
                                                & (corona_recovered_non_cumulative.index != 184)
                                                & (corona_recovered_non_cumulative.index != 125)].sum(axis=1, numeric_only=True).sum()
corona_recovered_data_frame_for_plot = pd.DataFrame(corona_recovered_dict, index=[0])
labels = 'USA', 'Brazil', 'Chile, India, Russia', 'The rest of the world'
sizes = [14.41, 12.86, 16.95, 55.78]
explode = (0, 0, 0, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("Corona recovered around the world")
plt.show()

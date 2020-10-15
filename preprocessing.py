import pandas as pd
from corona_data_sets import original_corona_recovered_data, original_corona_deaths_data, original_corona_confirmed_data
import pycountry_convert as pc
from sklearn import preprocessing


def pre_processing(original_data, supervised_or_unsupervised):
    try:
        pd.options.mode.chained_assignment = None

        def remove_columns(data_frame, col_name):
            try:
                columns = list(data_frame.columns)
                include_columns = [x for x in columns if x not in col_name]
                new_data_frame = data_frame[include_columns]
                return new_data_frame
            except:
                print('Something got wrong - remove_columns')

        name = original_data.isnull().sum().where(lambda x: x > 100).dropna().keys().to_list()
        original_data = remove_columns(original_data, name)

        def non_cumulative_data(data_frame):
            try:
                non_cumulative = data_frame.diff(axis=1)
                non_cumulative['1/22/20'] = data_frame['1/22/20']
                non_cumulative['Country/Region'] = data_frame['Country/Region']
                return non_cumulative
            except:
                print('Something got wrong - non_cumulative_data')

        data_frame_non_cumulative = non_cumulative_data(original_data)

        def country_to_continent(country_name):
            try:
                country_alpha2 = pc.country_name_to_country_alpha2(country_name)
                country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
                country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
                return country_continent_name
            except:
                return None

        def get_exceptional_country(country_name):
            try:
                if country_name in ['Congo (Kinshasa)', 'Congo (Brazzaville)', "Cote d'Ivoire", 'Timor-Leste', 'MS Zaandam',
                                    'Western Sahara']:
                    country_continent_name = 'Africa'
                elif country_name == 'Diamond Princess' or country_name == 'Holy See' or country_name == 'Kosovo':
                    country_continent_name = 'Europe'
                elif country_name == 'Korea, South' or country_name == 'Taiwan*' or country_name == 'West Bank and Gaza' or country_name == 'Burma':
                    country_continent_name = 'Asia'
                elif country_name == 'US':
                    country_continent_name = 'North America'
                return country_continent_name
            except:
                print("Something got wrong -get_exceptional_country ")

        # adding_continent_to_confirm
        data_frame_non_cumulative['Continent'] = None
        for i in data_frame_non_cumulative.index:
            if country_to_continent(data_frame_non_cumulative['Country/Region'][i]) is None:
                data_frame_non_cumulative['Continent'][i] = get_exceptional_country(data_frame_non_cumulative['Country/Region'][i])
            else:
                data_frame_non_cumulative['Continent'][i] = country_to_continent(data_frame_non_cumulative['Country/Region'][i])

        data_frame_non_cumulative = remove_columns(data_frame_non_cumulative, 'Country/Region')
        data_frame_non_cumulative = remove_columns(data_frame_non_cumulative, 'Lat')
        data_frame_non_cumulative = remove_columns(data_frame_non_cumulative, 'Long')

        if supervised_or_unsupervised == 'supervised':
            data_frame_for_supervised = data_frame_non_cumulative

            def encoders(data_frame):
                try:
                    encoders = {
                     'Continent': preprocessing.LabelEncoder()
                     }
                    data_frame['Continent'] = encoders['Continent'].fit_transform(data_frame['Continent'].astype(str))
                except:
                    print('Something got wrong - encoders')

            encoders(data_frame_for_supervised)
            return data_frame_for_supervised

        if supervised_or_unsupervised == 'unsupervised':
            data_frame_for_unsupervised = data_frame_non_cumulative

            def get_dummies(data_frame):
                try:
                    data_frame = pd.get_dummies(data_frame)
                    return data_frame
                except:
                    print('Something got wrong - get_dummies')

            data_frame_for_unsupervised = get_dummies(data_frame_for_unsupervised)
            return data_frame_for_unsupervised
        return data_frame_non_cumulative
    except:
        print("Something got wrong - pre_processing")


corona_confirmed_for_supervised = pre_processing(original_corona_confirmed_data, 'supervised')
corona_recovered_for_supervised = pre_processing(original_corona_recovered_data, 'supervised')
corona_deaths_for_supervised = pre_processing(original_corona_deaths_data, 'supervised')

corona_confirmed_for_unsupervised = pre_processing(original_corona_confirmed_data, 'unsupervised')
corona_recovered_for_unsupervised = pre_processing(original_corona_recovered_data, 'unsupervised')
corona_deaths_for_unsupervised = pre_processing(original_corona_deaths_data, 'unsupervised')

corona_confirmed_non_cumulative = pre_processing(original_corona_confirmed_data, 'for analysis')
corona_recovered_non_cumulative = pre_processing(original_corona_recovered_data, 'for analysis')
corona_deaths_non_cumulative = pre_processing(original_corona_deaths_data, 'for analysis')


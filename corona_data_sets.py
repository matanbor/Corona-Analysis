import pandas as pd

def read_data(csv_file):
    try:
        return pd.read_csv(csv_file)
    except:
        print("The file is not found")
        return None


original_corona_confirmed_data = read_data('corona_confirmed_global.csv')
original_corona_deaths_data = read_data('corona_deaths_global.csv')
original_corona_recovered_data = read_data('corona_recovered_global.csv')



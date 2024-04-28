#!/usr/bin/env python
# coding: utf-8


import pandas as pd
class Transformer :

    def __init__(self):
        self.unemployment_df = None
        self.crime_df = None

    def transform_data_delete_null(self):
        unemployment_pre = pd.read_csv(r"D:\\Github\\made-ws23\\project\\data\\API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_6299762.csv", skiprows=3)
        crime_pre = pd.read_csv(r"D:\\Github\\made-ws23\\project\\data\\API_VC.IHR.PSRC.P5_DS2_en_csv_v2_6299884.csv", skiprows=3)

        # Unemployment data pre-processing

        # Finding columns with all null values
        unemployment_pre.columns[unemployment_pre.isna().all()].tolist

        # Dropping columns with Null values
        unemployment_pre.drop(columns=['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
                                       '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
                                       '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
                                       '1987', '1988', '1989', '1990', '2022', 'Unnamed: 67'], inplace=True)

        # Dropping columns with no significant meaning
        unemployment_pre.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'], inplace=True)

        # Finding rows with all null values
        unemployment_pre[unemployment_pre.loc[:, '1991':].isna().all(axis=1)].index

        # Dropping rows with all null values
        unemployment_pre.drop(index=[0, 6, 11, 12, 27, 51, 52, 57, 78, 79, 84, 90, 91,
                                     108, 110, 124, 125, 137, 147, 149, 155, 164, 179, 188, 212, 225,
                                     226, 228, 245, 255, 261], inplace=True)


        # Crime data pre-processing


        # Finding columns with all null values
        crime_pre.columns[crime_pre.isna().all()].tolist


        # Dropping columns with Null values
        crime_pre.drop(columns=['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
                                '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
                                '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
                                '1987', '1988', '1989', '1990', '2022', 'Unnamed: 67'], inplace=True)


        # Dropping columns with no significant meaning
        crime_pre.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'], inplace=True)


        # Finding countries where total null values are greater than 5 starting from 1990 to 2021
        countries_with_nulls = crime_pre[crime_pre.loc[:, '1991':].isna().sum(axis=1) > 5]

        # Drop the countries having NAN values greater than 6
        crime_pre_cleaned = crime_pre.drop(countries_with_nulls[countries_with_nulls.sum(axis=1) > 6].index)

        # Fill NaN values in columns with their mean
        crime_pre_cleaned_filled = crime_pre_cleaned.fillna(crime_pre_cleaned.mean())
        unemployment_pre_cleaned = unemployment_pre.fillna(unemployment_pre.mean())

        return (crime_pre_cleaned_filled, unemployment_pre_cleaned)

    def sync_both_data(self):
        self.crime_df, self.unemployment_df = self.transform_data_delete_null()
        # removing extra countries from unemployment data to sync with crime data
        remaining_countries = self.crime_df['Country Name'].tolist()

        # Filter the rows for the remaining countries
        unemployment_remaining_countries = self.unemployment_df[self.unemployment_df['Country Name'].isin(remaining_countries)]

        u = unemployment_remaining_countries.set_index('Country Name').T.columns.tolist()
        c = self.crime_df.set_index('Country Name').T.columns.tolist()

        temp = [x for x in c if x not in u]

        crime_skim = self.crime_df.set_index('Country Name').T
        # removing temp list
        crime_skim.drop(
            columns=['Bermuda', 'Cayman Islands', 'Faroe Islands', 'Micronesia, Fed. Sts.', 'Gibraltar',
                     'Not classified',
                     'Liechtenstein', 'Monaco', 'Northern Mariana Islands', 'Nauru', 'San Marino',
                     'Sint Maarten (Dutch part)'], inplace=True)

    # transformed crime data
        crime_final = crime_skim.T.reset_index()

    # transformed unemployment data
        unemployment_final = unemployment_remaining_countries.reset_index(drop=True)

        return crime_final, unemployment_final

# Getter methods to retrieve the transformed dataframes

    def get_unemployment_data_not_null(self):
        return self.transform_data_delete_null()[1]

    def get_crime_data_not_null(self):
        return self.transform_data_delete_null()[0]

    def get_unemployment_data(self):
        return self.sync_both_data()[1]

    def get_crime_data(self):
        return self.sync_both_data()[0]

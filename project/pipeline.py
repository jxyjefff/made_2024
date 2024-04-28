from ETL import extract, transform, load
import os
import warnings

def main():
    # Define API URLs for data extraction
    unemployment_api_url = "https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv"
    crime_api_url = "https://api.worldbank.org/v2/en/indicator/VC.IHR.PSRC.P5?downloadformat=csv"

    # Set the download path
    download_path = "D:\\Github\\made-ws23\\project\\data"

    # Initialize Extractor and extract data
    extractor = extract.Extractor()

    extractor.extract_unemployment_data(unemployment_api_url, download_path)
    extractor.extract_crime_data(crime_api_url, download_path)

    print("Data extraction completed.")

    # Initialize Transformer and transform data
    transformer = transform.Transformer()
    transformer.transform_data_delete_null()
    transformer.sync_both_data()

    # Get transformed dataframes
    transformed_unemployment_data = transformer.get_unemployment_data()
    transformed_crime_data = transformer.get_crime_data()

    print("Data transformation completed.")

    loader = load.Loader()
    # Define output paths
    unemployment_output_path = os.path.join(download_path, 'unemployment.csv')
    crime_output_path = os.path.join(download_path, 'crime.csv')

    # Save transformed dataframes to CSV
    loader.load_data_and_save(transformed_unemployment_data, unemployment_output_path)
    loader.load_data_and_save(transformed_crime_data, crime_output_path)

    print("Data loading and saving completed.")

    return True


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()

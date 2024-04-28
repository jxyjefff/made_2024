import requests
import zipfile
import os

class Extractor :
    def __init__(self) -> None:
        pass
    def extract_unemployment_data(self, api_url, download_path):
        response = requests.get(api_url)
        if response.headers['Content-Type'] == 'application/zip':
            zip_file_path = os.path.join(download_path, 'unemployment_data.zip')

            with open(zip_file_path, 'wb') as zip_file:
                zip_file.write(response.content)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(download_path)

            os.remove(zip_file_path)
        else:
            print("Error: The downloaded file is not a zip file.")
            return False

        return True

    def extract_crime_data(self, api_url, download_path):
        response = requests.get(api_url)

        if response.headers['Content-Type'] == 'application/zip':
            zip_file_path = os.path.join(download_path, 'crime_data.zip')

            with open(zip_file_path, 'wb') as zip_file:
                zip_file.write(response.content)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(download_path)

            os.remove(zip_file_path)
        else:
            print("Error: The downloaded file is not a zip file.")
            return False

        return True
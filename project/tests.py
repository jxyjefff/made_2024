import unittest
import warnings
from ETL import extract, transform,load
from pipeline import main

class TestExtractor(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.api_url_unemployment = "https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.ZS?downloadformat=csv"
        self.api_url_crime = "https://api.worldbank.org/v2/en/indicator/VC.IHR.PSRC.P5?downloadformat=csv"
        self.download_path = "D:\\Github\\made-ws23\\project\\data"

    def test_extract_unemployment_data(self):
        result = extract.Extractor.extract_unemployment_data(self, self.api_url_unemployment, self.download_path)
        self.assertTrue(result, "Fail")
    def test_extract_crime_data(self):
        result = extract.Extractor.extract_crime_data(self, self.api_url_crime, self.download_path)
        self.assertTrue(result, "Fail")

class TestTransformer(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.t = transform.Transformer()

    def test_null_values(self):
        # testing null values
        self.t.transform_data_delete_null()
        self.assertFalse(self.t.get_unemployment_data_not_null().isnull().values.any())
        self.assertFalse(self.t.get_crime_data_not_null().isnull().values.any())
    def test_transform_data(self):
        self.t.sync_both_data()
        # testing columns of both dataframes are equal
        self.assertTrue(self.t.get_unemployment_data().columns.all() == self.t.get_crime_data().columns.all(), "Columns of both dataframes are not equal")
        # testing rows of both dataframes are equal
        self.assertTrue(self.t.get_unemployment_data().T.columns.all() == self.t.get_crime_data().T.columns.all(), "Rows of both dataframes are not equal")

class TestLoader(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.t = transform.Transformer()
        self.t.transform_data_delete_null()
        self.t.sync_both_data()
        self.output_file_u = "D:/Github/made-ws23/project/data/unemployment.csv"
        self.output_file_c = "D:/Github/made-ws23/project/data/crime.csv"
    def test_load_data_and_save(self):
        resultu = load.Loader().load_data_and_save(self.t.get_unemployment_data(), self.output_file_u)
        self.assertTrue(resultu, "Fail")
        resultc = load.Loader().load_data_and_save(self.t.get_crime_data(), self.output_file_c)
        self.assertTrue(resultc, "Fail")

class TestPipeline(unittest.TestCase):
    def test_main(self):
        m = main()
        self.assertTrue(m, "Everything is not fine")

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    unittest.main()

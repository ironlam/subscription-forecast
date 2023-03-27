import os
import unittest
from forecast import read_data, prepare_data, forecast_subscriptions
import pandas as pd


class TestForecast(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join('dataset', 'subscriptions.csv')

    def test_read_data(self):
        data = read_data(self.file_path)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn('id', data.columns)
        self.assertIn('source', data.columns)
        self.assertIn('subscription_level', data.columns)
        self.assertIn('created_at', data.columns)

    def test_prepare_data(self):
        data = read_data(self.file_path)
        prepared_data = prepare_data(data, 'Android')
        self.assertIsInstance(prepared_data, pd.DataFrame)
        self.assertIn('ds', prepared_data.columns)
        self.assertIn('subscription_level', prepared_data.columns)
        self.assertIn('y', prepared_data.columns)

    def test_forecast_subscriptions(self):
        data = read_data(self.file_path)
        prepared_data = prepare_data(data, 'Android')
        future, forecast = forecast_subscriptions(prepared_data, 180)
        self.assertIsInstance(future, pd.DataFrame)
        self.assertIsInstance(forecast, pd.DataFrame)
        self.assertIn('ds', future.columns)
        self.assertIn('ds', forecast.columns)
        self.assertIn('yhat', forecast.columns)
        self.assertIn('yhat_lower', forecast.columns)
        self.assertIn('yhat_upper', forecast.columns)


if __name__ == '__main__':
    unittest.main()

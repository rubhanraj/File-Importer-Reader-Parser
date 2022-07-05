

import unittest
import pandas as pd
import os.path

from quotes_group_reader import QuotesGroupReader


class TestQuotesGroupReader(unittest.TestCase):

    def setUp(self):
        self.quotes_group_reader = QuotesGroupReader(
                "/Users/rubhanxavierraj/Downloads/Sample Data/Storage",
                "/Users/rubhanxavierraj/Downloads/Sample Data/Output",
                "31/12/2019",
                "Cap Vols"
                )
        
    def test_output_json(self):

        path_of_the_current_directory = os.path.abspath(os.path.dirname(__file__))
        quote_table = pd.read_csv(os.path.join(path_of_the_current_directory, "latest_quotes_table_test.csv"))
        
        output_json = {
                        'GroupName': 'Cap Vols',
                        'AsOfDate': '31/12/2019',
                        'Quotes': [
                                     {
                                       "GroupName": "Cap Vols",
                                       "ProductId": "EUCF101 Curncy",
                                       "AsOfDate": "31/11/2019",
                                       "Value": 2.678727415
                                     },
                                     {
                                       "GroupName": "Cap Vols",
                                       "ProductId": "EUCF1010 Curncy",
                                       "AsOfDate": "31/11/2019",
                                       "Value": 18478.8126
                                     }
                                ]
                        }
        
        self.assertEqual(self.quotes_group_reader.get_output_json(quote_table), output_json, "Should be equal")

    def test_csvs_list(self):
        list_of_csvs = self.quotes_group_reader.get_list_of_csvs()
        check_list = [item.endswith("csv") for item in list_of_csvs]
        
        self.assertEqual(all(check_list), True, "Should be equal")

if __name__ == '__main__':
    unittest.main()
    




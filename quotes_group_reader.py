#!/usr/bin/env python3
#!/usr/bin/env python
import os
import sys
import json
import argparse
import shutil
import pandas as pd

print('------------------------------')
print('Quotes Group Reader Running...')
print('------------------------------')


class ArgumentsParser:
    def __init__(self):
        # Adding argument parser arguments
        self.parser = argparse.ArgumentParser(
                                                prog = 'QuotesGroupReader',
                                                usage = '\n%(prog)s [options] --storage_dir <path to storage directory> --output_dir <path to input directory> --date <date of the quote> --group <name of the quote group>\n',
                                                description = 'It reads all csv files from the input directory and stores data to storage directory',
                                                epilog=' ----------\n-- Quotes Importer --\n----------'
                                        )
        
        
        self.parser.add_argument(
                                   '--storage_dir',
                                   help = 'path to the directory to store the CSV files',
                                   type = str,
                                   required = True
                               )
        
        
        self.parser.add_argument(
                                   '--output_dir',
                                   help = 'path to the directory to store the output json',
                                   type = str,
                                   required = True
                               )
        
        
        self.parser.add_argument(
                                   '--date',
                                   help = 'date of the quote',
                                   type = str,
                                   required = True
                               )
        
        
        self.parser.add_argument(
                                   '--group',
                                   help = 'name of the quote group',
                                   type = str,
                                   required = True
                       )
        
    def read_arguments(self):
        # Extracting the arguments
        args = self.parser.parse_args()
        
        # Reading arguments
        storage = args.storage_dir
        output = args.output_dir
        date = args.date
        group = args.group
        return storage, output, date, group

class QuotesGroupReader:
    #  Constructor initialising the arguments
    def __init__(self, storage, output, date, group):
        self.storage = storage
        self.output = output
        self.date = date
        self.group = group
    
    # Method to get date components    
    def get_date_components(self, date):
        date_components_list = date.split('/')
        day = date_components_list[0]
        month = date_components_list[1]
        year = date_components_list[2]
        return day, month, year
    
    # Method to get the list of CSVs in the folder
    def get_list_of_csvs(self):        
        files_list = os.listdir(self.storage)
        csv_files_list = [ self.storage + '/' + filename for filename in files_list if filename.endswith('.csv') ]
        return csv_files_list
    
    # Method to check if the output file and the latest quote table exists 
    def check_if_file_exists_if_csv_files_list_is_empty(self, csv_files_list):  
        print('Checking if output file exists if csv files list is empty...')
        day, month, year = self.get_date_components(self.date)
        if csv_files_list == []:
            if os.path.isfile(self.output + '/' + self.group + '-' + year + '-' + month + '-' + day + '.json'):
                print("No files to process. Output file already exists")
                sys.exit()
            else:
                print("Import files to read quotes")
                sys.exit()
    
    # Method to create a directory if it doesn't exist
    def create_directory(self, location):
        if not os.path.exists(location):
            os.makedirs(location)

    # Method to merge the CSVs and return a data frame
    def get_full_dataframe_after_read(self, csv_files_list):
        return pd.concat(map(pd.read_csv, csv_files_list), ignore_index=True)

    # Method to get unique dates 
    def get_unique_dates(self, full_dataframe_after_read):
        return list(full_dataframe_after_read['AsOfDate'].unique())

    # Method to get the latest quote table
    def get_latest_quote_table(self, unique_date):
        day, month, year = self.get_date_components(unique_date)
        if os.path.isfile(self.storage + '/' + year + '/' + month + '/' + day +  "/QuoteTable/latest_quotes_table.csv"):
            latest_quotes_table = pd.read_csv(self.storage + year + '/' + month + '/' + day +  "/QuoteTable/latest_quotes_table.csv")
        else:
            group_mapping = pd.read_csv("/Sample Data/GroupMapping.csv")
            latest_quotes_table = pd.DataFrame(columns=['GroupName', 'ProductId'])
            latest_quotes_table['GroupName'] = group_mapping['GroupName']
            latest_quotes_table['ProductId'] = group_mapping['ProductId']
        return latest_quotes_table

    # Method to create quote tables            
    def create_quote_tables(self, unique_date, latest_quotes_table, full_dataframe_after_read):
        day, month, year = self.get_date_components(unique_date)         
        full_dataframe_after_read_unique_date = full_dataframe_after_read[full_dataframe_after_read['AsOfDate'] == unique_date]
        full_dataframe_after_read_unique_date_with_max_quote_value = full_dataframe_after_read_unique_date.loc[full_dataframe_after_read_unique_date.groupby('ProductId')['Value'].idxmax()]
        latest_quotes_table_unique_date = pd.merge(latest_quotes_table, full_dataframe_after_read_unique_date_with_max_quote_value, on = 'ProductId', how = 'left')
        location_of_latest_quotes_table = self.storage + '/' + year + '/' + month + '/' + day + '/QuotesTable/' 
        self.create_directory(location_of_latest_quotes_table)
        latest_quotes_table_unique_date.to_csv(location_of_latest_quotes_table + 'latest_quotes_table.csv', sep=',', index=False)

    # Method to read quote table
    def read_quotes_table(self):
        day, month, year = self.get_date_components(self.date)
        latest_quotes_table_unique_date = pd.read_csv(self.storage + '/' + year + '/' + month + '/' + day +  "/QuotesTable/latest_quotes_table.csv")
        latest_quotes_table_filtered_unique_date_with_group_name = latest_quotes_table_unique_date[latest_quotes_table_unique_date['GroupName'] == self.group].drop('GroupName', axis = 1)
        return latest_quotes_table_filtered_unique_date_with_group_name

    # Method to create the output json
    def get_output_json(self, quotes_table):
        output_json = {
                        'GroupName': self.group,
                        'AsOfDate': self.date,
                        'Quotes': quotes_table.to_dict(orient="records")
                    }
        return output_json

    # Method to write the 
    def write_output_json(self, output_json):
        day, month, year = self.get_date_components(self.date)
        output_file_name = self.output + '/' + self.group + '-' + year + '-' + month + '-' + day + '.json'
        
        with open(output_file_name, 'w') as fp:
            json.dump(output_json, fp, indent=4)
            
    # Method to move processed files
    def move_read_files(self, csv_files_list):
        # Moving the files which are read to Read Files folder    
        for file_name in csv_files_list:
            shutil.move(os.path.join(self.storage, '/' , file_name), self.storage + '/ReadFiles/')


def main():
    
    print('Reading inputs...')
    arguments_parser = ArgumentsParser()
    storage, output, date, group = arguments_parser.read_arguments()    
    
    print('Initialising Quotes Group Reader...')
    quotes_group_reader = QuotesGroupReader(storage, output, date, group)
    day, month, year = quotes_group_reader.get_date_components(date)
    
    print("Gathering List of CSVs...")
    csv_files_list = quotes_group_reader.get_list_of_csvs()
    quotes_group_reader.check_if_file_exists_if_csv_files_list_is_empty(csv_files_list)
    
    print("Creating quote tables...")
    full_dataframe_after_read = quotes_group_reader. get_full_dataframe_after_read(csv_files_list)
    unique_dates = quotes_group_reader.get_unique_dates(full_dataframe_after_read)
    for unique_date in unique_dates:
        latest_quotes_table = quotes_group_reader.get_latest_quote_table(unique_date)
        quotes_group_reader.create_quote_tables(unique_date, latest_quotes_table, full_dataframe_after_read)

    print("Reading the Quote table corresponding to the input request...")
    quotes_table = quotes_group_reader.read_quotes_table()
    
    print("Preparing the output JSON...")
    output_json = quotes_group_reader.get_output_json(quotes_table)
    quotes_group_reader.write_output_json(output_json)
    
    print('Creating ReadFiles folder and moving read files to it...')
    quotes_group_reader.create_directory(storage +  "/ReadFiles/") 
    quotes_group_reader.move_read_files(csv_files_list)
    
    print("Quotes Group Read Completed...!")


if __name__ == '__main__':
    main()


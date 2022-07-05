#!/usr/bin/env python
import os
import argparse
import shutil

print('------------------------------')
print('Quotes Importer Running...')
print('------------------------------')


class ArgumentsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                                                prog = 'QuotesImporter',
                                                usage = '\n%(prog)s [options] --input_dir <path to input directory> --storage_dir <path to storage directory> \n',
                                                description = 'It reads all csv files from the input directory and stores data to storage directory',
                                                epilog=' ----------\n-- Quotes Importer --\n----------'
                                        )
        
        self.parser.add_argument(
                                   '--input_dir',
                                   help = 'Path to the directory which has the input CSV files',
                                   type = str,
                                   required = True
                               )
        
        self.parser.add_argument(
                                   '--storage_dir',
                                   help = 'Path to the directory to store the CSV files',
                                   type = str,
                                   required = True
                               )
        
    def read_arguments(self):
        # Extracting the arguments
        args = self.parser.parse_args()
        return args.input_dir, args.storage_dir

class ImportFiles:
    # Method to import files from source tot target directory
    def importing_files(self, source, target):
        files = os.listdir(source)
        # iterating over all the files in
        # the source directory
        for file_name in files:
            # copying the files to the
            # destination directory
            shutil.copy2(os.path.join(source, file_name), target)


def main():
    print('Reading inputs...')
    arguments_parser = ArgumentsParser()
    source, target = arguments_parser.read_arguments()
    
    print('Importing files...')
    import_files = ImportFiles()
    import_files.importing_files(source, target)
    
    print("Files successfully imported! ")

if __name__ == "__main__":
    main()
    
    
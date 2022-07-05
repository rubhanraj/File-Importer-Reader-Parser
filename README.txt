Installation:
————————

To start with, please install python 3.9 in your machine. You can download it form the following link:

https://www.python.org/downloads/release/python-390/

After this run the following command to create a virtual environment:

pip install virtualenv

Create a virtual environment by running the following command:

python -m venv <name_of_virtualenv>


Activate the virtual environment by running the following command (for MacOS):

source <name_of_virtualenv>/bin/activate

Once installed, install the requirements from the requirements.txt file by running:

pip install -r requirements.txt

Usage:
———————

After installing you can run the quotes_importer.py file by running the following command:

python quotes_importer.py —-input_dir <path_of_the_input_directory> —-storage_dir <path_of_the_storage_directory>

you can run the quotes_group_reader.py file by running the following command:


python quotes_group_reader.py —-storage_dir <path_of_the_storage_directory> —-output_dir <path_of_the_output_directory> --date <as_of_date> --group <group_name>

You can run the tests cases by running:

python -m unittest discover ./tests


Algorithm:
————————

Quotes Importer:
—————
- Quotes Importer uses the copy function of shutil package to copy the files from source to target folders.

Quotes Group Reader:
—————
- Quotes Group Reader reads the number of CSVs in the input folder.
- It combines all the CSVs and create a single data frame (In the future, batch processing can be enable for this process to handle large amounts of data)
- Based on the dates in the single data frame, for every date, the tool creates a folder structure and a “latest quotes table”. After every read, this table gets updated with the latest max quote value.
- After creating/updating the quotes table for every date, the tool reads the “latest_quote_table” that was requested in the output and converts it to a json and returns it.
- I there are no files to read in the storage directory, the algorithm looks for the “latest quote table” and return it directly.

Thank you!





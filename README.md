# nft-csv-project

## Description
This project is a simple script that creates json files from the data on a given nft csv file and generates a CHIP-0007 compatible json, calculates the SHA256 of the json file and appends it to each line of the given csv.

The script was created with python programming language and it is compatible with python 3.6 and above.

No external libraries are required.

## Usage
1. Clone the repository
2. Install python 3.6 or above if you don't have it already
3. move the csv file to the project directory. This is very important, the script will not work if the csv file is not in the same directory as the script.
4. run the script with the following command:
``` python3 main.py ``` for linux and mac
``` python main.py ``` for windows
5. The csv file will be updated with the SHA256 of the json files and created in the project directory
6. The CHIP-0007 compatible json file will be created in the `json files` directory

## Example
The example csv file is located in the example directory and it is called "example.csv".

The example json file is located in the example directory and it is called "example.json".
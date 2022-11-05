import csv
import json
import hashlib
import os

hasher = hashlib.sha256()

csv_file_name = ''
def check_file_exists() -> str:

    file_name = input('Enter the name of the CSV file: ')
    if os.path.exists(file_name) and file_name.endswith('.csv'):
        print(file_name)
        return file_name
    print("please enter a valid file name")
    check_file_exists()


json_file_path = 'json files'
csv_file_path = check_file_exists()
new_csv_file_path = "output.csv"


def format_attributes(attribs: str) -> list[dict[str, str]]:
    temp = attribs.split(';')
    formatted_attributes = []

    for attribute in temp:
        split_attribute = attribute.split(':')
        try:
            formatted_attributes.append({
                'trait_type': split_attribute[0],
                'value': split_attribute[1]
            })
        except IndexError:
            continue

    return formatted_attributes


data_list = []

with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        team_name = row['TEAM NAMES']
        series_number = row['Series Number']
        file_name = row['Filename']
        name = row['Name']
        description = row['Description']
        gender = row['Gender']
        attributes = row['Attributes']
        uuid = row['UUID']

        output = {
            "format": "CHIP-0007",
            "series_number": series_number,
            "file_name": file_name,
            "name": name,
            "description": description,
            "gender": gender,
            "attributes": format_attributes(attributes),
            "collection": {
                "name": "HNGi9",
                "id": uuid,
                "attributes": []
            },
            "uuid": uuid,
            "data": {
                "example_data": "example_data"
            }
        }

        # create and hash json file
        data_json = json.dumps(output, indent=4)
        hasher.update(data_json.encode('utf-8'))
        open(f'{json_file_path}/{name}.json', 'w').write(data_json)
        hashed_data = hasher.hexdigest()
        output["hash"] = hashed_data
        output["team_name"] = team_name
        output["attributes"] = attributes
        data_list.append(output)

# convert dict to csv
with open(new_csv_file_path, 'w') as csv_file:
    fieldnames = ['TEAM NAMES', 'Series Number',
                  'Filename', 'Name', 'Description',
                  'Gender', 'Attributes', 'UUID', 'HASH']

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for data in data_list:
        writer.writerow({
            'Series Number': data['series_number'],
            'Filename': data['file_name'],
            'Name': data['name'],
            'Description': data['description'],
            'Gender': data['gender'],
            'UUID': data['uuid'],
            'Attributes': data['attributes'],
            'HASH': data['hash']
        })

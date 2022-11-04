import csv
import json
import hashlib

hasher = hashlib.sha256()

csv_file_path = 'HNGi9 CSV FILE - Sheet1.csv'
json_file_path = 'json files'
new_csv_file_path = 'HNGi9CSV FILE-Sheet2.csv'


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

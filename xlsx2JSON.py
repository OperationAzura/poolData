import openpyxl
import json
from statistics import mean

def convert_xlsx_to_json(input_file, output_file):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook(input_file)

    # Select the first sheet
    sheet = workbook.active

    # Initialize an empty list to store rows
    rows = []

    # Iterate over all rows in the sheet
    for row in sheet.iter_rows(values_only=True):
        rows.append(row)

    # Get the header row
    header = rows[0]

    # Initialize an empty list to store dictionaries
    data = []

    # Keep track of seen timestamps
    seen_timestamps = set()

    # Iterate over the remaining rows
    for row in rows[1:]:
        # Check if "SALT(TDS)" value is non-zero or non-empty
        salt_value = float(row[header.index("SALT(TDS)")])
        ph_value = float(row[header.index("pH")])
        orp_value = float(row[header.index("ORP(mV)")])
        temperature_value = float(row[header.index("Temperature(\u00b0F)")])
        timestamp = row[header.index("Date")]

        if salt_value and salt_value > 1000 and ph_value and 4 < ph_value < 9 and salt_value < 5000:
            # Check if timestamp is already seen
            if timestamp not in seen_timestamps:
                # Create a dictionary for the first row in each time block
                row_data = {
                    "Date": timestamp,
                    "pH": round(ph_value, 2),
                    "SALT(TDS)": round(salt_value, 2),
                    "ORP(mV)": round(orp_value, 2),
                    "Temperature(\u00b0F)": round(temperature_value, 2)
                }

                # Append the dictionary to the data list
                data.append(row_data)

                # Add the timestamp to seen timestamps
                seen_timestamps.add(timestamp)

    # Convert the data to JSON
    json_data = json.dumps(data, indent=4)

    # Write the JSON string to a file
    with open(output_file, 'w') as f:
        f.write(json_data)

    print(f"Conversion complete. JSON data saved to {output_file}.")

# Specify the input Excel file and output JSON file paths
input_file = 'input.xlsx'
output_file = 'output.json'

# Call the conversion function
convert_xlsx_to_json(input_file, output_file)

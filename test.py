import csv

def clean_csv(input_file, output_file):
    data = []

    # Read the CSV file with UTF-8 encoding
    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    # Clean the data by replacing empty fields with "N/A"
    for row in data:
        for i in range(len(row)):
            if not row[i]:
                row[i] = "N/A"

    # Write the cleaned data to a new CSV file with text qualifier and UTF-8 encoding
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)


if __name__ == "__main__":
    input_csv_file = "data.csv"
    output_csv_file = "cleaned_file2.csv"

    clean_csv(input_csv_file, output_csv_file)

    print("CSV cleaning complete. Cleaned data saved to", output_csv_file)

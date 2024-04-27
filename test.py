import csv

input_file_path = 'E:\Scrapy\Restaurantscraper\Free_Proxy_List.csv'
output_file_path = 'Restaurantscraper/Free_Proxy_List.txt'

# Assuming IP is the first column and port is the eighth column in your detailed proxy list
ip_index = 0  # index of the IP address in the CSV
port_index = 7  # index of the port in the CSV

with open(input_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        for row in reader:
            if row:  # check if the row is not empty
                ip = row[ip_index].strip('"')  # Remove any extra quotes
                port = row[port_index].strip('"')  # Remove any extra quotes
                outfile.write(f"{ip}:{port}\n")

print("Conversion completed. Check", output_file_path)

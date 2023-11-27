import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient

# Set up your Data Lake Storage account credentials
account_name = "lab2dl"
account_key = "sv44h7iPnAhb229nllmkA4e9/nJWBSKe2bNOmI6XDaJ4nyE3KmsbK4mwE2gYt3hfN3lSsAblSLuk+AStwpTadw=="
container_name_output = "output"

# Create a DataLakeServiceClient
service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=account_key)

# Create DataLakeFileSystemClient for input and output containers
file_system_client_output = service_client.get_file_system_client(container_name_output)

amazon = pd.read_csv("AMAZON.csv")
apple = pd.read_csv("APPLE.csv")
facebook = pd.read_csv("FACEBOOK.csv")
google = pd.read_csv("GOOGLE.csv")
microsoft = pd.read_csv("MICROSOFT.csv")
tesla = pd.read_csv("TESLA.csv")
zoom = pd.read_csv("ZOOM.csv")

df_list = [amazon, apple, facebook, google, microsoft, tesla, zoom]

# combining the dataframes to one df
combined_df = pd.concat(df_list, ignore_index=True)

combined_df = combined_df.rename(columns={"company_name": "stock_name"})

# Create a BytesIO object to simulate a file-like object from the DataFrame
combined_stock_data = combined_df.to_csv(index=False)

# Set up the DataLakeDirectoryClient for the output container and directory
directory_path = "/"  
directory_client_output = file_system_client_output.get_directory_client(directory_path)

# Upload the combined CSV file to the directory
file_name = "combined_stock_data.csv"
output_file_path = f"{file_name}"

try:
    with directory_client_output.create_file(file_name) as file:
        file.upload_data(combined_stock_data.encode(), overwrite=True)
    print(f"File '{output_file_path}' uploaded successfully.")
except Exception as e:
    print(f"Error uploading file '{output_file_path}': {e}")

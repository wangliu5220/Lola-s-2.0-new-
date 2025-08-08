# Downloads the images from the data and stores them in a folder with product UPC as name
# Later if this is deployed then it should download the images per request to some backend Database management system
# Also if this is used later on maybe change structure to class and not just random collection of functions 
import requests
import json
import os
import openpyxl
import pandas as pd


def read_xlsx_file(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def get_column_values(file_path, sheet_name, *column_names):
    """Get the values in a specific column or set of columns

    Args:
        df (pandas.DataFrame): The dataframe to get the column values from
        *column_names (str): The name or names of the columns to get the values from
        sheet_name (str): The name of the sheet to get the values from

    Returns:
        list or lists: The values in the specified columns
    """
    df = read_xlsx_file(file_path, sheet_name)
    return [df[column_name].tolist() for column_name in column_names]

def download_image(image_url):
    """_summary_

    Args:
        image_url (string): Urk link to image

    Returns:
        Not sure but I think its a byte value of some sort: if you save the return as a png or jpeg it should work, prob shouldv'e looked into this lol
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

def Sort_and_save_image(UPC, image_url, image_name):
    save_path = f'AI_Image_Scrapping/downloaded_images/{UPC}/{image_name}.png'
    save_dir = os.path.dirname(save_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image = download_image(image_url)

    with open(save_path, 'wb') as f:
        f.write(image.content)
        
def main():
    # for now it will get all the product names, UPC, and image urls as a list of lists (maybe tuples idk)
    # ex) [0][0] = name of first product, [1][0] = upc of first product, [2][0] = image url of first product... (first num is column, second is row)
    excel_file_path = 'AI_Image_Scrapping\Image_Data\mock_data_web_scraped.xlsx'
    sheet_name = 'Sheet 1'
    
    vals = get_column_values(
        excel_file_path, sheet_name,
        'product_name',
        'universal_product_code',
        *[f'image_url_{i}' for i in range(1, 14)]
    )
    for i in range (0,13):
        print(vals[i][0])
if __name__ == "__main__":
    main()
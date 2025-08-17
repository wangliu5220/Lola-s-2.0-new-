# Downloads the images from the data and stores them in a folder with product UPC as name
# Later if this is deployed then it should download the images per request to some backend Database management system
# Also if this is used later on maybe change structure to class and not just random collection of functions 
import requests
import json
import os
import pandas as pd
import Image_finder

# Working order is send xlsx file path, sheet name, column names to get_column_values funtion which calls read_xlsx_file function and returns a list of lists
# Then from the list of lists, loop through the items and call the Sort_and_save_image function which will download and sort the images into their respective upc folder

def pad_upc(upc):
    return str(upc).zfill(12)
    

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
        image_url (string): Url link to image

    Returns:
        Not sure but I think its a byte value of some sort: if you save the return as a png or jpeg it should work, prob shouldv'e looked into this lol
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

def Sort_and_save_image(UPC, image_url, image_name, item_name):
    """
    Sorts the images into a folder with the product UPC as the name, and saves the image with the image name as the filename.
    Args:
        UPC (string): The universal product code of the product
        image_url (string): The url of the image to be downloaded
        image_name (string): The name of the image as given in the excel sheet
        
    Returns: 
        None
    """
    if pd.isna(image_url):
        print("nan image url")
        return    
    len_adjusted_upc = pad_upc(UPC)
    
    upc_dir = f'AI_Image_Scrapping/downloaded_images/{len_adjusted_upc}'

    # Create the UPC directory if it doesn't exist
    if not os.path.exists(upc_dir):
        os.makedirs(upc_dir)

    has_nutrition = Image_finder.is_image(image_url)
    print(has_nutrition)
    if has_nutrition == 'no':
        return
    
    save_path = f'AI_Image_Scrapping/downloaded_images/{len_adjusted_upc}/{item_name}_' + image_name + '.png'
    save_dir = os.path.dirname(save_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image = download_image(image_url)    
    with open(save_path, 'wb') as f:
        f.write(image.content)
        
        
def main():
    """    
        for now it will get all the product names, UPC, and image urls as a list of lists (maybe tuples idk)
        ex) [0][0] = name of first product, [1][0] = upc of first product, [2][0] = image url of first product... (first num is column, second is row)
    """    
    
    excel_file_path = 'final_cut/finalized_web_scraped_data.xlsx'
    sheet_name = 'Sheet 1'
    
    vals = get_column_values(
        excel_file_path, sheet_name,
        'product_name',
        'universal_product_code',
        *[f'image_url_{i}' for i in range(1, 18)]
    )
    for j in range(len(vals[0])): # Rows
        item_name = vals[0][j]
        item_upc = vals[1][j]
        images = [vals[i][j] for i in range(2, 13)]
        print(item_name, int(item_upc))
        print(images)
        if pd.isna(item_upc):
            continue
        for k in range(len(images)):
            if pd.isna(item_upc):
                continue
            image_url = images[k]
            image_name = f"image_{k + 1}"
            try:
                Sort_and_save_image(int(item_upc), image_url, image_name, item_name)
            except Exception as e:
                print(f"Failed to save image for {item_name} with url {image_url}: {e}")
        
        
if __name__ == "__main__":
    main()
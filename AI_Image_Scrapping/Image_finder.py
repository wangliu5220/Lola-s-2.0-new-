# Find and identify the nutrition panel from the images.
import os
import json
import boto3
from botocore.exceptions import ClientError
import Image_Processor
import Image_downloader

# Raod map: write function that downloads all the images into a folder for each product.
#           Run the images through the AI to identify which ones might contain nutrition information. 
#           store the images, and the nutrition image in a json dictionary where the UPC is the key and images are values in a list. (Images are encoded in base64.)
#           This will make it easier later on when processing the information. Assuming there will have to be some repetitive image checking and processing. 

model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"

def is_image(image_url):
    # get passed in information about an image, download to temp folder and run through AI for nutrition/ingredients check. 
    image = Image_downloader.download_image(image_url)

    temp_folder = "AI_Image_Scrapping/temp_images"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    temp_image_path = 'AI_Image_Scrapping/temp_images/temp_image.png'
    with open(temp_image_path, 'wb') as temp_file:
        temp_file.write(image.content)
        
    # Pass to AI to check for nutrition/ingredients
    response = Image_Processor.generate_conversation_image(
            bedrock_client=
            boto3.client(
                service_name="bedrock-runtime",
                region_name="us-east-1"
            ),
            model_id=model_id,
            input_text = 'Is there nutrition information on this image? Is there a list of ingredients on the image? Ingredients should have a label on the image that states explicitly that it is an ingredient and contain the word "ingredient" or "ingredients". Answer only with either yes or no in lowercase.',
            input_image = 'AI_Image_Scrapping/temp_images/temp_image.png'
            
            )

    return(response['output']['message']['content'][0]['text'])
    

def main():
    # downloaded_images_folder = 'AI_Image_Scrapping\downloaded_images'
    # for root, dirs, files in os.walk(downloaded_images_folder):
    #     for file in files:
    #         print(file)
    #         path = os.path.join(root, file)
    #         response = Image_Processor.generate_conversation_image(
    #             bedrock_client=
    #             boto3.client(
    #                 service_name="bedrock-runtime",
    #                 region_name="us-east-1"
    #             ),
    #             model_id=model_id,
    #             input_text = 'Is there nutrition information on this image? Is there a list of ingredients on the image? Answer only with either yes or no.',
    #             input_image = path
                
    #             )

    #         print(response['output']['message']['content'][0]['text'])
    return
    
    


# if __name__ == "__main__":
    # main()    
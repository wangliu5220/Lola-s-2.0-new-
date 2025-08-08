# Find and identify the nutrition panel from the images.
import requests
import os
import json
import boto3
from botocore.exceptions import ClientError
import Image_Processor

# Raod map: write function that downloads all the images into a folder for each product.
#           Run the images through the AI to identify which ones might contain nutrition information. 
#           store the images, and the nutrition image in a json dictionary where the UPC is the key and images are values in a list. (Images are encoded in base64.)
#           This will make it easier later on when processing the information. Assuming there will have to be some repetitive image checking and processing. 

model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"


def main():
    
    response = Image_Processor.generate_conversation_image(
        bedrock_client=
        boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
        ),
        model_id=model_id,
        input_text = 'Is there nutrition information on this image? Is there a list of ingredients on the image?',
        input_image = 'AI_Image_Scrapping\downloaded_images\coca_cola.jpeg'
        
        )

    print(response['output']['message'])
    
    


if __name__ == "__main__":
    main()

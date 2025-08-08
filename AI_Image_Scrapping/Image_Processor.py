import boto3
import os
import json
import logging
from botocore.exceptions import ClientError


# Set the API key as an environment variable


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_conversation_image(bedrock_client,
                          model_id,
                          input_text,
                          input_image):
    """
    Sends a message to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        input text : The text prompt accompanying the image.
        input_image : The path to the input image.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)
    image_exts = []
    raw_images = []
    # input_document_path = "AI_Image_Scrapping/Image_Data/Nutr_Data_Image_AI_scrape_real.xlsx"
    
    # Get image extensions and read in image as bytes
    # for image in input_images:
    #     # # Get image extension and read in image as bytes
    image_ext = input_image.split(".")[-1]
    with open(input_image, "rb") as f:
        raw_image = f.read()
        print("image read")

    # input_document_format = input_document_path.split(".")[-1]
    # with open(input_document_path, 'rb') as input_document_file:
    #     input_document = input_document_file.read()
    
    message = {
        "role": "user",
        "content": [
            {
                "text": input_text
            },
            {
                "image": {
                    "format": image_ext,
                    "source": {
                        "bytes": raw_image
                    }
                }
            }
        ]
    }
    

    messages = [message]

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system = [
            {"text": "You are a data science expert, and your task is to identify and sort key nutrition information from the provided image into the requested categories only using the information form the image given."}
        ],
        inferenceConfig={"maxTokens": 3000, "temperature": .2, "topP": 0.2},
    )

    return response

def generate_message_document(bedrock_client,
                     model_id,
                     input_text,
                     input_document_path,
                     ):
    """
    Sends a message to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        input text : The input message.
        input_document_path : The path to the input document.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Get format from path and read the path
    input_document_format = input_document_path.split(".")[-1]
    with open(input_document_path, 'rb') as input_document_file:
        input_document = input_document_file.read()

    # Message to send.
    message = {
        "role": "user",
        "content": [
            {
                "text": input_text
            },
            {
                "document": {
                    "name": "MyDocument",
                    "format": input_document_format,
                    "source": {
                        "bytes": input_document
                    }
                }
            }
        ]
    }

    messages = [message]

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"maxTokens": 1500, "temperature": 0.5, "topP": 0.9},

    )

    return response


def main():

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # model_id = "us.meta.llama3-2-11b-instruct-v1:0"
    model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    tool_list = [
        
    ]
    
    
    input_text_image = ("Please obtain the nutrition information from these images."
                        "In the image find and sort the nutrition information into the following categories: "
                        "Product Name, Servings per container, Serving Size , % Juice, Amount per serving, Calories, Total Fat (g), Total Fat (% DV), Sodium (mg), Sodium (% DV), Total Carbs (g), Total Carbs (% DV), Total Sugars (g), Includes added sugars (g), Includes Added Sugars (% DV), Protein (g), Protein (% DV), Cholesterol (mg), Cholesterol (% DV), Saturated Fat (g), Saturated Fat (% DV), Dietary Fiber (g), Dietary Fiber (% DV), Trans Fats (g), Trans fats (% DV), Polyunsaturated Fat (g), Monounsaturated Fat (g), and Ingredients"
                        
                        "Each of these categories should be its own key in a json dictionary. The daily value for a category should also be a distinct key."
                        "Cholesterol will sometimes appear as 'Cholest.', which is the same thing."
                        "Includes added sugars (g) will sometimes appear as 'Incl. (g) Added Sugars (% DV)', which is the same thing."
                        "Saturated Fat will sometimes appear as 'Sat. Fat g (% DV)', which is the same thing."
                        "Dietary Fiber will sometimes appear as 'Fiber g (% DV)', which is the same thing."
                        "If there is no daily value for a category, still include it as a key but leave the value as 'Null'."
                        "In the case that the category is not present, include the key but set the value as 'null'."
                        "In the case of serving size, if there are units present, include them in the value and leave the key unchanged."
                        "Do not include line breaks, foward slashes, or back slashes in the response."
                        "Do not return any extra comments, information, or text not related to the categories listed."
                        "Return the nutrition information in json format as a dictionary. Please use brackets and braces for the json."
    )
    input_images = [
        # 'AI_Image_Scrapping\images\coke.png',
        # 'AI_Image_Scrapping\images\diet_dp.webp',
        # 'AI_Image_Scrapping\images\Milk.webp',
        'AI_Image_Scrapping\images\choco_milk.webp',
        # 'AI_Image_Scrapping\images\chobani.png',
        # 'AI_Image_Scrapping\images\polar.png',
        # 'AI_Image_Scrapping\images\kombucha.png',
        # 'AI_Image_Scrapping\images\lemonade.webp',
        # 'AI_Image_Scrapping\images/naked.webp',
        # 'AI_Image_Scrapping\images\monster.webp',
        # 'AI_Image_Scrapping\images/tazo.webp',
        # 'AI_Image_Scrapping\images/vita.webp',
        # 'AI_Image_Scrapping\images\jumex.webp',
        # 'AI_Image_Scrapping\images\olipop.webp',
        # 'AI_Image_Scrapping\images\carnation.webp',
        # 'AI_Image_Scrapping\images/frap.webp',
        # 'AI_Image_Scrapping\images\horizon.webp',
        # 'AI_Image_Scrapping\images\mountain.webp',
        # 'AI_Image_Scrapping\images\culture.webp',
        # 'AI_Image_Scrapping\images/no_pulp.webp',
        # 'AI_Image_Scrapping\images\ice.png',
        # 'AI_Image_Scrapping\images\sanzo.webp',
        # 'AI_Image_Scrapping\images\core.png',
    ]
    input_text_doc = ("Please obtain the nutrition information from this txt file of a beverage nutrition panel."
                        "In the image find and sort the nutrition information into the following categories: "
                        "Product Name, Servings per container, Serving Size , % Juice, Amount per serving, Calories, Total Fat (g), Total Fat (% DV), Sodium (mg), Sodium (% DV), Total Carbs (g), Total Carbs (% DV), Total Sugars (g), Includes added sugars (g), Includes Added Sugars (% DV), Protein (g), Protein (% DV), Cholesterol (mg), Cholesterol (% DV), Saturated Fat (g), Saturated Fat (% DV), Dietary Fiber (g), Dietary Fiber (% DV), Trans Fats (g), Trans fats (% DV), Polyunsaturated Fat (g), Monounsaturated Fat (g), and Ingredients"
                        
                        "Each of these categories should be its own key in a json dictionary. The daily value for a category should also be a distinct key."
                        "Cholesterol will sometimes appear as 'Cholest.', which is the same thing."
                        "Includes added sugars (g) will sometimes appear as 'Incl. (g) Added Sugars (% DV)', which is the same thing."
                        "Saturated Fat will sometimes appear as 'Sat. Fat g (% DV)', which is the same thing."
                        "Dietary Fiber will sometimes appear as 'Fiber g (% DV)', which is the same thing."
                        "If there is no daily value for a category, still include it as a key but leave the value as 'Null'."
                        "In the case that the category is not present, include the key but set the value as 'null'."
                        "In the case of serving size, if there are units present, include them in the value and leave the key unchanged."
                        "Do not include line breaks, foward slashes, or back slashes in the response."
                        "Do not return any extra comments, information, or text not related to the categories listed."
                        "Return the nutrition information in json format as a dictionary. Please use brackets and braces for the json."
    )
    input_doc = "AI_Image_Scrapping/rawText.txt"
    
    
    
    try:

        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
            )

        with open('AI_Image_Scrapping\AI_Response.jsonl', 'w') as f:
            
            response = generate_message_document(bedrock_client, model_id, input_text_image, input_doc) 

            # for i in range(len(input_images)):
            #     response = generate_conversation_image(
            #         bedrock_client, 
            #         model_id, 
            #         input_text_image,
            #         input_images[i]
            #         )

            output_message = response['output']['message']
        
            # Write the response to a json file
            json.dump(output_message["content"], f, indent=4)
                
            print(f"Role: {output_message['role']}")

            for content in output_message['content']:
                print(f"Text: {content['text']}")

            token_usage = response['usage']
            print(f"Input tokens:  {token_usage['inputTokens']}")
            print(f"Output tokens:  {token_usage['outputTokens']}")
            print(f"Total tokens:  {token_usage['totalTokens']}")
            print(f"Stop reason: {response['stopReason']}")

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")

    else:
        print(
            f"Finished generating text with model {model_id}.")


if __name__ == "__main__":
    main()
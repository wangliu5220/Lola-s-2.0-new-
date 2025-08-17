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
    # image_exts = []
    # raw_images = []
    # image extension and read in image as bytes
    image_ext = input_image.split(".")[-1]
    with open(input_image, "rb") as f:
        raw_image = f.read()
        print("image read")

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

def generate_json_image_conversation(bedrock_client,
                          model_id,
                          input_text,
                          input_images,
                          tool_list):
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
    messages = []
    
        
    message = {
        "role": "user",
        "content": [
            {
                "text": input_text
            },
            {
                "text": "Please use the summarize_nutrition_info tool to identify and sort key nutrition information from the provided image into the requested categories only using the information form the image given."
            },
        ]
    }
        
    for input_image in input_images:
        image_ext = input_image.split(".")[-1]
        with open(input_image, "rb") as f:
            raw_image = f.read()
            print("image read")
        message['content'].append({
            "image": {
                "format": image_ext,
                "source": {
                    "bytes": raw_image
                }
            }
        })
            
    messages = [message]
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={
            "maxTokens": 3000,
            "temperature": 0
        },
        toolConfig={
            "tools": tool_list,
            "toolChoice": {
                "tool": {
                    "name": "summarize_nutrition_info"
                }
            }
        }
    )
    return response


def main():

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # model_id = "us.meta.llama3-2-11b-instruct-v1:0"
    model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    tool_list = [
        {
        "toolSpec": {
            "name": "summarize_nutrition_info",
            "description": "Summarize nutrition and ingredient information.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {                        
                        "servings_per_container": {
                            "type": ["string", "null"],
                            "description": "Number of servings in the container. If not found in the image it will be None"
                        },
                        "serving_size": {
                            "type": ["string", "null"],
                            "description": "The serving size of the product. If not found in the image it will be None"
                        },
                        "percent_juice": {
                            "type": ["string", "null"],
                            "description": "The percentage of juice in the product. If not found in the image it will be None"
                        },
                        "amount_per_serving": {
                            "type": ["string", "null"],
                            "description": "The amount of the product per serving. If not found in the image it will be None"
                        },
                        "calories": {
                            "type": ["string", "null"],
                            "description": "The number of calories in the product. If not found in the image it will be None"
                        },
                        "total_fat_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of total fat in the product in absolute terms. If not found in the image it will be None"
                        },
                        "total_fat_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of total fat in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "sodium_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of sodium in the product in absolute terms. If not found in the image it will be None"
                        },
                        "sodium_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of sodium in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "total_carbs_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of total carbs in the product in absolute terms. If not found in the image it will be None"
                        },
                        "total_carbs_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of total carbs in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "total_sugars_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of total sugars in the product in absolute terms. If not found in the image it will be None"
                        },
                        "included_added_sugars_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of included added sugars in the product in absolute terms. If not found in the image it will be None"
                        },
                        "included_added_sugars_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of included added sugars in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "protein_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of protein in the product in absolute terms. If not found in the image it will be None"
                        },
                        "protein_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of protein in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "cholesterol_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of cholesterol in the product in absolute terms. If not found in the image it will be None"
                        },
                        "cholesterol_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of cholesterol in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "saturated_fat_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of saturated fat in the product in absolute terms. If not found in the image it will be None"
                        },
                        "saturated_fat_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of saturated fat in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "trans_fat_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of trans fat in the product in absolute terms. If not found in the image it will be None"
                        },
                        "trans_fat_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of trans fat in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "fiber_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of fiber in the product in absolute terms. If not found in the image it will be None"
                        },
                        "fiber_DV": {
                            "type": ["string", "null"],
                            "description": "The amount of fiber in the product as a percentage of the daily value. If not found in the image it will be None"
                        },
                        "polyunsaturated_fat_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of polyunsaturated fat in the product in absolute terms. If not found in the image it will be None"
                        },
                        "monounsaturated_fat_absolute": {
                            "type": ["string", "null"],
                            "description": "The amount of monounsaturated fat in the product in absolute terms. If not found in the image it will be None"
                        },
                        "ingredients": {
                            "type": "array",
                            "description": "An array of product ingredients.",
                            "items": { "type": "string" }
                        },
                        
                    },
                    "required": [
                        "product_name",
                        "servings_per_container",
                        "serving_size",
                        "percent_juice",
                        "amount_per_serving",
                        "calories",
                        "total_fat_absolute",
                        "total_fat_DV",
                        "sodium_absolute",
                        "sodium_DV",
                        "total_carbs_absolute",
                        "total_carbs_DV",
                        "total_sugars_absolute",
                        "included_added_sugars_absolute",
                        "included_added_sugars_DV",
                        "protein_absolute",
                        "protein_DV",
                        "cholesterol_absolute",
                        "cholesterol_DV",
                        "saturated_fat_absolute",
                        "saturated_fat_DV",
                        "trans_fat_absolute",
                        "trans_fat_DV",
                        "fiber_absolute",
                        "fiber_DV",
                        "polyunsaturated_fat_absolute",
                        "monounsaturated_fat_absolute",
                        "ingredients"
                    ]
                }
            }
        }
        }
        
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
    # input_images = ['AI_Image_Scrapping\downloaded_images/464287973721\(4 pack) Jumex Mango Nectar from Concentrate, 11.3 Fl. oz._image_3.png',
    #                 'AI_Image_Scrapping\downloaded_images\850017346024\Culture Pop Soda Watermelon, Probiotic Soda, 12 fl oz_image_2.png'
        
    # ]
    input_images = {}
    
    # input_text_doc = ("Please obtain the nutrition information from this txt file of a beverage nutrition panel."
    #                     "In the image find and sort the nutrition information into the following categories: "
    #                     "Product Name, Servings per container, Serving Size , % Juice, Amount per serving, Calories, Total Fat (g), Total Fat (% DV), Sodium (mg), Sodium (% DV), Total Carbs (g), Total Carbs (% DV), Total Sugars (g), Includes added sugars (g), Includes Added Sugars (% DV), Protein (g), Protein (% DV), Cholesterol (mg), Cholesterol (% DV), Saturated Fat (g), Saturated Fat (% DV), Dietary Fiber (g), Dietary Fiber (% DV), Trans Fats (g), Trans fats (% DV), Polyunsaturated Fat (g), Monounsaturated Fat (g), and Ingredients"
                        
    #                     "Each of these categories should be its own key in a json dictionary. The daily value for a category should also be a distinct key."
    #                     "Cholesterol will sometimes appear as 'Cholest.', which is the same thing."
    #                     "Includes added sugars (g) will sometimes appear as 'Incl. (g) Added Sugars (% DV)', which is the same thing."
    #                     "Saturated Fat will sometimes appear as 'Sat. Fat g (% DV)', which is the same thing."
    #                     "Dietary Fiber will sometimes appear as 'Fiber g (% DV)', which is the same thing."
    #                     "If there is no daily value for a category, still include it as a key but leave the value as 'Null'."
    #                     "In the case that the category is not present, include the key but set the value as 'null'."
    #                     "In the case of serving size, if there are units present, include them in the value and leave the key unchanged."
    #                     "Do not include line breaks, foward slashes, or back slashes in the response."
    #                     "Do not return any extra comments, information, or text not related to the categories listed."
    #                     "Return the nutrition information in json format as a dictionary. Please use brackets and braces for the json."
    # )
    # input_doc = "AI_Image_Scrapping/rawText.txt"
    
    
    try:

        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
            )
        upc_dir = []

        downloaded_images_dir = 'AI_Image_Scrapping/downloaded_images'
        for root, dirs, files in os.walk(downloaded_images_dir):
            upc_dir.extend(dirs)
            
            if root.split('\\')[-1] in upc_dir:
                input_images[root.split('\\')[-1]] = [os.path.join(root, file) for file in files if file.endswith(".png")]
        print(input_images)
                    
        with open('AI_Image_Scrapping\AI_Response.jsonl', 'w') as f:
            f.write('[\n')
            for upc in upc_dir:
                response = generate_json_image_conversation(
                    bedrock_client,
                    model_id,
                    input_text_image,
                    input_images[upc],
                    tool_list
                )
                response_message = response['output']['message']

                response_content_blocks = response_message['content']

                content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)

                tool_use_block = content_block['toolUse']

                tool_result_dict = tool_use_block['input']
                tool_result_dict['universal_product_code'] = upc
                print(json.dumps(tool_result_dict, indent=4))
                json.dump(tool_result_dict, f, indent=4)
                if f.tell() > 0:
                    f.write(',\n')
            f.write('\n]')

            # if response['output']['message']['contentType'] == "text/plain":
            #     print(f"Generated text: {response['output']['message']['content']}")

            #     token_usage = response['usage']
            #     print(f"Input tokens:  {token_usage['inputTokens']}")
            #     print(f"Output tokens:  {token_usage['outputTokens']}")
            #     print(f"Total tokens:  {token_usage['totalTokens']}")
            #     print(f"Stop reason: {response['stopReason']}")

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")

    else:
        print(
            f"Finished generating text with model {model_id}.")


if __name__ == "__main__":
    main()
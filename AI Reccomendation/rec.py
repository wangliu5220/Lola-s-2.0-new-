import sys
import boto3
import botocore
from botocore.exceptions import ClientError
import json
import os
import base64
import pandas as pd

def generate_message_document(bedrock_client,
                     model_id,
                     input_product,
                     input_text,
                     doc_path,
                     tool_list,
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

    rec_document_format = doc_path.split(".")[-1]
    with open(doc_path, 'rb') as input_document_file:
        rec_document = input_document_file.read()
    rec_b64 = base64.b64encode(rec_document)
    print(f"Rec doc (base64): {len(rec_b64)} bytes")
    print(f"Total: {len(rec_b64)} bytes")

    # Message to send.
    message = {
        "role": "user",
        "content": [
            {
                "document": {
                    "name": "product_information_sheet",
                    "format": rec_document_format,
                    "source": {
                        "bytes": rec_document
                    }
                    
                }
            },
            {
                "text": input_text
            },
            {
                "text": input_product
            },
            {
                "text": "Please use the Get_Reccomendations tool to find the relavent products and product information."
            },

        ]
    }

    messages = [message]
    print(f"Message size: {sys.getsizeof(messages[0])} bytes")

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"maxTokens": 7000, "temperature": 0.5},
        toolConfig={
                    "tools": tool_list,
                    "toolChoice": {
                        "tool": {
                            "name": "Get_Reccomendations"
                        }
                    }
                }
        )

    return response


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, "cleaned_9_3.xlsx")
    df = pd.read_excel(excel_path)
    tool_list = [
        {
        "toolSpec": {
            "name": "Get_Reccomendations",
            "description": "Information of 4 products.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "product_1_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_1_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the first product"
                        },
                        "prod_1_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the first product"
                        },
                        "product_2_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_2_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the second product"
                        },
                        "prod_2_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the second product"
                        },
                        "product_3_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_3_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the third product"
                        },
                        "prod_3_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the third product"
                        },
                        "product_4_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_4_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the fourth product"
                        },
                        "prod_4_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the fourth product"
                        }
                    }
                }
            }
        }
        }
    ]
    df1 = df[["shelf", "product_name", "price_per_100", "calories_per_100", "sodium_absolute_per_100", 
             "saturated_fat_absolute_per_100", "included_added_sugars_absolute_per_100","universal_product_code"
              #"product_URL", "thumbnail_image_url","universal_product_code", "ultra_processed_flag"
             ]]
    df2 = df[["product_name","product_URL", "thumbnail_image_url","universal_product_code", "ultra_processed_flag"]]
    df1.to_excel("AI Reccomendation/temp_reduced_sheet1.xlsx", index=False)
    df2.to_excel("AI Reccomendation/temp_reduced_sheet2.xlsx", index=False)
    
    # reduce added sugars, sodium, saturated fat per 100, calories
    #  idk if this should be per the daily value but these are important too
    # 2. ultraproccessed 3. beverage category 4. price (average price)

    cleaned_excel_path1 = "AI Reccomendation/temp_reduced_sheet1.xlsx"
    cleaned_excel_path2 = "AI Reccomendation/temp_reduced_sheet2.xlsx"

    model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    product_name_input = input("Please enter a product name: ")

    message = ("Given a product, give recommendations using the xlsx document provided."
               "Give at least 4 products alongside their name and universal product code."
               "The following are product recommendation considerations ranging from highest importance to lowest."
                "Nutrition (must-have): Lower added sugars per 100, lower calories per 100, lower sodium per 100, and lower saturated fat per 100g/mL."
                "Rank these nutrition must-haves in this order:"
                "1. Lower added sugars per 100"
                "2. Lower calories per 100"
                "3. Lower sodium per 100"
                "4. Lower saturated fat per 100g/mL"
                "Ultraprocessed: Prefer swaps from ultraprocessed → non-ultraprocessed; if none exist, choose lower nutrient-dense ultraprocessed options."
                "Category & Texture: Stay in the same beverage category (soda→soda) or close (soda→seltzer/kombucha), keeping texture (carbonated→carbonated)."
                "Price: Keep within ±5% to 10% price per 100g/mL; otherwise, select best-value alternatives."
                "Package size & type: Match original purpose (bulk vs single-serve)."
                "Popularity: Prefer higher ratings/reviews once above factors are satisfied."
                "Flavor: Maintain similar flavor profile when possible."
                "Always provide: (a) the ranked alternatives, and (b) a short justification for each based on these rules."
               )
    
    
    try: 
        
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
            )
        response = generate_message_document(
            bedrock_client,
            model_id,
            product_name_input,
            message,
            cleaned_excel_path1,
            tool_list
        )
        
        print(response['output']['message']['content'])
        response_message = response['output']['message']
        with open("AI Reccomendation/chat_hist.json", "w") as f:
            response_content_blocks = response_message['content']
            content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)
            tool_use_block = content_block['toolUse']
            tool_result_dict = tool_use_block['input']
            print(json.dumps(tool_result_dict, indent=4))
            json.dump(tool_result_dict, f, indent=4)
    except ClientError as e:
        print("Client Error: " +e.response['Error']['Message'])
    return



if __name__ == "__main__":
    main()
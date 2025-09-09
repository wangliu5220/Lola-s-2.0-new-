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
                "text": "Use the Get_Recommendations tool to find the relevant products and product information. Return the results in the same format as the tool."
            },

        ]
    }

    messages = [message]
    print(f"Message size: {sys.getsizeof(messages[0])} bytes")

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"maxTokens": 6000, "temperature": 0.1},
        toolConfig={
                    "tools": tool_list,
                    "toolChoice": {
                        "tool": {
                            "name": "Get_Recomendations"
                        }
                    }
                },
        system = [
            {
                "text": "You are a nutritionist providing product recommendations."
            }
        ]
    )

    return response

def print_dict_response(dict):
    line_sep = 0
    for key, value in dict.items():
        if line_sep % 3 == 0:
            print("\n")
        print(f"{key}: {value}")
        line_sep += 1

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, "cleaned_9_3.xlsx")
    df = pd.read_excel(excel_path)
    tool_list = [
        {
        "toolSpec": {
            "name": "Get_Recomendations",
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
                        },
                        "product_5_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_5_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the fifth product"
                        },
                        "prod_5_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the fifth product"
                        },
                        "product_6_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_6_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the sixth product"
                        },
                        "prod_6_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the sixth product"
                        },
                        "product_7_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_7_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the seventh product"
                        },
                        "prod_7_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the seventh product"
                        },
                        "product_8_name": {
                            "type": ["string"],
                            "description": "The value from the product_name column of the excel sheet"
                        },
                        "prod_8_UPC": {
                            "type": ["string"],
                            "description": "The universal product code of the eighth product"
                        },
                        "prod_8_reasoning": {
                            "type": ["string"],
                            "description": "The reasoning for recommending the eighth product"
                        },
                    }
                }
            }
        }
        }
    ]
    df1 = df[["shelf", "product_name", "price_per_100", "calories_per_100", "sodium_absolute_per_100", 
             "saturated_fat_absolute_per_100", "included_added_sugars_absolute_per_100","universal_product_code", "ultra_processed_flag"
             ]]
    df2 = df[["product_name","product_URL", "thumbnail_image_url","universal_product_code", "ultra_processed_flag"]]
    df1.to_excel("AI Reccomendation/temp_reduced_sheet1.xlsx", index=False)
    df2.to_excel("AI Reccomendation/temp_reduced_sheet2.xlsx", index=False)

    cleaned_excel_path1 = "AI Reccomendation/temp_reduced_sheet1.xlsx"
    cleaned_excel_path2 = "AI Reccomendation/temp_reduced_sheet2.xlsx"

    # print(df2.head(3))
    
    model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"

    message = ("Given a product, give recommendations using the xlsx document provided."
               "Give at least 8 products and always provide their product_name, universal product code, and a reasoning for why the product was chosen in this order."
               "The following are product recommendation considerations ranging from highest importance to lowest."
               "For all product recommendations use only these following criteria as valid reasons to recommend a product:"
                "1. Nutrition (must-have): Lower added sugars per 100, lower calories per 100, lower sodium per 100, and lower saturated fat per 100g/mL. Rank these nutrition must-haves in this order:"
                "1.1 Lower added sugars per 100"
                "1.2 Lower calories per 100"
                "1.3 Lower sodium per 100"
                "1.4 Lower saturated fat per 100g/mL"
                "2. Ultraprocessed: Prefer swaps from ultraprocessed → non-ultraprocessed; if none exist, choose lower nutrient-dense ultraprocessed options."
                "3. Category & Texture: Stay in the same beverage category (soda→soda) or close (soda→seltzer/kombucha), keeping texture (carbonated→carbonated)."
                "4. Price: Keep within ±5% to 10% price per 100g/mL; otherwise, select best-value alternatives."
                "5. Package size & type: Match original purpose (bulk vs single-serve)."
                "6. Popularity: Prefer higher ratings/reviews once above factors are satisfied."
                "7. Flavor: Maintain similar flavor profile when possible."
                "In the recommendation process be very logical and use the nutrition information provided in the xlsx document."
                "All recommendations should fulfill the first requirement on nutrition. Product one should fulfill the most requirements and be the closest in terms of product type and functionality (ie. carbonated, caffeinated, sports drink)."
                "For each product down the list, the requirements should be progressively relaxed and the variety in product type can also vary if and only if it does not compromise nutrition."
                "Always provide: (a) the ranked alternatives, and (b) a detailed justification for each based on these rules."

               )
    
    print("\nRandom product names: \n")
    for i in range(6):
        print(df2.sample(1)["product_name"].iloc[0])
    print("\n")
            
    product_name_input = input("Please enter a product name: ")
    
    while(product_name_input != "exit"):
        product_urls = []
        thumbnail_urls = []
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
            
            # print(response['output']['message']['content'])
            response_message = response['output']['message']
            with open("AI Reccomendation/chat_hist.json", "w") as f:
                response_content_blocks = response_message['content']
                content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)
                tool_use_block = content_block['toolUse']
                tool_result_dict = tool_use_block['input']
                # prod_1_UPC_row = df2.loc[df2["universal_product_code"] == prod_1_UPC]
                custom_order = ([
                    "product_1_name", 
                    "prod_1_UPC", 
                    "prod_1_reasoning",
                    "product_2_name", 
                    "prod_2_UPC", 
                    "prod_2_reasoning",
                    "product_3_name",
                    "prod_3_UPC",
                    "prod_3_reasoning",
                    "product_4_name",
                    "prod_4_UPC",
                    "prod_4_reasoning",
                    "product_5_name",
                    "prod_5_UPC",
                    "prod_5_reasoning",
                    "product_6_name",
                    "prod_6_UPC",
                    "prod_6_reasoning",
                    "product_7_name",
                    "prod_7_UPC",
                    "prod_7_reasoning",
                    "product_8_name",
                    "prod_8_UPC",
                    "prod_8_reasoning"
                    ]
                )
                tool_result_dict = dict(sorted(tool_result_dict.items(), key=lambda x: custom_order.index(x[0]) if x[0] in custom_order else float('inf')))
                # print(json.dumps(tool_result_dict, indent=4))
                print_dict_response(tool_result_dict)
                json.dump(tool_result_dict, f, indent=4)

        except ClientError as e:
            print("Client Error: " +e.response['Error']['Message'])
        
        product_name_input = input("Please enter new search term: ")
    return



if __name__ == "__main__":
    main()
import boto3
import botocore
import os


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
    
    return


def __main__():
    if __name__ == "__main__":
        main()
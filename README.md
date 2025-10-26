
# Lola's 2.0

## Update and Install Dependencies: 
```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

Key Libraries that will be installed : 

1. beautifulsoup4
2. requests 
3. pandas
4. boto3
5. botocore


## Startup Guide For Setting Up Bedrock API


To run the AI functionality on your local machine, you need to first get access to AWS credentials.
Here is a quick start-up guide assuming you have access to an already set up IAM user profile with Bedrock permissions and public/private access keys:
(Also make sure that u requested access to the model u want to use in the AWS Bedrock interface)

1. Download [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. After downloading, open a terminal and type 'aws configure' and enter the following information 

   a.    AWS access key ID
   
   b.    AWS secret access key
   
   c.    Default region name: us-east-1
   
   d.    Output format: just press enter to skip

   
3. Restart VSCode if using VSCode (if need be restart the computer as well)

You should now be able to send Bedrock API calls without having to add the API key to your code

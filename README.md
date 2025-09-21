**Startup Guide For Setting Up Bedrock API**


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


**Other Stuff**

You need to install these libraries: 

1. beautifulsoup4
2. requests 
3. pandas
4. boto3
5. Maybe botocore (forgot if this comes with the boto3 library)

For each library above, type this into the terminal "pip install [name of library]"
If you want feel free to switch into a virtual environment, if you need help let me know. 

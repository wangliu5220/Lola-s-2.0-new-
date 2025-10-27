
# Lola's 2.0

## Virtual Environment
It is likely in our best interest to work within a virtual environment so that we can properly handle our dependencies.

This is how you would do set one up and use it:
```bash
python3 -m venv --copies venv
source venv/bin/activate
```

To exit:
```bash
deactivate
```

## Update and Install Dependencies: 

Before development run:
```bash
pip install -r requirements.txt
```

After development run this command from the root directory of Lola's:
```bash
pip freeze > requirements.txt
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


## Initializing and Running Qdrant Databse Locally

In the root directory run:
```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

To view the database, you can go to http://localhost:6333/dashboard after running the previous commands.

If you see that there are no entries in the database, you may have to run the ingest script in Team_M/backend/db_ingest.py

## Running FastAPI Server

```bash
fastapi run Team_M/backend/api/main.py --reload
```
*Note that API endpoints will  not work if the database is not running.*
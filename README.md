   
# Amazon Review Analysis and Price Comparison


Abel Phillip 001056119


Aishwarya Parab


Vidhi Patel


## Introduction


Data pipeline for analyzing the sentiment behind the review of a product on amazon, summarizing the review and translating it in the required language. All of this is deployed on the cloud to run a completely serverless infrastructure on demand. 


## Set-up
The pipeline uses the services as follows


EC2,
Lambda,
API Gateway,
S3,
DynamoDB,
Glue,
Comprehend,
Translate,
AWS Cognito


## Clone Repository


git clone https://github.com/abel-philip/product_review_sentiment_analysis_with_AWS


### Deploying Lambda Functions
Upload the .py lambda files as functions and add the dependencies from the zipped python folder in the layers of the lambda


### Deploying Streamlit App
The python code for this app can be found on the dev branch /streamlit/


```
pip3 install streamlit
pip3 install boto3
pip3 install pandas
pip3 install configparser
pip3 install requests
```


### S3 Bucket
Create an s3 bucket of name 'etl-reviews' that the lambda can access and store the review data in it


### DynamoDB
Review_Sentiment table in dynamoDB stores the sentiments from the comprehend Lambda


### AWS GLue
In the VPC console, create a VPC and make sure the DNS hostnames and DNS Resolutions are enabled. Then create a Glue database 'Review_Database'
Create a crawler linked to the S3 with a connection that uses the above vpc. Then run the crawler and select S3 destination bucket. 


















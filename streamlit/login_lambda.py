import boto3
from boto3.dynamodb.conditions import Key, Attr
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from mangum import Mangum
# key = Fernet.generate_key()
key= '-OiJlttOaFGgb_8GVAsJRy5c8sokNizC1BZ8GGt2TX8='
# parameters for authentication
API_KEY = "123abc"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"
userRegion = "us-east-1"
userClientId = "4hkma6pavubar061g3u11fek9q"
usrPoolId= "us-east-1_o7TlGk5JE"
cidp = boto3.client('cognito-idp',region_name='us-east-1')
auth = Cognito(region= userRegion, userPoolId= usrPoolId)
getUser = CognitoCurrentUser(region= userRegion, userPoolId= usrPoolId)

app = FastAPI()
@app.get("/", tags=["Homo"])
async def homepage():
    return "Welcome to API homepage!"

# Sign Up
@app.get("/createUser", tags=["Create User"])
async def sign_up_cognito(usrName: str, usrPassword: str):
    cidp.sign_up(ClientId= userClientId, Username= usrName, Password= usrPassword)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User_details') # made already
    response = table.put_item(
       Item={
            'Username': usrName, #partition key
            'Password': usrPassword,
        }
    )
    result = "User Created. Confirm Sign Up"
    return result

# Confirm Sign up
@app.get("/confirmUser", tags=["Confirm User"])
async def create_user_on_cognito(usrName: str, usrPassword: str):
    cidp.admin_confirm_sign_up(UserPoolId= usrPoolId, Username= usrName)
   
    return "User Confirmed"

# Generate JWT Token
@app.get("/tokens", tags=["Generate TOkens"])
async def generate_JWT_token(usrName: str, usrPassword: str):
    JWT = cidp.admin_initiate_auth(UserPoolId= usrPoolId, ClientId= userClientId, AuthFlow= "ADMIN_NO_SRP_AUTH", AuthParameters= { "USERNAME": usrName, "PASSWORD": usrPassword })   
    AccessToken = JWT["AuthenticationResult"]["AccessToken"]
    RefreshToken = JWT["AuthenticationResult"]["RefreshToken"]
    IDToken = JWT["AuthenticationResult"]["IdToken"]
    refreshToken = cidp.admin_initiate_auth(UserPoolId= usrPoolId, ClientId= userClientId, AuthFlow= "REFRESH_TOKEN_AUTH", AuthParameters= {"REFRESH_TOKEN" : RefreshToken})
    dynamodb = boto3.resource('dynamodb')
    refreshToken = refreshToken["AuthenticationResult"]["IdToken"]
    table = dynamodb.Table('Tokens') 
    response = table.update_item(Key = {'Username': usrName},
        UpdateExpression="set RefreshToken=:r,JWT=:t,AccessToken=:a,IDToken=:i",
        ExpressionAttributeValues={
            ':t':JWT,
            ':a': AccessToken,
            ':r': refreshToken,
            ':i': IDToken
        }
    )
    result = "Tokens Created"
    return response,result,refreshToken

# Logout page to delete cookies and block user from accessing the data
@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response
# Access the Swagger//Documentation page
# To access - with token - http://localtest.me:8000/documentation?access_token=123abc
"""@app.get("/documentation", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response"""


@app.get("/product_reviews")
async def get_product_reviews(product_id: str):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Review_Sentiments')
    response = table.scan(
        FilterExpression=Attr('product_id').eq(product_id)
    )
    positives = [ i['review'] for i in response['Items'] if i['sentiment']=='POSITIVE']
    negatives = [i['review'] for i in response['Items'] if i['sentiment']=='NEGATIVE']
    return positives, negatives
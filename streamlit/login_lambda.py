import boto3, io, json,time
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
    str1 = ""  
    str2=""
    try:
        for ele in positives:  
            str1 += ele
            str2=ele
        for ele in negatives:  
            str1 += ele
        print(str1)
    except:
        print("exception")
    outbucket = 'final-reviews'
    s3 = boto3.resource('s3')
    outfile = io.StringIO(str1)
    # Generate output file and close it!
    outobj = s3.Object(outbucket, product_id + '.txt')
    outobj.put(Body=outfile.getvalue())
    outfile.close()
    return positives, negatives

@app.get("/keywordextract", tags=["Extraction"])
async def deidentify(ExeName: str, keyname : str, TranslatedLanguage: str ):
    #arn:aws:states:us-east-1:198250712026:stateMachine:DeIdandMaskStateMachine-V9YcZVzewMXk
    text = '''result Was not sure that a camera this inexpensive would be 'any good' - but as it turns out -- -actually a pretty nice little camera that I have mounted on top of my LED screen ---
     disturbed sound
    Took some tweaking to get it focused and attached to my monitor. I use it as one of my cameras to watch my 3D printer via Teamveiwer as I print things by remote from work. I don't know what it is, I bought two for a project, but it has a better picture than my 40 microsoft brand camera.
    Was not sure that a camera this inexpensive would be 'any good' - but as it turns out -- -actually a pretty nice little camera that I have mounted on top of my LED screen ---
    disturbed sound
    Took some tweaking to get it focused and attached to my monitor. I use it as one of my cameras to watch my 3D printer via Teamveiwer as I print things by remote from work. I don't know what it is, I bought two for a project, but it has a better picture than my 40 microsoft brand camera.'''
    print("1")
    TranslatedLanguage = TranslatedLanguage
    # The Amazon Resource Name (ARN) of the state machine to execute.
    STATE_MACHINE_ARN = 'arn:aws:states:us-east-1:362654931460:stateMachine:StateMachineAmazon'
    #The name of the execution user input
    EXECUTION_NAME = ExeName #u have to take this from user ...
    #reading the file to be deidentified
    print("3")
    #The string that contains the JSON input data for the execution
    # isEnglish = isEnglish
    # TranslatedLanguage = TranslatedLanguage
    # inputJSON = (f'{"message": "he is an amazing boy. He works very hard","{isEnglish}": "yes","{TranslatedLanguage}": "en"}')
    if TranslatedLanguage == 'fr':
        inputJSON = {"message": "This is a fairly good product. REeally recommend buying this product","isEnglish": "no","TranslatedLanguage": "fr"}
    if TranslatedLanguage == 'en':
        inputJSON = {"message": "This is a fairly good product","isEnglish": "yes","TranslatedLanguage": "en"}
    # inputJSON = {"message": "This product is really good","isEnglish": "yes","TranslatedLanguage": "en"}
    # inputJSON = '{"message": "he is an amazing boy. He works very hard","isEnglish": "'+isEnglish+',"TranslatedLanguage":"'+TranslatedLanguage+'"}'
    # inputJSON = {"message": "he is an amazing boy. He works very hard","isEnglish": "yes","TranslatedLanguage": "en"}
    INPUT = json.dumps(inputJSON)
    print(INPUT)
    sfn = boto3.client('stepfunctions')
    print("4")
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=EXECUTION_NAME,
        input=INPUT
    )
    print("5")
    #display the arn that identifies the execution
    executionARN = response.get('executionArn')
    print("running with Mask")
    #waiting
    time.sleep(1)
    print("wait....")
    time.sleep(5)
    print("wait....")
    time.sleep(4)
    print("wait....")
    
    #getting actual response
    response = sfn.get_execution_history(
        executionArn=executionARN,
        maxResults=1,
        reverseOrder=True,
        includeExecutionData=True
    )
    return response

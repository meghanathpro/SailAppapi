from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fyers_api import fyersModel
from fyers_api import accessToken

app = FastAPI()
session_data = []


@app.get("/")
def read_root():
    return {"Bro": "eta"}

# 1.Installing fyers, giving app_id & client_key to generate redirect url for access.

@app.get("/login",response_class=HTMLResponse)
async def read_items(client_id1: str,secret_key1: str,redirect_uri1: str):
 
    session=accessToken.SessionModel(client_id=client_id1,secret_key=secret_key1,redirect_uri=redirect_uri1,response_type="code",grant_type="authorization_code",state = "None")
    session_data.append(session)
    response = session.generate_authcode()  
    return RedirectResponse(url= response)

# 2.Redirect with auth_code and submitting for access token.

@app.get("/redirect", response_class=HTMLResponse)
async def read_root(s: str, code: int, auth_code: str,state: str):

    return """
        <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <div style="text-align: center;" >
            <h1 style="color:blue;"> Running : {s}</h1>
            <h2>Success : {code}<h2>
            <h3>Auth_ID : {auth_code}<h3>
            <h3>State : {state}<h3>
            <a href="https://8590yx.deta.dev/finalauth?auth_detail={auth_code}&secret_key=&client_id0="> Grant Token</a>
            </div>
        </body>

       
    </html>
    """.format(s=s,code=code,auth_code=auth_code,state=state)

# 3.Final accesstoken retriving and checking basic details
@app.get("/finalauth",response_class=HTMLResponse)
async def read_item(auth_detail: str, secret_key: str, client_id0:str):

    redirect_uri="https://8590yx.deta.dev/redirect"
    
    #session=accessToken.SessionModel(client_id=client_id0,secret_key=secret_key,redirect_uri=redirect_uri,response_type="code", grant_type="authorization_code",state=None)
    session=session_data[0]
    session.set_token(auth_detail)
    response = session.generate_token()
    access_token = response["access_token"]

    resp_id="/usermenu?name_id="+client_id0+"&auth_hash="+access_token

    return RedirectResponse(url= resp_id)



@app.get("/usermenu")
async def read_item(name_id: str,auth_hash:str):

    fyers = fyersModel.FyersModel(client_id=name_id, token=auth_hash)
    profile_info=fyers.get_profile()

    return profile_info

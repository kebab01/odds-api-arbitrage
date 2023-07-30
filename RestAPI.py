from http.client import HTTPException
from fastapi import FastAPI, Header, HTTPException, Request
from dotenv import load_dotenv
import os
import uvicorn
import logging
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
import json
import main
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio

load_dotenv()

logging.basicConfig(filename="api.log", level=logging.NOTSET, format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
app = FastAPI()

async def validate_authorization_header(request: Request, call_next):
    if request.url.path != "/docs":
        authorization_header = request.headers.get("Authorization")
        print(authorization_header)
        if not authorization_header:
            error_message = {"error": "Authorization header is missing"}
            return JSONResponse(status_code=401, content=error_message)

        provided_token = authorization_header.split("Bearer ")[-1]
        if provided_token != AUTH_TOKEN:
            error_message = {"error": "Invalid authorization token"}
            return JSONResponse(status_code=401, content=error_message)

    response = await call_next(request)
    return response


app.middleware("http")(validate_authorization_header)

@app.get('/updates')
async def get_events():
    
    try:
        with open('opportunities.json','r') as f:
            data=json.load(fp=f);
    except FileNotFoundError:
        logging.error("Could not find file")
        raise HTTPException(status_code=500)
    
    logging.info("Serving opportunities.json to client")
    return data

@app.get('/retrieve-latest')
async def retrieve_latest():
    await main.find_opportunities()

    return 200

@app.get("/download-excel")
def download_excel():
    # Specify the path to the existing Excel file on the server
    file_path = "./bets.xlsx"
    # Use FileResponse to serve the existing Excel file
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="opportunities.xlsx")



if __name__ == "__main__":
    uvicorn.run("RestAPI:app", host="0.0.0.0", port=8080, log_level="trace", reload=True)

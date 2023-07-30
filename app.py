import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import cv2
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from main import management,check,gen_frames,updatedValues1,updatedValues2

load_dotenv('.env')

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed1')
def video_feed1():
    return StreamingResponse(management("recording.mp4","CarPosition",10), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/video_feed2')
def video_feed2():
    return StreamingResponse(management("CMR_bike.mp4","bikepickle",4), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/value1')
def values1():
    data = {"value":updatedValues1()}
    return JSONResponse(content=data)
@app.get('/value2')
def values2():
    data = {"value":updatedValues2()}
    return JSONResponse(content=data)

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)
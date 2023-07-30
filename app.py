import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import cv2
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from main import management,check,gen_frames

load_dotenv('.env')

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/video_feed_1')
def video_feed_1():
    return StreamingResponse(management("static/recording.mp4","CarPosition",10), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/video_feed_2')
def video_feed_2():
    return StreamingResponse(management("static/CMR_bike.mp4","bikepickle",4), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/video_feed_3')
def video_feed_3():
    return StreamingResponse(management("static/CMR_car_ug.mp4","pickle_ug_1",2), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)
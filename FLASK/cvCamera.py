import numpy as np
import cv2
import datetime
from flask import Flask, render_template

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera

def generate(cap=cap):
    while True:
        ## Capture fame by frame
        ret, frame = cap.read()

        ## Put a timestamp on it
        # timestamp = datetime.datetime.now()
        # cv2.putText(frame, timestamp.strftime(
        # "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
        #         cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        outputFrame = frame.copy()

        # check if the output frame is available, otherwise skip
        # the iteration of the loop
        if outputFrame is None:
            continue

        # encode the frame in JPEG format
        ##(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        # ensure the frame was successfully encoded

        if not flag:
            continue

        yield frame


cv2.imshow("thing", generate())

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("streamPage.html", video_feed=generate())

app.run(host="localhost", port=8080, debug=True)

# from starlette.responses import StreamingResponse
# from imutils.video import VideoStream
# TODO: replace Flask with FastAPI for modern streaming features + async handlers
# from fastapi import FastAPI
import cv2
from util import CCAInputs, generate_cca_frame
from streamer import BaseStreamer
import threading
from flask import Flask, render_template, Response
import numpy as np
import time

outputFrame = None
lock = threading.Lock()
args = CCAInputs(
  num_states=5,
  width=400,
  height=400,
  threshold=3,
  range_value=3,
  hood='moore',
  hood_switch_prob=0.1,
  random_seed=5000
)

app = Flask(__name__)

class CCAStream(BaseStreamer):
    def __init__(self):
        super(CCAStream, self).__init__()

    @staticmethod
    def frames():
        states = np.random.randint(0, args.num_states, (args.width, args.height), dtype=int)
        start_time = time.time()
        x = 1 # displays the frame rate every 1 second
        counter = 0

        while True:
          states, img = generate_cca_frame(states, args)

          counter += 1
          if (time.time() - start_time) > x :
              print("FPS: ", counter / (time.time() - start_time))
              counter = 0
              start_time = time.time()
          yield cv2.imencode('.jpg', img)[1].tobytes()          


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(CCAStream()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

'''
TODO: switch over
FastAPI implementation references
'''
# def generate():
# 	# grab global references to the output frame and lock variables
# 	global outputFrame, lock
 
# 	# loop over frames from the output stream
# 	while True:
# 		# wait until the lock is acquired
# 		with lock:
# 			# check if the output frame is available, otherwise skip
# 			# the iteration of the loop
# 			if outputFrame is None:
# 				continue
 
# 			# encode the frame in JPEG format
# 			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
 
# 			# ensure the frame was successfully encoded
# 			if not flag:
# 				continue
 
# 		# yield the output frame in the byte format
# 		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
# 			bytearray(encodedImage) + b'\r\n')


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/view_cca")
# async def cca_viewer() -> Response:
#   response = StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")
#   await response

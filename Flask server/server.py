from flask import Flask, render_template, request, Response
from cv2 import cv2
import numpy as np
import RPi.GPIO as GPIO
import acts
import math
import time
from camera import VideoCamera

video_camera = VideoCamera()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
#         time_start = time.time()
        frame = video_camera.get_object()
#         time_finish = time.time()
#         fps = 1/(time_finish - time_start)
#         print("Time Start: {}\nTime Finish:{}".format(time_start,time_finish) +"\nFPS:" +  str(round(fps,2)))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def man_frame():
    while True:
#         time_start = time.time()
        frame = video_camera.get_frame()
#         time_finish = time.time()
#         fps = 1/(time_finish - time_start)
#         print("Time Start: {}\nTime Finish:{}".format(time_start,time_finish) +"\nFPS:" +  str(round(fps,2)))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/manuel')
def manuel():
    acts.stop()
    return render_template("manuel.html")

@app.route('/manuelcmd', methods=['POST','GET'])
def manuelcmd():
    if request.method == 'POST':
        comm = request.form.get('cmd') 
    #comm = request.form["cmd"]
        if comm == 'F':
            acts.forward()
            return "Forward!"

        elif comm == 'S':
            acts.stop()
            return "Stopped!"

        elif comm == 'B':
            acts.back()
            return "Backward!"

        elif comm == 'L':
            acts.left()
            return "Left!"

        elif comm == 'R':
            acts.right()
            return "Right!"
        
        elif comm == '1':
            acts.gear1()
            return "Speed: 25%!"

        elif comm == '2':
            acts.gear2()
            return "Speed: 50%!"
        
        elif comm == '3':
            acts.gear3()
            return "Speed: 75%!"
        
        elif comm == '4':
            acts.gear4()
            return "Speed: 100%!"
    else:
        return "You have not permission to access!"

@app.route('/video_manuel')
def video_manuel():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(man_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
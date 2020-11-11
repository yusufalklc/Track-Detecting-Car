import cv2
from threading import Thread
import imutils
import time
import numpy as np
import acts

last_comm = ""

class WebcamVideoStream:
    def __init__(self, src=0, name="WebcamVideoStream"):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3,320)
        self.stream.set(4,240)
        (self.grabbed, self.frame) = self.stream.read()
        self.name = name
        self.stopped = False
    
    def start(self):
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
        
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = WebcamVideoStream(src=0).start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_object(self):
        global last_comm
        frame = self.flip_if_needed(self.vs.read()).copy() 
        roi = frame[50:(100), 0:320]    # region of interest
        kernel = np.ones((3, 3), np.uint8)
        black = cv2.inRange(roi, (0, 0, 0), (180, 255, 25))
        black = cv2.erode(black, kernel, iterations=5)
        black = cv2.dilate(black, kernel, iterations=9)
        contours, hierarchy = cv2.findContours(black.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        if len(contours) > 0:
            x, y, w, h = cv2.boundingRect(contours[0])
        #    cv2.drawContours(vid, contours, -1, (0, 150, 150), 3)
            cv2.line(frame, (int(x + (w / 2)), 150),
                     (int(x + (w / 2)), (150 + 50)), (255, 0, 0), 3)
            cv2.line(frame, (int(x + (w / 2)), 150 + 25),
                     (160, 150 + 25), (0, 255, 255), 2, 4)
            if (x + w / 2) > 200:
                cv2.putText(frame, "Turn Right!", (x, y + 150 + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                last_comm = "Right"
                acts.right()
            if (x + w / 2) < 120:
                cv2.putText(frame, "Turn Left!", (x, y + 150 + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                last_comm = "Left"
                acts.left()
            if 130 < (x + w / 2) < 190:
                cv2.putText(frame, "Forward!", (x, y + 150 + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                acts.forward()
            else:
                if last_comm == "Right":
                    print("Last Command: Right")
                    acts.right()
                if last_comm == "Left":
                    print("Last Command: Left")
                    acts.left()
                    
        cv2.line(frame, (160, 250), (160, 300), (255, 255, 255), 3)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes())

    



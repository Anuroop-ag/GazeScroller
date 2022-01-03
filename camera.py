import cv2
import numpy as np
import dlib
import math 
import keyboard
from numpy.lib.twodim_base import eye
from pync.TerminalNotifier import notify
import pynput
import time
import pync
from pynput.mouse import Button, Controller
keyboard = pynput.keyboard.Controller()
from pynput.keyboard import Key

class VideoCamera(object) :
    def __init__(self):
        self.video = cv2.VideoCapture(0) 
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape68.dat")
        self.flag = 0
        self.initial_delta_eyes = 0.3
        self.initial_ratio = 0.3
        self.scrollon  = False
        self.nose_initial = 0
    def __del__(self):
        self.video.release()
    
    def midpoint(self,p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    def nose_movement(self,curr,direction) :
        mouse = Controller()
        mouse.scroll(0,direction * 5)

    def calculateRatio(self,points, marks) : 
        
        numerator = math.hypot(marks.part(points[1]).x - marks.part(points[5]).x,marks.part(points[1]).y - marks.part(points[5]).y) + math.hypot(marks.part(points[2]).x - marks.part(points[4]).x,marks.part(points[2]).y - marks.part(points[4]).y)
        denominator = 2 * math.hypot(marks.part(points[0]).x -  marks.part(points[3]).x , marks.part(points[0]).y - marks.part(points[3]).y)   
        ratio = numerator / denominator 
        return  ratio

    def initial_delta(self,eye_marks) : 
        righteye_left_point = (eye_marks.part(36).x, eye_marks.part(36).y)
        righteye_right_point = (eye_marks.part(39).x, eye_marks.part(39).y)
        righteye_center_top =  self.midpoint(eye_marks.part(37), eye_marks.part(38))
        righteye_center_bottom = self.midpoint(eye_marks.part(41), eye_marks.part(40))
        righteye_blink_dist = math.hypot(righteye_center_top[0]-righteye_center_bottom[0],righteye_center_top[1]-righteye_center_bottom[1])
        righteye_eye_width = math.hypot(righteye_left_point[0]-righteye_right_point[0],righteye_left_point[1]-righteye_center_bottom[1])
        
        eye_ratio = self.calculateRatio([36,37,38,39,40,41],eye_marks)

        # print(eye_ratio)
        right_ratio = (righteye_eye_width/righteye_blink_dist)
        self.nose_initial =  eye_marks.part(33).y - 30
        return right_ratio

    def get_winking(self,eye_marks,delta) : 
        righteye_left_point = (eye_marks.part(36).x, eye_marks.part(36).y)
        righteye_right_point = (eye_marks.part(39).x, eye_marks.part(39).y)
        righteye_center_top = self.midpoint(eye_marks.part(37), eye_marks.part(38))
        righteye_center_bottom = self.midpoint(eye_marks.part(41), eye_marks.part(40))
        righteye_blink_dist = math.hypot(righteye_center_top[0]-righteye_center_bottom[0],righteye_center_top[1]-righteye_center_bottom[1])
        righteye_eye_width = math.hypot(righteye_left_point[0]-righteye_right_point[0],righteye_left_point[1]-righteye_center_bottom[1])
        
        eye_ratio_right = self.calculateRatio([36,37,38,39,40,41],eye_marks)
        eye_ratio_left = self.calculateRatio([42,43,44,45,46,47],eye_marks)
        # print(eye_ratio_right , eye_ratio_left)
        
        #left Eye
        lefteye_left_point = (eye_marks.part(42).x, eye_marks.part(42).y)
        lefteye_right_point = (eye_marks.part(45).x, eye_marks.part(45).y)
        lefteye_center_top = self.midpoint(eye_marks.part(43), eye_marks.part(44))
        lefteye_center_bottom = self.midpoint(eye_marks.part(47), eye_marks.part(46))
        lefteye_blink_dist = math.hypot(lefteye_center_top[0]-lefteye_center_bottom[0],lefteye_center_top[1]-lefteye_center_bottom[1])
        lefteye_eye_width = math.hypot(lefteye_left_point[0]-lefteye_right_point[0],lefteye_left_point[1]-lefteye_center_bottom[1])
        
        right_ratio = (righteye_eye_width/righteye_blink_dist)
        left_ratio = lefteye_eye_width/lefteye_blink_dist
        curr_delta = right_ratio
        
    
        # print(curr_delta-delta,right_ratio-left_ratio)
        if curr_delta > delta + 0.3  and abs(right_ratio-left_ratio) > 0.5:
            # cv2.putText(frame,"Scroll Movement Activated",(50,150),cv2.FONT_ITALIC,3,(255,0,0))
            return True,curr_delta
        else :
            # cv2.putText(frame,"Scroll Movement Deactiacted",(50,150),cv2.FONT_ITALIC,3,(255,0,0))
            return False, delta




    def notify(self,check):
        if check :
            pync.notify("Scroll option is Enabled" )
        else : 
            pync.notify("Scroll option Disabled " )
        time.sleep(0.1)

    def get_frame(self) :
        ret,frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        for face in faces:
            landmarks = self.predictor(gray, face)
            if self.flag == 0 :
                self.initial_ratio = self.initial_delta(landmarks)
                self.flag = 1
            
            #mark eye pupil 
            center = self.midpoint(landmarks.part(43),landmarks.part(46))
            cv2.circle(frame, center, 10,(255, 0, 0), 2)
            
            #get_winks
            blinked,diff= self.get_winking(landmarks,self.initial_ratio)
            
            if blinked == True :
                self.scrollon = not self.scrollon
                self.notify(self.scrollon)
                cv2.putText(frame,"Works",(50,150),cv2.FONT_ITALIC,3,(255,0,0))
                keyboard.press(Key.space)
                keyboard.release(Key.space)

            #mark nose
            nose = (landmarks.part(33).x, landmarks.part(33).y)
            nose_center = (landmarks.part(33).x, landmarks.part(33).y-30)
            # cv2.circle(frame, nose_center, 4,(0, 255, 0), 5) 
            cv2.line(frame,(landmarks.part(36).x,landmarks.part(36).y),(landmarks.part(45).x,landmarks.part(45).y),(0,255,0),3)
            cv2.line(frame,(landmarks.part(27).x,landmarks.part(27).y-30),(landmarks.part(29).x,landmarks.part(29).y),(0,255,0),3)
            self.nose_movement(nose,+1)
            

            if self.scrollon == True : 
                cv2.putText(frame,"Scrolling is Enabled",(40,150),cv2.FONT_ITALIC,1,(255,0,0))
                test = str(nose[1]) 
                print(nose[1],self.nose_initial)
                if nose[1] <self.nose_initial -10 :
                    self.nose_movement(nose,-1)
                if nose[1] >self.nose_initial+10:
                    self.nose_movement(nose,+1)
            else :
                cv2.putText(frame,"Scrolling is Disabled",(40,150),cv2.FONT_ITALIC,1,(255,0,0))
             
        ret,jpeg = cv2.imencode('.jpg',frame)
        
        
        return jpeg.tobytes()



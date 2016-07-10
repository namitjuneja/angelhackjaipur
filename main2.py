import numpy as np
import cv2, time, requests, random

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def send_request(filename):
    tf = ["true", "false"]
    r = requests.get('http://172.16.22.196:9000/api/users/demography/' + random.choice(["male", "female"]) + '/' + random.choice(["child", "youth", "adult", "elderly"]) + '/' +filename+'/' + random.choice(tf) + '/' + random.choice(tf))
    print 'http://172.16.22.196:9000/api/users/demography/' + random.choice(["male", "female"]) + '/' + random.choice(["child", "youth", "adult", "elderly"]) + '/' +filename+'/' + random.choice(tf) + '/' + random.choice(tf)
    # http://localhost:9000/api/users/demography/:gender/:age
    print r
 
if __name__ == '__main__':

    hog = cv2.HOGDescriptor()#HOG
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )#HOG


    
            #ftw0 very slow
            #ftw slow and inaccurate

    cap = cv2.VideoCapture('ha.mp4')                        #video record code
    facedata = "haarcascade_frontalface_default.xml" #face detect haar casscade training data
    # facedata = "haarcascade_upperbody.xml" 
    cascade = cv2.CascadeClassifier(facedata)        #training the classififer

    ret, frame = cap.read()                          #read data from input stream
    print cap.get(3), cap.get(4), "<-dimensions"
    
    count = 0

    #while frames get retrieved successfuly
    while(ret):  

        count +=1
        img = frame

        #HOG START
        # found,w=hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
        # draw_detections(img,found)
        # cv2.imshow('feed',frame)
        #HOG END  

        

        minisize = (img.shape[1],img.shape[0])       #video code
        miniframe = cv2.resize(img, minisize)
 
        faces = cascade.detectMultiScale(miniframe)

        ex = ey = eh = ew = 0
        #print "faces_len, face[0]_len", type(faces), type(faces[0])
        img2 = img.copy()
        
        for f in faces:
        
            x, y, w, h = [ v for v in f ]
            
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
            text_color_blue = (255,0,0)
            text_color_yellow = (0,255,255)
            # cv2.putText(img, "Gender: Male", (x+w,y+15), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=2)
            cv2.putText(img, "Age: ADULT", (x+w,y+30-15), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color_blue, thickness=2)
            cv2.putText(img, "Height: 6 feet", (x+w,y+45-15), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color_blue, thickness=2)
            cv2.putText(img, "X:"+str(x), (x+w,y+60), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color_yellow, thickness=2)
            cv2.putText(img, "Y:"+str(y), (x+w,y+75), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color_yellow, thickness=2)
            

            sub_face = img2[y-10:y+h+10, x-10:x+w+10]
            face_file_name = "faces/face_" + str(y) + ".jpg"

            # print cv2.imwrite("tatti.png", sub_face)
            # print cv2.imwrite("big.png", img)
            
        
        print count
        if (count == 94 or count == 136 or count == 350 or count == 205 or count == 231 or count == 278 or count == 301 or count == 330 or count == 420 or count == 498 or count == 505 or count == 592 or count == 643 or count == 678 or count == 709 or count == 850 ):
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", count
            cv2.imshow("sb", sub_face)
            cv2.imwrite('/var/www/html/public/' + str((count/10)+1) + '.png', sub_face)
            send_request(str((count/10)+1) + '.png')
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()


    cap.release()
    cv2.destroyAllWindows()
    

    #while(True):
        #key = cv2.waitKey(20)
        #if key in [27, ord('Q'), ord('q')]:
            #break
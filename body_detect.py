import numpy as np
import cv2

cs = []

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
	global cs
	for x, y, w, h in rects:
		# the HOG detector returns slightly larger rectangles than the real objects.
		# so we slightly shrink the rectangles to get a nicer output.
		pad_w, pad_h = int(0.15*w), int(0.05*h)
		# cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

		cs.append(     (  ((x+w-pad_w)+(x+pad_w))/2,    ((y+h-pad_h)+(y+pad_h))/2   )        )

	for c in cs:
		overlay = img.copy()
		output = img.copy()

		cv2.circle(overlay, c,10,(0,255,255,200),-1)

		alpha = 0.05
		cv2.addWeighted(overlay, alpha, img, 1 - alpha,
		0, img)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    cap=cv2.VideoCapture('allah.mp4')
    # cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        draw_detections(frame,found)



        cv2.imshow('feed',frame)



        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cv2.destroyAllWindows()

import cv2
import pickle
import numpy as np
x = 0
y = 0
def updatedValues1():
    global x
    return x
def updatedValues2():
    global y
    return y
def management(video_file,pickle_file,threshold):
    cap = cv2.VideoCapture(video_file)
    if (cap.isOpened()== False):
	    print("Error opening video file")
    with open(pickle_file,'rb') as p:
        poslist = pickle.load(p)
    return gen_frames(cap,poslist,threshold,video_file)




def check(Fimg,img,poslist,threshold):
    Empty= 0
    vac=[]
    for i in range(3,len(poslist),4):
        mask = np.zeros(Fimg.shape[0:2], dtype=np.uint8)
        points = np.array([[[poslist[i-3][0],poslist[i-3][1]],[poslist[i-2][0],poslist[i-2][1]],[poslist[i-1][0],poslist[i-1][1]],[poslist[i][0],poslist[i][1]]]])
        #method 1 smooth region
        cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
        #method 2 not so smooth region
        # cv2.fillPoly(mask, points, (255))
        res = cv2.bitwise_and(Fimg,Fimg,mask = mask)
        rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
        cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
        ## crate the white background of the same size of original image
        wbg = np.ones_like(Fimg, np.uint8)*255
        cv2.bitwise_not(wbg,wbg, mask=mask)
        # overlap the resulted cropped image on the white background
                      
        number_of_white_pix= np.sum(cropped == 255)
        number_of_black_pix = np.sum(cropped == 0)
        total=number_of_white_pix+number_of_black_pix
        count=(number_of_white_pix/total)*100

        if count <threshold:
            color = (0, 255, 0)
            Empty+= 1
            vac.append(i//4)
        else:
            color = (0, 0, 255)
        pts = np.array([list(poslist[i-3]),list(poslist[i-2]),list(poslist[i-1]),list(poslist[i])],np.int32)
        pts = pts.reshape((-1, 1, 2))
        #cv2.rectangle(img, (poslist[i-1][0],poslist[i-1][1]), (poslist[i][0], poslist[i][1]), (255, 0, 255), 2)
        cv2.polylines(img, [pts], True, color,2)
        # cvzone.putTextRect(img, str(count), (poslist[i-3][0], poslist[i-1][1] - 3), scale=1,
        #                    thickness=2, offset=0, colorR=color)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale =0.9
    color = (100, 0, 255)
    thickness = 3
    # cv2.putText(img,  f'Vaccant: {Empty}/{len(poslist)//4}', (20, 30), font, 
    #                fontScale, color, thickness, cv2.LINE_AA)
    # cv2.putText(img, f'{vac}', (30, 1000), font, 
    #                fontScale, color, thickness, cv2.LINE_AA)
    return Empty

def gen_frames(cap,poslist,threshold,file):
    global x
    global y
    while(cap.isOpened()):
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        ret,img = cap.read()
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur_img = cv2.GaussianBlur(gray_img,(3,3),1)
        threshold_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY_INV, 25,16)
        median_img = cv2.medianBlur(threshold_img, 5)
        kernel = np.ones((3,3), np.int8)

        dilated_img = cv2.dilate(median_img, kernel , iterations=1)
            
        Empty = check(dilated_img,img,poslist,threshold)
        if file=='recording.mp4':
            x = Empty
        elif file=='CMR_bike.mp4':
            y = Empty

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'COntent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

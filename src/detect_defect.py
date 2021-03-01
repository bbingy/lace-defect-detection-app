# import torch
# import torch.nn as nn
import numpy as np
from cv2 import cv2 as cv2
import matplotlib.pyplot as plt
import random


def AreaMuSigma(img,R):
    img = np.array(img,dtype = float)
    h = np.ones((2*R+1,2*R+1))
    n = h.sum()
    c1 = cv2.filter2D(img**2, -1, h/n, borderType=cv2.BORDER_REFLECT)
    mean = cv2.filter2D(img, -1, h/n, borderType=cv2.BORDER_REFLECT)
    c2 = mean**2
    J = np.sqrt( np.maximum(c1-c2,0) )
    return mean,J

def KL(mu1,sigma1,mu2,sigma2):
    return np.log(sigma2/(sigma1+1e-5))+(sigma1**2+(mu1-mu2)**2)/(2*sigma2**2+1e-5)-0.5


def detect(viddir,frame_id, random_num):
    viddir = '/home/lby/lace-defect-detection-app/'+viddir
    print(viddir)
    print(frame_id)
    vidcap = cv2.VideoCapture(viddir)
    R = 5
    vidcap.set(cv2.CAP_PROP_POS_FRAMES,frame_id)
    #找一个队列用来判别有没有缺陷
    defect_center_queue=[]
    for i in range(4):
        defect_center_queue.append(np.array((0,0)))
    num = 0

    while vidcap.isOpened():
        cur_frame_num = vidcap.get(cv2.CAP_PROP_POS_FRAMES)
        ret,frame0 = vidcap.read()
        frame0_gray = cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)
        frame0_gray = frame0_gray[490:1080,90:1440]
        if(not ret):
            break
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,cur_frame_num+626)#or 626
        ret,frame1 = vidcap.read()
        frame1_gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        frame1_gray = frame1_gray[490:1080,90:1440]
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,cur_frame_num+1)
        
        Mu1,Sigma1 = AreaMuSigma(frame0_gray,R)
        Mu2,Sigma2 = AreaMuSigma(frame1_gray,R)
        
        KL_value = KL(Mu1,Sigma1,Mu2,Sigma2)
        KL_value = KL_value/np.max(KL_value)

        #后处理
        kl_max = np.max(KL_value)
        _,mask = cv2.threshold(KL_value,0.1*kl_max,1,cv2.THRESH_BINARY)
        mask = mask.astype(np.uint8)
        #甚至可以膨胀一下
        kernel = np.ones((10, 10), np.uint8)
        mask = cv2.dilate(mask, kernel)

        _,labels,status,centroids = cv2.connectedComponentsWithStats(mask)#labels,stats,centroids
        labels = labels.astype(np.uint8)

        status = np.delete(status,0,axis=0)
        max_idx=np.argmax(status[:,4],axis=0) + 1  #因为我把第一个删掉了

        labels[labels != max_idx] = 0
        labels[labels == max_idx] = 255

        max_centroids = centroids[max_idx - 1]
        if judgeDefect(max_centroids,defect_center_queue):

            #暂时不知道为什么会框歪,所以加一个delta修正一下
            delta = 30
            max_status = status[max_idx - 1]
            left = int(max_status[0] - max_status[2]/2 + 90)
            top = int(max_status[1] -max_status[3]/2 + 490 + delta)
            right = int(max_status[0] + max_status[2]/2 + 90)
            bottom = int(max_status[1] + max_status[3]/2 + 490 + delta)
            
            cv2.rectangle(frame0, (left,top), (right,bottom),(0, 255, 0), 2)

        if(num==10):
            # prepare for the front page
            mask_save_path = '/home/lby/lace-defect-detection-app/src/static/result_mask_'+random_num+'.png'
            origin_save_path = '/home/lby/lace-defect-detection-app/src/static/result_origin_'+random_num+'.png'
            cv2.imwrite(mask_save_path, KL_value*255)
            cv2.imwrite(origin_save_path, frame0[490:1080,90:1440])
            break
        
        #更新检测是否有缺陷列表
        defect_center_queue.append(max_centroids)
        defect_center_queue.pop(0)
        num += 1
        # break

    # random_num = str(random.random())
    # save_path = './static/result'+str(random_num)+'.png'
        # cv2.namedWindow("enhanced",0)
        # cv2.resizeWindow("enhanced", 640, 480)
        # cv2.imshow("enhanced",frame0)
        # k=cv2.waitKey(20)
        # if (k&0xff == ord('q')):
        #     break
    # save_path = './static/result.png'
    # cv2.imwrite(save_path, KL_value*255)
    # return save_path


#视频流处理速度瓶颈主要在videocapture.set/get，想想能不能实时性一些


def judgeDefect(newpoint,defect_center_queue):
    ex=1
    for i in range(len(defect_center_queue)):
        if abs(newpoint[0]-defect_center_queue[i][0])>ex:
            return False
    return True


if __name__ == "__main__":
    detect("/home/lby/lace-defect-detection-app/src/static/1.mp4", 600)
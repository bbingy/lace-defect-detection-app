import torch
import torch.nn as nn
import numpy as np
import cv2
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

def detect(viddir):
    vidcap = cv2.VideoCapture(viddir)
    R = 5
    vidcap.set(cv2.CAP_PROP_POS_FRAMES,1000)
    while(True):
        cur_frame_num = vidcap.get(cv2.CAP_PROP_POS_FRAMES)
        ret,frame0 = vidcap.read()
        frame0_gray = cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)
        frame0_gray = frame0_gray[490:1080,90:1440]
        if(not ret):
            break
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,cur_frame_num-640)
        ret,frame1 = vidcap.read()
        frame1_gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        frame1_gray = frame1_gray[490:1080,90:1440]
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,cur_frame_num+1)
        
        Mu1,Sigma1 = AreaMuSigma(frame0_gray,R)
        Mu2,Sigma2 = AreaMuSigma(frame1_gray,R)
        
        KL_value = KL(Mu1,Sigma1,Mu2,Sigma2)
        KL_value = KL_value/np.max(KL_value)
        break
    # random_num = str(random.random())
    # save_path = './static/result'+str(random_num)+'.png'
    save_path = './static/result.png'
    cv2.imwrite(save_path, KL_value*255)
    return save_path
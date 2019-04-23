# -*- coding: utf-8 -*-
"""
Created on Fri May  4 20:40:15 2018

@author: runze
"""

import os
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
path1 = '/media/runze/0C4317430C431743/418contra'
path2 = '/media/runze/0C4317430C431743/418contra_'

All = os.listdir(path1)
Image = []
Mask = []

for name in All:
    if 'mask' in name:
        Mask.append(name)
    else:
        Image.append(name)

L = []
R = []
for image in Image:
    if 'LEFT' in image:
        L.append(image)
    else:
        R.append(image)
assert len(L) == len(R)

def cut(image):
    img = cv2.imread(image)
    img = img[int(0.05 * img.shape[0]):int(0.95 * img.shape[0]),
          0:img.shape[1]]
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, imgray_2 = cv2.threshold(imgray, 30, 255, cv2.THRESH_BINARY)
    # plt.figure()
    # plt.imshow(imgray_2)
    # plt.show()
    contours, hierarchy = cv2.findContours(imgray_2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    areas = []
    for cont in contours:
        areas.append(cv2.contourArea(cont))
    i = areas.index(max(areas))

    x1,x2,y1,y2 = min(contours[i][:,:,0]),max(contours[i][:,:,0]),\
                  min(contours[i][:,:,1]),max(contours[i][:,:,1])

    return x1[0],x2[0],y1[0],y2[0]

os.chdir(path1)

for img_l in L:
    print('name:', img_l,
          'time:', time.strftime('%Y-%m-%d %H:%M:%S'))
    w1,w2,h1,h2 = cut(img_l)
    img_L = cv2.imread(img_l)
    img_L = img_L[h1:h2,w1:w2]
    try:
        mask_l = img_l.split('.png')[0][:-1]+'.mask.png'
        mask_L = cv2.imread(mask_l)
        mask_L = mask_L[h1:h2,w1:w2]
    except:
        pass
    img_r = img_l.split('.')[0]+'.RIGHT'+img_l.split('.')[1].split('LEFT')[1]+'.png'
    try:
        w1,w2,h1,h2 = cut(img_r)
        img_R = cv2.imread(img_r)
        img_R = img_R[h1:h2,w1:w2]
    except:
        with open('./exception.txt','a')as f:
            print(img_l)
    try:
        mask_r = img_r.split('.png')[0][:-1]+'.mask.png'
        mask_R = cv2.imread(mask_r)
        mask_R = mask_R[h1:h2,w1:w2]
    except:
        pass
    height_l, width_l = img_L.shape[0], img_L.shape[1]
    height_r, width_r = img_R.shape[0], img_R.shape[1]
    h, w = max(height_l,height_r), max(width_l, width_r)
    img_L = cv2.resize(img_L,(w,h))
    img_R = cv2.resize(img_R,(w,h))
    try:
        mask_L = cv2.resize(mask_L, (w, h))
        mask_R = cv2.resize(mask_R, (w, h))
    except:
        pass

    cv2.imwrite(os.path.join(path2,img_l),img_L)
    cv2.imwrite(os.path.join(path2,img_r),img_R)
    if mask_L is not None:
        cv2.imwrite(os.path.join(path2,mask_l),mask_L)
    if mask_R is not None:
        cv2.imwrite(os.path.join(path2,mask_r),mask_R)











# def DDSM_segment(path1, path2):
#     img_name = os.listdir(path1)
#     for name in img_name:
#         print('name:', name,
#               'time:', time.strftime('%Y-%m-%d %H:%M:%S'))
#         image = cv2.imread(os.path.join(path1,name))
#         img = image[int(0.05 * image.shape[0]):int(0.95 * image.shape[0]),
#               0:image.shape[1]]
#         imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         ret, imgray_2 = cv2.threshold(imgray, 30, 255, cv2.THRESH_BINARY)
#         image, contours, hierarchy = cv2.findContours(imgray_2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
#         areas = []
#         for cont in contours:
#             areas.append(cv2.contourArea(cont))
#         i = areas.index(max(areas))
#         poly_img = np.zeros(img.shape, dtype=np.uint8)
#         cv2.drawContours(poly_img, contours, i, (255, 255, 255), -1)
#
#         height1, height2, width1, width2 = box(poly_img)
#         #        print(image.shape)
#         #        print(height1, height2, width1, width2)
#         poly_img = poly_img[height1:height2, width1:width2] & img[height1:height2, width1:width2]
#         poly_img = cv2.resize(poly_img, (224, 224))
#         cv2.imwrite(path2 + '/' + name, poly_img)
#
#
# def box(poly_img):
#     poly_img = poly_img[:, :, 0]
#
#     x_num = count_255(poly_img)
#     for i in x_num:
#         if i != 0:
#             height1 = x_num.index(i)
#             break
#     x_num.reverse()
#     for i in x_num:
#         if i != 0:
#             height2 = len(x_num) - x_num.index(i) - 1
#             break
#     y_num = count_255(np.transpose(poly_img))
#     for i in y_num:
#         if i != 0:
#             width1 = y_num.index(i)
#             break
#     y_num.reverse()
#     for i in y_num:
#         if i != 0:
#             width2 = len(y_num) - y_num.index(i) - 1
#             break
#     return height1, height2, width1, width2
#
#
# def count_255(list):
#     num_255 = []
#     for i in list:
#         num = 0
#         for j in i:
#             if j == 255:
#                 num += 1
#         num_255.append(num)
#     return num_255
#
#
# # DDSM_segment(path_B, save_path_B)
# # DDSM_segment(paht_N, save_path_N)
# # DDSM_segment(path_C, save_path_C)
# DDSM_segment(path1, path2)

#

#####################################调试过程#####################################
# image = cv2.imread('test1.png')
# print(image)
# cv2.namedWindow('image', cv2.WINDOW_FREERATIO)
# cv2.imshow('image', image)
#
# img = image[int(0.1*image.shape[0]):int(0.9*image.shape[0]),
#              int(0.1*image.shape[1]):int(0.9*image.shape[1])]
# imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##创建窗口，参数2可调节窗口形状类别（此处自适应）
# cv2.namedWindow('imgray',cv2.WINDOW_FREERATIO)
##show图像（参数1为窗口名称）
# cv2.imshow('imgray', imgray)
##图像二值化，高于20置为255，低于40置为0
# ret, imgray_2 = cv2.threshold(imgray,30, 255, cv2.THRESH_BINARY)
# cv2.namedWindow('imgray_2', cv2.WINDOW_FREERATIO)
# cv2.imshow('imgray_2',imgray_2)
#
#
##opencv检测并绘制轮廓
# image, contours, hierarchy = cv2.findContours(imgray_2,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
#
##对所有contours求面积并返回最大面积索引
# areas = []
# for cont in contours:
#    areas.append(cv2.contourArea(cont))
# i = areas.index(max(areas))
#
##绘制边缘
##img_draw = cv2.drawContours(img, contours, i, (0,255,0), 3)
##cv2.namedWindow('img_draw',cv2.WINDOW_FREERATIO)
##cv2.imshow('img_draw', img)
#
# poly_img = np.zeros(img.shape, dtype = np.uint8)
# cv2.drawContours(poly_img, contours, i, (255,255,255),-1)
#
# poly_2 = poly_img[:,:,0]
# height_255num = []
# width_255num = []
##for i in poly_2:
##    num = 0
##    for j in i:
##        if j == 255:
##            num +=1
##    width_255num.append(num)
##print(max(width_255num))
#
# poly_2_transpose = np.transpose(poly_2)
# for i in poly_2_transpose:
#    num = 0
#    for j in i:
#        if j ==255:
#            num += 1
#    height_255num.append(num)
# height1 = int((poly_2.shape[0]-max(height_255num))*0.45)
# height2 = int(poly_2.shape[0]-((poly_2.shape[0]-max(height_255num))*0.45))
# width1 = min(height_255num.index(min(height_255num)),height_255num.index(max(height_255num)))
# width2 = max(height_255num.index(min(height_255num)),height_255num.index(max(height_255num)))
#
#
#
##print(poly_img)
##print(poly_img[:,:,0])
##poly_2 = poly_img[:,:,0]
##print(poly_2.shape)
##print(poly_2[0])
##print(poly_2[1])
##black_num = []
##for i in poly_2:
##    num = 0
##    for j in i:
##        if j == 0:
##            num +=1
##    black_num.append(num)
##print(black_num)
##hight = int(poly_img.shape[0])
##weith = int(1.01*(poly_img.shape[1]-min(black_num)))
##poly_img = poly_img[1:hight,1:weith]
##print(poly_img.shape)
##裁剪多余黑色背景
#
# poly_img = poly_img[height1:height2,width1:width2]
#
# cv2.namedWindow('poly_img', cv2.WINDOW_FREERATIO)
# cv2.imshow('poly_img',poly_img)
#
# poly_img = poly_img & img[height1:height2,width1:width2]
# cv2.namedWindow('poly_img',cv2.WINDOW_FREERATIO)
# cv2.imshow('poly_img', poly_img)
#
#
##避免图像一闪而过并在结束后释放窗口
# cv2.waitKey()
# cv2.destroyAllWindows()
#
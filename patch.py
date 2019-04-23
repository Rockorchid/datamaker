import os
import cv2
import time
import random
import matplotlib.pyplot as plt

pth1 = '/media/runze/0C4317430C431743/418contra_'
pth2 = '/media/runze/0C4317430C431743/422contra_patch'

L = []
M = []
R = []
for i in os.listdir(pth1):
    if 'LEFT' in i and 'mask' not in i:
        L.append(i)
    if 'mask' in i:
        M.append(i)
    if 'RIGHT' in i and 'mask' not in i:
        R.append(i)

def boundary(img_name):
    img = cv2.imread(img_name)
    # if 'mask' not in img_name:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
    # plt.figure()
    # plt.imshow(img,cmap='gray')
    # plt.show()
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    if 'mask' not in img_name:
        areas = []
        for cont in contours:
            areas.append(cv2.contourArea(cont))
        i = areas.index(max(areas))

        x1, x2, y1, y2 = min(contours[i][:, :, 0]), max(contours[i][:, :, 0]), \
                         min(contours[i][:, :, 1]), max(contours[i][:, :, 1])

        return (x1[0], x2[0], y1[0], y2[0], contours[i])
    else:
        mask_cont = []
        # w = 0
        # h = 0
        for cont in contours:
            x1, x2, y1, y2 = min(cont[:, :, 0]), max(cont[:, :, 0]), \
                             min(cont[:, :, 1]), max(cont[:, :, 1])
            # w_max = x2 - x1
            # h_max = y2 - y1
            # if w_max > w:
            #     w = w_max
            # if h_max > h:
            #     h = h_max
            mask_cont.append((x1[0], x2[0], y1[0], y2[0]))
        return mask_cont


def count(img_patch):
    img_patch = cv2.cvtColor(img_patch, cv2.COLOR_BGR2GRAY)
    ret, img_patch = cv2.threshold(img_patch, 30, 255, cv2.THRESH_BINARY)
    # plt.figure()
    # plt.imshow(img_patch,cmap='gray')
    # plt.show()
    num_0 = 0
    num_255 = 0
    for i in img_patch:
        for j in i:
            if j == 0:
                num_0 = num_0 + 1
            elif j == 255:
                num_255 = num_255 + 1
    assert num_0 + num_255 == img_patch.shape[0] * img_patch.shape[1]
    return num_255 / (num_0 + num_255)

def extract_patch(img_name, m_bounds, other_bound):

    patches = []
    img = cv2.imread(img_name)
    # plt.figure()
    # plt.imshow(img,cmap='gray')
    # plt.show()
    for m_bound in m_bounds:
        w = m_bound[1] - m_bound[0] - 1
        h = m_bound[3] - m_bound[2] - 1
        try:
            bound_x1 = m_bound[0] - w
            assert bound_x1 >= 0
        except:
            bound_x1 = 0
        bound_x2 = m_bound[1]
        try:
            assert bound_x1 < bound_x2
        except:
            with open('/home/runze/codes/datamaker/expection.txt', 'a') as f:
                print(img_name, 'bound_x1, bound_x2: {}'.format(bound_x1, bound_x2), file=f)
        try:
            bound_y1 = m_bound[2] - h
            assert bound_y1 >= 0
        except:
            bound_y1 = 0
        bound_y2 = m_bound[3]
        try:
            assert bound_y1 < bound_y2
        except:
            with open('/home/runze/codes/datamaker/expection.txt', 'a') as f:
                print(img_name, 'bound_y1, bound_y2: {}'.format(bound_y1, bound_y2), file=f)

        x = m_bound[0]
        y = m_bound[2]
        ratio = 0
        loopnum = 0
        while ratio < 0.8 or ((x >= bound_x1 and x <= bound_x2) and (y>= bound_y1 and y <= bound_y2)):
            x = random.randint(other_bound[0], other_bound[1] - w)
            range_y = []
            for m in other_bound[4]:
                for n in m:
                    if n[0] == x:
                        range_y.append(n[1])
            y_min, y_max = min(range_y), max(range_y)
            y = random.randint(y_min, y_max)
            img_patch = img[y:y+h, x:x+w]
            # plt.figure()
            # plt.imshow(img_patch)
            # plt.show()
            ratio = count(img_patch)
            loopnum = loopnum + 1
            print(loopnum)
            if loopnum >= 100:
                with open('/home/runze/codes/datamaker/expection.txt','a') as f:
                    print(img_name, file=f)
                break
        patches.append((x, y, w, h))
    return patches

os.chdir(pth1)

for mask in M:
    m_bounds = boundary(mask)
    print('{} contours numbers :'.format(mask), len(m_bounds),
          'time:', time.strftime('%Y-%m-%d %H:%M:%S'))
    for l in L:
        if mask.split('.mask')[0] in l:
            l_bound = boundary(l)
            patches = extract_patch(l, m_bounds, l_bound)
            img_l = cv2.imread(l)
            r = l.split('.')[0]+'.RIGHT'+l.split('.')[1].split('LEFT')[1]+'.png'
            img_r = cv2.imread(r)
            img_r = cv2.flip(img_r,1)
            i = 1
            j = 1
            for patch in patches:
                patch_l = img_l[patch[1]: patch[1] + patch[3], patch[0]: patch[0] + patch[2]]
                patch_r = img_r[patch[1]: patch[1] + patch[3], patch[0]: patch[0] + patch[2]]
                cv2.imwrite(pth2+'/'+l.split('.png')[0]+'_normal_patch_{}'.format(i)+'.png', patch_l)
                cv2.imwrite(pth2+'/'+r.split('.png')[0]+'_normal_patch_{}'.format(i)+'.png', patch_r)
                i = i + 1
            for m_bound in m_bounds:
                patch_l = img_l[m_bound[2]: m_bound[3], m_bound[0]: m_bound[1]]
                patch_r = img_r[m_bound[2]: m_bound[3], m_bound[0]: m_bound[1]]
                cv2.imwrite(pth2 + '/' + l.split('.png')[0] + '_abnormal_patch_{}_ill'.format(j) + '.png', patch_l)
                cv2.imwrite(pth2 + '/' + r.split('.png')[0] + '_abnormal_patch_{}_noill'.format(j) + '.png', patch_r)
                j = j + 1
            assert i == j

    for r in R:
        if mask.split('.mask')[0] in r:
            r_bound = boundary(r)
            patches = extract_patch(r, m_bounds, r_bound)
            img_r = cv2.imread(r)
            l = r.split('.')[0] + '.LEFT' + r.split('.')[1].split('RIGHT')[1] + '.png'
            img_l = cv2.imread(l)
            img_l = cv2.flip(img_l, 1)
            i = 1
            j = 1
            for patch in patches:
                patch_l = img_l[patch[1]: patch[1] + patch[3], patch[0]: patch[0] + patch[2]]
                patch_r = img_r[patch[1]: patch[1] + patch[3], patch[0]: patch[0] + patch[2]]
                cv2.imwrite(pth2+'/'+l.split('.png')[0]+'_normal_patch_{}'.format(i)+'.png', patch_l)
                cv2.imwrite(pth2+'/'+r.split('.png')[0]+'_normal_patch_{}'.format(i)+'.png', patch_r)
                i = i + 1
            for m_bound in m_bounds:
                patch_l = img_l[m_bound[2]: m_bound[3], m_bound[0]: m_bound[1]]
                patch_r = img_r[m_bound[2]: m_bound[3], m_bound[0]: m_bound[1]]
                cv2.imwrite(pth2 + '/' + l.split('.png')[0] + '_abnormal_patch_{}_noill'.format(j) + '.png', patch_l)
                cv2.imwrite(pth2 + '/' + r.split('.png')[0] + '_abnormal_patch_{}_ill'.format(j) + '.png', patch_r)
                j = j + 1
            assert i == j







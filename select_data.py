import os
import shutil
rootpth = 'E:/8bitFormatDDSM'
makepth = 'E:/418contra'
names = []
for i in os.listdir(rootpth):
    if 'normal' not in i:
        names.append(i)
names.remove('BCRP')
masspth = []
for name in names:
    for root, dirs, files in os.walk(os.path.join(rootpth,name)):
        # print('root: %s' % root)
        # print('dirs: %s' % dirs)
        # print('files: %s' % files)
        # print('')
        for file in files:
            if file.split('.')[-1] == 'OVERLAY':
                with open(os.path.join(root,file),'r') as f:
                    content = f.readlines()
                    for line in content:
                        if 'MASS' in line and root not in masspth:  #2572
                            masspth.append(root)
print(len(masspth))
print(masspth)

for pth in masspth:
    for file_ in os.listdir(pth):
        if file_.split('.')[-1] == 'png':
            print(pth,file_)
            new_name = pth.split('\\')[1]+'_'+pth.split('\\')[2]+'_'+file_
            shutil.copy(os.path.join(pth,file_),os.path.join(makepth,file_))
            os.rename(os.path.join(makepth,file_),os.path.join(makepth,new_name))


###########rename##################

# import os
#
# makepth = 'E:/418contra'
# name = os.listdir(makepth)
# j = 0
# k = 0
# for i in name:
#     if len(i.split('.')) == 3:
#         j = j+1
#         if 'LEFT_CC' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'L_CC.'+i.split('.')[-1]
#         elif 'LEFT_MLO' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'L_MLO.'+i.split('.')[-1]
#         elif 'RIGHT_CC' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'R_CC.'+i.split('.')[-1]
#         elif 'RIGHT_MLO' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'R_MLO.'+i.split('.')[-1]
#     elif len(i.split('.')) == 4:
#         k = k+1
#         if 'LEFT_CC' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'L_CC.'+i.split('.')[-2]+'.png'
#         elif 'LEFT_MLO' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'L_MLO.'+i.split('.')[-2]+'.png'
#         elif 'RIGHT_CC' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'R_CC.'+i.split('.')[-2]+'.png'
#         elif 'RIGHT_MLO' in i.split('.')[1]:
#             newname = i.split('.')[0]+'_'+'R_MLO.'+i.split('.')[-2]+'.png'
#     print(newname)
#     os.rename(os.path.join(makepth,i),os.path.join(makepth,newname))
# print(len(name))
# print(j)
# print(k)
#
#
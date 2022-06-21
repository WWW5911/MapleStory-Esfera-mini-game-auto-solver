from PIL import Image
import numpy as np
import random
import math
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime
import pyperclip
from PIL import ImageGrab

tmp_value = pyperclip.paste() 

def checkkk(strr):
    path = os.path.split(os.path.realpath(__file__))[0] + "/" + strr
    if not os.path.isdir(path):
        os.makedirs(path)
    return path    

def colorCheck(rgba, target, rangee):
    if abs(target[0] - rgba[0]) < rangee and abs(target[1] - rgba[1]) < rangee and abs(target[2] - rgba[2]) < rangee:
        return True
    return False

def Xcal(V, theta, t):
    return V * math.cos(theta * math.pi / 180) * t

def Ycal(V, theta, t):
    g = 1010 * 2
    return V * math.sin(theta * math.pi / 180) * t - (1/2 * g * t*t)






try:
    shutil.rmtree("tmp")
except:
    pass

checkkk("tmp")
open("tmp\此資料夾會被自動刪除", "w")
checkkk("result")

playerS = [255, 221, 68]
targetS = [255, 17, 17]


im = ImageGrab.grabclipboard()
im.save('tmp/0.png','PNG')
img = Image.open("tmp/0.png")
width, height = img.size

player = []
target = []
for y in range(height):
    for x in range(width):
        rgba = img.getpixel((x,y))
        if colorCheck(rgba, playerS, 5):
            player.append([x, y])
        
        if colorCheck(rgba, targetS, 5):
            target.append([x,y])

player = [np.average(np.array(player).T[0]), np.average(np.array(player).T[1])]
list.sort(target)
tmp = []
tmpp = []
tmpp.append(target[0])
for i in range(1, len(target)):
    tmpp.append(target[i])
    if math.dist(target[i-1], target[i]) > 10:
        tmp.append( [np.average(np.array(tmpp).T[0]), np.average(np.array(tmpp).T[1])] )
        tmpp = []
tmp.append( [np.average(np.array(tmpp).T[0]), np.average(np.array(tmpp).T[1])] )

target = tmp
V0X, V0Y = 1000, 1000


isEli = [ False for k in range(len(target))]

debug = True
ans = []
imglist = []
angle = -1

while angle <= 90:
    angle += 1
    flag = False
    place = []
    if debug :
        imggg = Image.open("tmp/0.png")
    for i in range(1000):
        place.append( [Xcal(V0X, angle, i/1000), Ycal(V0Y, angle, i/1000)] )
        
    for p in place:
        try:
            if int(p[0] + player[0]) > width:
                break
            if int(-p[1] + player[1]) < 0:
                continue
            

            bullet = [p[0] + player[0], -p[1] + player[1]]

            if debug:
                imggg.putpixel((int(p[0] + player[0]), int(-p[1] + player[1])), (255,255,255,99) )    

            for point in range(len(target)):
                if (not isEli[point]) and math.dist(bullet, target[point]) < 2:
                    print(angle)
                    ans.append(angle)
                    if os.path.isfile("tmp/angle= " + str(angle) + ".png"):
                        tag = 1
                        while os.path.isfile("tmp/angle= " + str(angle) + "-" + str(tag)+ ".png"):
                            tag += 1
                        imglist.append("tmp/angle= " + str(angle) + "-" + str(tag) + ".png")
                        imggg.save("tmp/angle= " + str(angle) + "-" + str(tag) + ".png")
                    else:
                        imglist.append("tmp/angle= " + str(angle) + ".png")
                        imggg.save("tmp/angle= " + str(angle) + ".png")
                    isEli[point] = True
                    
                    angle -= 1
                    flag = True
                    break
            if flag:
                break
        except:
            pass
    



plt.figure(figsize=(6,  (int((len(imglist)-1)/2)+1)*2.5  ))
for ind in range(len(imglist)):
    plt.subplot(int((len(imglist)-1)/2)+1, 2, ind+1)
    plt.axis('off')
    tttmp = mpimg.imread(imglist[ind])
    plt.imshow(tttmp)
    plt.title("angle = " + str(ans[ind]))

# plt.show()

now = datetime.now()

path = now.strftime("%Y-%m-%d")
if os.path.isfile("result/" + path + ".png"):
    tag = 1
    while os.path.isfile("result/" + path + "-" + str(tag) +  ".png"):
        tag += 1
    path = path + "-" + str(tag) 

plt.tight_layout()
plt.savefig( "result/" + path + ".png", dpi = 300, transparent = False, format = "png")


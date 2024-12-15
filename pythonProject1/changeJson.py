import json
import numpy as np
import os,cv2
#把json格式的标注转换为yolo格式
def json2yolo(path,cls_dict,types="bbox"):
    # 打开文件,r是读取,encoding是指定编码格式
    with open(path ,'r',encoding = 'utf-8') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        data = json.load(fp)
        h=data["imageHeight"]
        w=data["imageWidth"]
        shapes=data["shapes"]
        all_lines=""
        for shape in shapes:
            if True:
                #转成np数组，为了方便将绝对数值转换为相对数值
                points=np.array(shape["points"]) #把二维list强制转换np数组  shape为n,2
                #print(points)#[[x1,y1],[x2,y2]]
                if types=="bbox":
                    print(len(points))
                    x, y, wi, hi = cv2.boundingRect(points.reshape((-1,1,2)).astype(np.float32))
                    cx,cy=x+wi/2,y+hi/2
                    cx,cy,wi,hi=cx/w,cy/h,wi/w,hi/h
                    msg="%.2f %.2f %.2f %.2f"%(cx,cy,wi,hi)
                else:
                    points[:,0]=points[:,0]/w #n,2数组的第0列除以w
                    points[:,1]=points[:,1]/h #n,2数组的第1列除以h
                    #把np数组转换为yolo格式的str
                    points=points.reshape(-1)
                    points=list(points)
                    points=['%.4f'%x for x in points]#把float型的list转换为str型的list
                    msg=" ".join(points)
                l=shape['label'].lower()
                line=str(cls_dict[l])+" "+msg+"\n"
                all_lines+=line
    print(all_lines)
    filename=path.replace('json','txt')
    fh = open(filename, 'w', encoding='utf-8')
    fh.write(all_lines)
    fh.close()
#定义文件路径
path="D:/projectneed/xbis6550_240424_C75/test1"
path_list=os.listdir(path)
cls_dict={
    "plasticbottle": 0,
    "scissors": 1,
    "screwdriver": 2,
    "glasscan": 3,
    "metalcan": 4,
    "plasticcan": 5,
    "cuffs": 6,
    "jackknife": 7,
    "metalstick": 8,
    "fruitknife": 9,
    "wrench": 10,
    "glassbottle": 11,
    "dagger": 12,
    "grenade": 13,
    "cookknife": 14,
    "mousse": 15,
    "spray": 16,
    "utilityknife": 17,
    "jackknifeback": 18,
    "lighter": 19,
    "electronicshock": 20,
    "slingshot": 21,
    "lipolymer": 22,
    "hammer": 23,
    "lighterfluid": 24,
    "tongs": 25,
    "bullet": 26,
    "fireworks": 27,
    "firecrackers": 28,
    "zippo": 29,
    "battery": 30,
    "metalbottle": 31,
    "alcohol": 32,
    "gun": 33,
    "axe": 34,
    "saw": 35,
    "knuckles": 36,
    "knucklesyellow": 37,
    "mgigniter": 38,
    "umbrella": 39,
    "nunchakus": 40,
    "machete": 41,
    "knifeback": 42,
    "blade": 43,
    "sparklers": 44,
    "rifle": 45,
    "sight": 46,
    "rifleclip": 47,
    "laptop": 48,
    "slamcrackers": 49,
    "exploder": 50,
    "cannoncracker": 51,
    "plasticgun": 52,
    "pistolclip": 53,
    "annihilator": 54,
    "glasscement": 55,
    "sickle": 56,
    "ignitiongun": 57,
    "trowel": 58,
    "rubberhammer": 59,
    "blunderbuss": 60,
    "watch": 61,
    "hook": 62,
    "handgrenade": 63,
    "mortar": 64,
    "landmine": 65,
    "cannon": 66,
    "winebottle": 67,
    "shovel": 68,
    "spear": 69,
    "dart": 70,
    "shuriken": 71,
    "sword": 72,
    "crossbow": 73,
    "rake": 74
}
path_list2=[x for x in path_list if ".json" in x]
for p in path_list2:
    json2yolo(path+"/"+p,cls_dict)

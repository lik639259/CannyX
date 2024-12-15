import json
import cv2
import os

# 类别字典
class_dict = {
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

def load_labelme_data(image_dir, label_dir):
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_dir, filename)
            label_path = os.path.join(label_dir, filename.replace('.jpg', '.json').replace('.png', '.json'))
            
            # 加载图像
            image = cv2.imread(image_path)
            if image is None:
                print(f"无法加载图像: {image_path}")
                continue  # 跳过无法加载的图像
            
            height, width, _ = image.shape
            
            # 加载标签
            with open(label_path, 'r') as f:
                label_data = json.load(f)
                yolo_labels = []
                for shape in label_data['shapes']:
                    label = shape['label']
                    points = shape['points']
                    # 提取边界框坐标
                    x_min = min(point[0] for point in points)
                    y_min = min(point[1] for point in points)
                    x_max = max(point[0] for point in points)
                    y_max = max(point[1] for point in points)
                    
                    # 计算中心点和宽高
                    x_center = (x_min + x_max) / 2 / width
                    y_center = (y_min + y_max) / 2 / height
                    bbox_width = (x_max - x_min) / width
                    bbox_height = (y_max - y_min) / height
                    
                    # 获取类别索引
                    class_index = class_dict.get(label, -1)
                    if class_index != -1:
                        yolo_labels.append(f"{class_index} {x_center} {y_center} {bbox_width} {bbox_height}")
                
                # 保存 YOLO 格式的标签
                yolo_label_path = os.path.join(r'C:\Users\Desktop\xbis6550_240424_C75\labels', filename.replace('.jpg', '.txt').replace('.png', '.txt'))
                with open(yolo_label_path, 'w') as label_file:
                    label_file.write("\n".join(yolo_labels))

# 使用示例
image_dir = r'C:\Users\Desktop\xbis6550_240424_C75\pic'
label_dir = r'C:\Users\Desktop\xbis6550_240424_C75\json'
load_labelme_data(image_dir, label_dir)
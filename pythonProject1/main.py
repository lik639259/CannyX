import cv2
import utlis  # 引入自定义的工具模块

webcam = True  # 如果使用摄像头，设置为True
cap = cv2.VideoCapture(0)  # 初始化摄像头对象
# 设置 IP 地址和端口号
# ip_address = '10.69.170.190:8080'  # 例如 '192.168.1.100:8080'
#
# # 初始化摄像头对象
# cap = cv2.VideoCapture(f'http://{ip_address}/video')
cap.set(10, 120)  # 设置亮度为120
cap.set(3, 1920)  # 设置摄像头帧宽度为1920
cap.set(4, 1080)  # 设置摄像头帧高度为1080
scale = 3  # 缩放比例
wP = 210 * scale  # 目标宽度
hP = 297 * scale  # 目标高度

while True:
    # 从摄像头获取图像
    # if webcam: success, img = cap.read()  # 从摄像头读取帧
    # else: img = cv2.imread('d:\ilearnopencv\1.jpg')  # 从文件中读取图像
    img = cv2.imread('d:\\ilearnopencv\\12-150.jpg')  # 从文件中读取图像
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)  # 调整图像大小为原来的一半
    imgContours, conts = utlis.getContours(img, minArea=50000, filter=4)  # 获取图像的轮廓信息
    if len(conts) != 0:
        biggest = conts[0][2]  # 获取最大的轮廓
        imgWarp = utlis.warpImg(img, biggest, wP, hP)  # 透视变换图像
        imgContours2, conts2 = utlis.getContours(imgWarp, minArea=20000, filter=4, cThr=[50, 50])  # 获取透视变换后图像的轮廓信息
        if len(conts) != 0:
            for obj in conts2:
                cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)  # 绘制轮廓线
                nPoints = utlis.reorder(obj[2])  # 重新排序轮廓的顶点
                nW = round((utlis.findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10), 1)  # 计算宽度
                nH = round((utlis.findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10), 1)  # 计算高度
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]), (255, 0, 255), 3, 8, 0, 0.05)  # 绘制宽度箭头
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]), (255, 0, 255), 3, 8, 0, 0.05)  # 绘制高度箭头
                x, y, w, h = obj[3]  # 获取轮廓的边界框
                cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)  # 在图像上绘制宽度文本
                cv2.putText(imgContours2, ' {}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)  # 在图像上绘制高度文本
        cv2.imshow('Result', imgContours2)  # 显示处理后的图像
    cv2.imshow('Original', img)  # 显示原始图像
    cv2.waitKey(1)  # 等待按键事件


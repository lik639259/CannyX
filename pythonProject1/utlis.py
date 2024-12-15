import cv2
import numpy as np

def getContours(img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
    # 将图像转换为灰度图
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 对灰度图进行高斯模糊处理
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # 使用 Canny 边缘检测
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    # 对边缘图像进行膨胀
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    # 对膨胀后的图像进行腐蚀
    imgThre = cv2.erode(imgDial, kernel, iterations=2)
    # 如果需要显示 Canny 边缘检测结果，则显示
    if showCanny:
        cv2.imshow('Canny', imgThre)
    # 寻找图像中的轮廓
    contours, hierarchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []
    for i in contours:
        # 计算轮廓的面积
        area = cv2.contourArea(i)
        if area > minArea:
            # 计算轮廓的周长
            peri = cv2.arcLength(i, True)
            # 近似轮廓
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # 获取轮廓的边界框
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
                else:
                    finalContours.append([len(approx), area, approx, bbox, i])
    # 按照轮廓面积大小进行排序
    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)
    # 如果需要在图像上绘制轮廓，则进行绘制
    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)
    # 返回绘制了轮廓的图像以及轮廓信息列表
    return img, finalContours

def reorder(myPoints):
    # 从轮廓的顶点坐标中选择前四个点
    myPoints = myPoints[0:4]
    print("Original Points Shape:", myPoints.shape)
    print("Original Points:", myPoints)
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4, 2))
    print("Reshaped Points Shape:", myPoints.shape)
    print("Reshaped Points:", myPoints)
    # 计算轮廓的顶点坐标之和
    add = myPoints.sum(1)
    # 找到和最小的点作为新的顶点坐标的第一个点，找到和最大的点作为新的顶点坐标的第四个点
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    # 计算轮廓的顶点坐标之间的差异
    diff = np.diff(myPoints, axis=1)
    # 找到差异最小的点作为新的顶点坐标的第二个点，找到差异最大的点作为新的顶点坐标的第三个点
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    print("Reordered Points:", myPointsNew)
    # 返回重新排序后的轮廓顶点坐标
    return myPointsNew

def warpImg(img, points, w, h, pad=20):
    # 提取四个顶点
    points = points[0:4]
    # 重新排序顶点
    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    imgWarp = imgWarp[pad:imgWarp.shape[0] - pad, pad:imgWarp.shape[1] - pad]
    return imgWarp

def findDis(pts1, pts2):
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5

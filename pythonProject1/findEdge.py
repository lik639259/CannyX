import cv2
import math

# 读取图像
image = cv2.imread('ilearnopencv\\15.png')

# 灰度化
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 寻找轮廓
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 假设整个背景的实际大小
real_width = 40  # 假设单位为厘米
real_height = 40  # 假设单位为厘米

# 图像宽度和高度
image_width, image_height = image.shape[1], image.shape[0]

# 比例因子
scale_factor_x = real_width / image_width
scale_factor_y = real_height / image_height

# 遍历轮廓
for contour in contours:
    # 计算轮廓的面积
    area = cv2.contourArea(contour)
    # 根据面积进行筛选
    if area > 1000:  # 设置面积阈值
        # 获取轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        # 在图像上绘制原始轮廓
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        # 在图像上绘制扩大后的长方形
        cv2.rectangle(image, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)

        # 计算实际长、宽和对角线长度
        scaled_w = w * scale_factor_x
        scaled_h = h * scale_factor_y
        diagonal_length = math.sqrt((scaled_w ** 2) + (scaled_h ** 2))

        # 绘制长、宽和对角线长度
        cv2.putText(image, f'Width: {scaled_w:.2f} cm', (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(image, f'Height: {scaled_h:.2f} cm', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(image, f'Diagonal: {diagonal_length:.2f} cm', (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1)

# 缩小图像
# scaled_image = cv2.resize(image, None, fx=0.5, fy=0.5)

# 显示结果
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()




def calculate_real_size(data, pixel_to_mm):
    for item in data:
        top_image = item['top_image']
        side_image = item['side_image']
        labels = item['labels']

        # 假设从 JSON 中提取的边界框格式为 [x1, y1, x2, y2]
        top_bbox = labels['shapes'][0]['points']  # 取第一个物体的边界框
        side_bbox = labels['shapes'][1]['points']  # 取第二个物体的边界框

        # 计算顶部视角的宽度和高度
        top_x1, top_y1 = top_bbox[0]
        top_x2, top_y2 = top_bbox[1]
        top_width_pixels = abs(top_x2 - top_x1)
        top_height_pixels = abs(top_y2 - top_y1)

        # 计算侧面视角的深度
        side_x1, side_y1 = side_bbox[0]
        side_x2, side_y2 = side_bbox[1]
        side_depth_pixels = abs(side_x2 - side_x1)

        # 计算真实尺寸
        real_width = top_width_pixels * pixel_to_mm
        real_height = top_height_pixels * pixel_to_mm
        real_depth = side_depth_pixels * pixel_to_mm

        print(f'Object: {item["object"]}, Real Width: {real_width:.2f} mm, Real Height: {real_height:.2f} mm, Real Depth: {real_depth:.2f} mm')

# 使用示例
pixel_to_mm = 0.5  # 假设每个像素对应 0.5 mm
calculate_real_size(data, pixel_to_mm)
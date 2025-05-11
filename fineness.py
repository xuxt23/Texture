'''
用seedfilling算法进行连通域分析的python代码,读取路径为“filename”的二值化图片
输出为: 
1. 连通域个数除以图片总面积,命名为Fineness 
2. 连通域标记后的图片,存储路径为outpath

'''

import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import deque
from PIL import Image
import numpy as np
import imageio.v2 as imageio



def seed_filling(image, output_path):
    """
    使用种子填充算法进行连通域分析
    
    参数:
    image: 二值化图像（0表示背景，255表示前景）
    output_path: 标记后图像的输出路径
    
    返回:
    fineness: 连通域个数 / 图片总面积
    labeled_image: 标记后的图像
    """
    # 确保图像是二值的（0和255）
    maxvalue = np.max(image)
    if maxvalue != 255:
        image = image * 255 / maxvalue
    
    # 创建访问标记数组
    height, width = image.shape
    visited = np.zeros((height, width), dtype=bool)
    
    # 创建标记图像（彩色）
    labeled_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 定义移动方向（8连通）
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]
    
    # 为不同连通域分配不同的颜色
    colors = []
    for i in range(1, 1000):  # 预先生成1000种颜色
        # 生成足够明亮且彼此差异较大的颜色
        color = np.random.randint(50, 256, size=3)
        colors.append((int(color[0]), int(color[1]), int(color[2])))
    
    region_count = 0
    total_pixels = height * width
    object_pixels = np.sum(image == 255)
    
    # 遍历图像
    for y in range(height):
        for x in range(width):
            # 如果是前景像素且未访问过
            if image[y, x] == 255 and not visited[y, x]:
                region_count += 1
                color = colors[region_count % len(colors)]
                
                # 使用BFS进行种子填充
                queue = deque([(y, x)])
                visited[y, x] = True
                
                while queue:
                    cy, cx = queue.popleft()
                    labeled_image[cy, cx] = color  # 标记像素
                    
                    # 检查8个方向的邻居
                    for i in range(8):
                        ny, nx = cy + dy[i], cx + dx[i]
                        
                        # 检查边界
                        if 0 <= ny < height and 0 <= nx < width:
                            # 如果是前景像素且未访问过
                            if image[ny, nx] == 255 and not visited[ny, nx]:
                                visited[ny, nx] = True
                                queue.append((ny, nx))
    
    # 计算Fineness
    if object_pixels > 0:
        fineness = region_count / total_pixels
    else:
        fineness = 0
    
    # 保存标记后的图像
    cv2.imwrite(output_path, labeled_image)
    
    return fineness, labeled_image

def main(filename, outpath):
    """
    主函数，读取二值化图像并进行连通域分析
    
    参数:
    filename: 输入图像路径
    outpath: 输出图像路径
    """

    # 读取图像
    image = imageio.imread(filename)

    print(f"图像形状: {image.shape}")
    print(f"像素值范围: {np.min(image)} - {np.max(image)}")     
    
    if image is None:
        print(f"无法读取图像: {filename}")
        return
    
    # 确保图像是二值的
    # _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    binary_image = image
    
    # 进行连通域分析
    fineness, labeled_image = seed_filling(binary_image, outpath)
    
    print(f"连通域个数: {int(fineness * binary_image.shape[0] * binary_image.shape[1])}")
    print(f"图像总面积: {binary_image.shape[0] * binary_image.shape[1]}")
    print(f"Fineness: {fineness:.6f}")
    print(f"标记后的图像已保存至: {outpath}")
    
    '''
    # 显示原图和标记后的图像
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('原始二值图像')
    plt.imshow(binary_image, cmap='gray')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.title(f'连通域标记 (Fineness={fineness:.6f})')
    plt.imshow(cv2.cvtColor(labeled_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
  
    '''


import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

resize_ratio = 1

search_N = 7    # 搜索邻域半径

show = False

area_min = 0

area_ratio = 0.85

# 180，255，255
low_hsv = np.array([100, 88, 100])
high_hsv = np.array([123, 255, 255])

# 对向量中每一个点，判断其值与邻域点值的大小，若大部分邻域点均大于其值，则为峰谷点
# 得到两个峰谷点的索引，比较大小
def find_min(x_vector):
    min_idx = []
    for idx in range(search_N,len(x_vector) - search_N):
        x_cur = x_vector[idx]
        greater_cnt_l = 0
        greater_cnt_r = 0
        for j1 in range(-search_N, 0):
            greater_cnt_l += int(x_vector[idx + j1] > x_cur)
        for j2 in range(1, search_N + 1):
            greater_cnt_r += int(x_vector[idx + j2] > x_cur)
        # print(greater_cnt)
        if (((greater_cnt_l > search_N-2) and (greater_cnt_r > search_N-2))):
            min_idx.append(x_vector[idx])
    if (min_idx != []):
        if (min_idx[0]>min_idx[-1]):
            print("FIND:    left")
            return -1
        if (min_idx[0]<min_idx[-1]):
            print("FIND:    right")
            return 1
        else:
            return 0
    return 0


def find_blue(input_img,low_hsv,high_hsv):

    hsv_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2HSV)
    img_blue = cv2.inRange(hsv_img, low_hsv, high_hsv)


# 检测有无标志
# 先检测椭圆，椭圆面积
def sign_detector(input_img, if_show):

    img = cv2.resize(input_img, (int(input_img.shape[1]*resize_ratio), int(input_img.shape[0]*resize_ratio)), interpolation = cv2.INTER_AREA)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 180，255，255

    img_blue = cv2.inRange(hsv_img, low_hsv, high_hsv)

    contours, hierarchy = cv2.findContours(img_blue,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#contours为轮廓集，可以计算轮廓的长度、面积等
    if (contours == []):
        # 没有轮廓返回
        print("no CONTOURS!")
        if (if_show):
            cv2.imshow("image", img)
        return 0
    else:
        # 找最大椭圆为标志
        S1_max = 0
        for cnt in contours:
            if len(cnt)>50:     # 可能是椭圆
                S1 = cv2.contourArea(cnt)
                ell = cv2.fitEllipse(cnt)
                # 拟合椭圆的面积
                S2 = (0.25) * math.pi * ell[1][0] * ell[1][1]     # 外接最小矩形 质心（圆心），边长，角度
                if (((S1/S2) > area_ratio) and (S1 > area_min) and (S1 > S1_max)):          # 确定是圆形，标志面积比例，可以更改，根据数据集。。。
                    S1_max = S1
                    (bb_x, bb_y, bb_w, bb_h) = cv2.boundingRect(cnt)    #  获取外接矩形
                    
                    if (if_show):
                        img = cv2.ellipse(img, ell, (0, 255, 0), 2)
                        img = cv2.circle(img, (int(ell[0][0]),int(ell[0][1])), 2, (0, 0, 255), 2)
                    
                    
    if S1_max != 0:
        img_mask = np.zeros_like(img_blue)
        img_mask[bb_y:bb_y+bb_h,bb_x:bb_x+bb_w] = 255
        img_res = cv2.bitwise_and(img_mask,img_blue)
        # 统计水平方向的像素个数
        sum_for_x = np.sum(img_res, 0)

        result = find_min(sum_for_x)    # -1 left;  1 right
        if (if_show):
            cv2.imshow("image", img)

        return result

    else:    
        if (if_show):
            cv2.imshow("image", img)
        print("sign NOT found!")
        return 0



# # 如果图片中有标志，则进行判断    
# def sign_read(input_img):            

#     img = cv2.resize(input_img, (int(input_img.shape[1]*resize_ratio), int(input_img.shape[0]*resize_ratio)), interpolation = cv2.INTER_AREA)

#     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # 180，255，255
#     low_hsv = np.array([100, 88, 0])
#     high_hsv = np.array([130, 255, 255])

#     img_blue = cv2.inRange(hsv_img, low_hsv, high_hsv)

#     contours, hierarchy = cv2.findContours(img_blue,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#contours为轮廓集，可以计算轮廓的长度、面积等

#     # 找椭圆
#     for cnt in contours:
#         if len(cnt)>50:
#             # 围合区域的面积
#             S1 = cv2.contourArea(cnt)
#             # bounding box
#             ell = cv2.fitEllipse(cnt)
#             # 拟合椭圆的面积
#             S2 = (0.25) * math.pi * ell[1][0] * ell[1][1]     # 外接最小矩形 质心（圆心），边长，角度
#             if (S1/S2) > 0.85 :#面积比例，可以更改，根据数据集。。。
#                 (bb_x, bb_y, bb_w, bb_h) = cv2.boundingRect(cnt)

#     img_mask = np.zeros_like(img_blue)
#     img_mask[bb_y:bb_y+bb_h,bb_x:bb_x+bb_w] = 255
#     img_res = cv2.bitwise_and(img_mask,img_blue)
#     # 统计水平方向的像素个数
#     sum_for_x = np.sum(img_res, 0)

#     result = find_min(sum_for_x)    # -1 left;  1 right

#     return result

if __name__ == "__main__":
    #加载图像img
    img = cv2.imread('./images/signs/signs/IMG_3134 Medium.jpeg',cv2.IMREAD_COLOR)
    # sign_read(img)
    sign_detector(img,0)
   
    














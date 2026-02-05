import cv2
import numpy as np
import json

# capture = cv2.VideoCapture(1) # capture - захват

# Дефолтное цветовое пространство
# Red Green Blue
# Пиксель - список из 3 чисел GBR [0, 255, 120]
# Чб пиксель - число от 0 до 255 (интенсивность)
# HSV - Hue Saturation Value, Цвет (тон) Насыщенность Яркость

def nothing(x):
    pass

cv2.namedWindow("HSV_Trackbar")

hsv_filter_dict = {
    "low":[0, 0, 0],
    "high":[255, 255, 255],
}

try:
    with open("hsv_filter.json", "r") as f:
        hsv_filter_dict = json.loads(f.read())
        print(hsv_filter_dict)
except Exception as e:
    print(e)

    
cv2.createTrackbar("hue_low","HSV_Trackbar", hsv_filter_dict['low'][0], 255, nothing) # Цвет нижний диапазон h - hue, l - low
cv2.createTrackbar("hue_high","HSV_Trackbar", hsv_filter_dict['high'][0], 255, nothing)
cv2.createTrackbar("saturation_low","HSV_Trackbar", hsv_filter_dict['low'][1], 255, nothing) 
cv2.createTrackbar("saturation_high","HSV_Trackbar", hsv_filter_dict['high'][1], 255, nothing)
cv2.createTrackbar("value_low","HSV_Trackbar", hsv_filter_dict['low'][2], 255, nothing) 
cv2.createTrackbar("value_high","HSV_Trackbar", hsv_filter_dict['high'][2], 255, nothing)




'''img_black = []
zero_list_100 = [0 for i in range(100)]
for i in range(100):
    img_black.append(zero_list_100)

img_black = np.array(img_black, dtype=np.uint8)
print(img_black)'''
while True:
    hue_low = cv2.getTrackbarPos("hue_low", "HSV_Trackbar")
    hue_high = cv2.getTrackbarPos("hue_high", "HSV_Trackbar")
    saturation_low = cv2.getTrackbarPos("saturation_low", "HSV_Trackbar")
    saturation_high = cv2.getTrackbarPos("saturation_high", "HSV_Trackbar")
    value_low = cv2.getTrackbarPos("value_low", "HSV_Trackbar")
    value_high = cv2.getTrackbarPos("value_high", "HSV_Trackbar")
    
    img = cv2.imread("img.jpg") # ret(bool) есть кадр или нет, img - изображение
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    
    
    key = cv2.waitKey(1) # Ждать 1 мс нажатия клавиши
    

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_int = [hue_low, saturation_low, value_low]
    higher_int = [hue_high, saturation_high, value_high]

    lower = np.array(lower_int, dtype=np.uint8)
    higher = np.array(higher_int, dtype=np.uint8)


    
    mask = cv2.inRange(img, lower, higher) # Маска

    n, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    # 0 — фон, компоненты начинаются с 1
    for i in range(1, n):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        cx, cy = centroids[i]
        if area >= 1000:
            cv2.rectangle(img, (x, y), (x + w, y + h), [0, 255, 0], 2)
            cv2.putText(img, f"{area}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)                   



    cv2.imshow("camera", img)
    cv2.imshow("Mask", mask)

    # cv2.imshow("HSV", img_hsv)

    # cv2.imshow("black", img_black)

    if key == ord("s"):
        with open("hsv_filter.json", "w") as f:
            hsv_filter_dict = {
                "low":lower_int,
                "high":higher_int,
            }
            hsv_filter_json = json.dumps(hsv_filter_dict)
            f.write(hsv_filter_json)
            print("HSV фильтр сохранён")
    if key == 27 or key == ord(" "):
        break
    

# capture.release()
cv2.destroyAllWindows()


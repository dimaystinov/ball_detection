import cv2
import numpy as np
import json
import os
import sys

# Папка с exe (или со скриптом при запуске из IDE)
def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

PATH_HSV_JSON = os.path.join(BASE_DIR, "hsv_filter.json")
PATH_CONF_JSON = os.path.join(BASE_DIR, "conf.json")
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
    with open(PATH_HSV_JSON, "r") as f:
        hsv_filter_dict = json.loads(f.read())
        print("hsv_filter_dict", hsv_filter_dict)
except Exception as e:
    print(e)

conf_dict = {
    "resize_coef": 0.5, 
    "file_name": "img.jpg",
    "file_type": "img",       # video
    "time_sleep": 200
    }

try:
    with open(PATH_CONF_JSON, "r") as f:
        conf_dict = json.loads(f.read())
        print("conf_dict", conf_dict)
except Exception as e:
    print(e)

PATH_IMG = os.path.join(BASE_DIR, conf_dict["file_name"])


    
cv2.createTrackbar("hue_low","HSV_Trackbar", hsv_filter_dict['low'][0], 255, nothing) # Цвет нижний диапазон h - hue, l - low
cv2.createTrackbar("hue_high","HSV_Trackbar", hsv_filter_dict['high'][0], 255, nothing)
cv2.createTrackbar("saturation_low","HSV_Trackbar", hsv_filter_dict['low'][1], 255, nothing) 
cv2.createTrackbar("saturation_high","HSV_Trackbar", hsv_filter_dict['high'][1], 255, nothing)
cv2.createTrackbar("value_low","HSV_Trackbar", hsv_filter_dict['low'][2], 255, nothing) 
cv2.createTrackbar("value_high","HSV_Trackbar", hsv_filter_dict['high'][2], 255, nothing)
cv2.createTrackbar("area_min","HSV_Trackbar", hsv_filter_dict['area'][0], 1000, nothing)
cv2.createTrackbar("area_max","HSV_Trackbar", hsv_filter_dict['area'][1], 100000, nothing)


if conf_dict["file_type"] == "video":
    cap = cv2.VideoCapture(conf_dict["file_name"])  # cap - сокр от capture (захват) захват видео
    width = int(cap.get(3))
    height = int(cap.get(4))
    new_width = int(width * conf_dict["resize_coef"])
    new_height = int(height * conf_dict["resize_coef"])
    fps = cap.get(cv2.CAP_PROP_FPS) // 3 # Или cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Лучше MJPG для AVI, без ошибок
    out = cv2.VideoWriter('output.avi', fourcc, fps, (new_width, new_height))


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
    area_min = cv2.getTrackbarPos("area_min", "HSV_Trackbar")
    area_max = cv2.getTrackbarPos("area_max", "HSV_Trackbar")
    
    if conf_dict["file_type"] == "img":
        img = cv2.imread(PATH_IMG)  # ret(bool) есть кадр или нет, img - изображение
    elif conf_dict["file_type"] == "video":
        ret, img = cap.read()
        if ret == False:
            print("Error")
            break

    img = cv2.resize(img, None, fx=conf_dict["resize_coef"], fy=conf_dict["resize_coef"])
    
    
    key = cv2.waitKey(conf_dict["time_sleep"]) # Ждать 1 мс нажатия клавиши
    

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_int = [hue_low, saturation_low, value_low]
    higher_int = [hue_high, saturation_high, value_high]

    lower = np.array(lower_int, dtype=np.uint8)
    higher = np.array(higher_int, dtype=np.uint8)


    
    mask = cv2.inRange(img_hsv, lower, higher)  # Маска по HSV

    n, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    # 0 — фон, компоненты начинаются с 1
    for i in range(1, n):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        cx, cy = centroids[i]
        if area >= area_min:
            cv2.rectangle(img, (x, y), (x + w, y + h), [0, 255, 0], 2)
            cv2.putText(img, f"{int(area), int((w + h) / 2)}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)                   



    cv2.imshow("camera", img)
    cv2.imshow("Mask", mask)
    if conf_dict["file_type"] == "video":
        out.write(img)

    # cv2.imshow("HSV", img_hsv)

    # cv2.imshow("black", img_black)

    if key == ord("s"):
        with open(PATH_HSV_JSON, "w") as f:
            hsv_filter_dict["low"] = lower_int
            hsv_filter_dict["high"] = higher_int
            hsv_filter_dict["area"] = [area_min, area_max]

            hsv_filter_json = json.dumps(hsv_filter_dict)
            f.write(hsv_filter_json)
            print("HSV фильтр сохранён")
    if key == 27 or key == ord(" "):
        break
    

if conf_dict["file_type"] == "video":
    cap.release()
    out.release()
cv2.destroyAllWindows()


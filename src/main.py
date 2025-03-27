import cv2
import numpy as np # type: ignore
import pyautogui

# Load the input image and the symbol image
input_image = cv2.imread('../assets/input.png')
quick_repair_image = cv2.imread('../assets/QuickRepair.png')
ok_image = cv2.imread('../assets/OK.png')
select_all_image = cv2.imread('../assets/SelectAll.png')
plus_image = cv2.imread('../assets/Plus.png')

# I want to have 3 phases:
# 1. Try to detect if there is a plus symbol
# 2. If there is a plus symbol, click on it
# 3. If there is no plus symbol, wait until you detech the Quick Repair symbol then click on the quick repair symbol
# 4. If there is no quick repair symbol, click on the Select All symbol, then wait for 100ms and click on the OK symbol
# 5. Repeat the process
# show me the steps in the cmd line
# threshold for matching images is 0.9

def detect_and_click(image, template, threshold=0.9):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    if len(locations[0]) > 0:
        # Click on the first detected location
        pt = (locations[1][0], locations[0][0])
        click_position_x = int(pt[0] + template.shape[1] / 2)
        click_position_y = int(pt[1] + template.shape[0] / 2)
        pyautogui.click(click_position_x, click_position_y)
        return True
    return False

def get_screenshot():
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)

try:
    clicked_on_plus: bool = False
    while True:
        # Reload the input image
        input_image = get_screenshot()
        while clicked_on_plus:
            cv2.waitKey(100)
            input_image = get_screenshot()
            if detect_and_click(input_image, quick_repair_image):
                clicked_on_plus = False
                input_image = get_screenshot()
                cv2.waitKey(200)
                if detect_and_click(input_image, select_all_image,0.8):
                    detect_and_click(input_image, select_all_image,0.8)
                    cv2.waitKey(200)
                    input_image = get_screenshot()
                    detect_and_click(input_image, ok_image,0.8)
        
        if clicked_on_plus == False and detect_and_click(input_image, plus_image,0.6):
            clicked_on_plus = True
            cv2.waitKey(200)
except KeyboardInterrupt:
    print("Process interrupted by user. Exiting...")
    cv2.destroyAllWindows()
    

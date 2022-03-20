import os

from pynput import mouse, keyboard
import time
import pygetwindow
from PIL import Image, ImageGrab
from paddleocr import PaddleOCR

myKeyboard = keyboard.Controller()
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)


def mypress(value, gap=0.2):
    myKeyboard.press(value)
    time.sleep(gap)
    myKeyboard.release(value)
    time.sleep(gap)


def medicine():
    mypress('x')
    time.sleep(2)

    for cnt in range(4):
        mypress('z')
        time.sleep(1)

    for cnt in range(4):
        mypress('x')
        time.sleep(1)


def use_camp():
    print('使用野营帐')
    mypress('x')
    time.sleep(2)

    for cnt in range(10):
        mypress('z')
        time.sleep(2)


def back_to_main(app_window):
    cnt = 0
    while cnt < 30:
        content = capture_content_to_recognizer(app_window, '周目')
        if '周' in content or '目' in content or '数' in content or '兵' in content:
            return
        else:
            mypress('x')
            time.sleep(2)
    raise RuntimeError("返回失败")


def save(app_window):
    print('保存')
    mypress('x')
    time.sleep(2)

    print('left')
    mypress(keyboard.Key.left)
    time.sleep(1)

    print('left')
    mypress(keyboard.Key.left)
    time.sleep(1)

    cnt = 0
    while cnt < 30:
        menu_title = capture_content_to_recognizer(app_window, '记载')
        cnt += 1
        if '记载' in menu_title:
            break
        else:
            if cnt > 30:
                mypress('x')
                time.sleep(2)
                return
            print('left')
            mypress(keyboard.Key.left)
            time.sleep(1)

    print('z')
    mypress('z')
    time.sleep(3)

    cnt = 0
    while cnt < 30:
        menu_title = capture_content_to_recognizer(app_window, 'save')
        cnt += 1
        print(menu_title)
        if 'save' in menu_title or 'Save' in menu_title:
            break
        else:
            if cnt > 30:
                back_to_main(app_window)
                return
            print('z')
            mypress(keyboard.Key.left)
            time.sleep(1)
    print('down')
    mypress(keyboard.Key.down)
    time.sleep(2)

    print('z')
    mypress('z')
    time.sleep(3)

    back_to_main(window)


def test_recognize(path, engine='paddle'):
    for root, dirs, files in os.walk(path):
        # 遍历文件
        for f in files:
            content = ''
            filename = os.path.join(root, f)
            if engine == 'paddle':
                res = ocr.ocr(filename)
                for line in res:
                    content += line[1][0]
            print(content)


def test_capture():
    time.sleep(3)
    app_window = pygetwindow.getActiveWindow()
    left = app_window.topleft[0]
    top = app_window.topleft[1]
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 5, top + 440, left + 150, top + 490, 'round.png', 'chi_sim')
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 10, top + 395, left + 490, top + 490, 'show.png', 'chi_sim')
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 7, top + 370, left + 120, top + 450, 'fight.png', 'chi_sim')
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 420, top + 370, left + 490, top + 430, 'blood.png')
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 200, top + 75, left + 300, top + 105, 'write.png', 'chi_sim')
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 30, top + 395, left + 110, top + 450, 'save.png')
    time.sleep(3)
    content = capture_img_to_recognizer(left + 250, top + 215, left + 363, top + 320, 'exit.png', 'chi_sim')
    #time.sleep(3)
    #content = capture_img_to_recognizer(left + 30, top + 395, left + 110, top + 450, 'load.png')
    time.sleep(3)
    back_to_main(app_window)

    time.sleep(3)
    save(app_window)

    time.sleep(3)
    back_to_main(app_window)

    time.sleep(3)
    use_camp()


def capture_content_to_recognizer(app_window, category, engine='paddle'):
    left = app_window.topleft[0]
    top = app_window.topleft[1]
    content = ''
    if '周目' in category:
        content = capture_img_to_recognizer(left + 5, top + 440, left + 150, top + 490, 'round.png', 'chi_sim')
    elif '总攻' in category:
        content = capture_img_to_recognizer(left + 7, top + 370, left + 120, top + 450, 'fight.png', 'chi_sim')
    elif '血条' in category:
        content = capture_img_to_recognizer(left + 420, top + 370, left + 490, top + 430, 'blood.png')
    elif '出现' in category:
        content = capture_img_to_recognizer(left + 10, top + 395, left + 490, top + 490, 'show.png', 'chi_sim')
    elif '记载' in category:
        content = capture_img_to_recognizer(left + 200, top + 75, left + 300, top + 105, 'write.png', 'chi_sim')
    elif 'save' in category:
        content = capture_img_to_recognizer(left + 30, top + 395, left + 110, top + 450, 'save.png')
    elif 'load' in category:
        content = capture_img_to_recognizer(left + 30, top + 395, left + 110, top + 450, 'load.png')
    elif 'exit' in category:
        content = capture_img_to_recognizer(left + 250, top + 215, left + 340, top + 320, 'exit.png', 'chi_sim')
    return content


def capture_img_to_recognizer(left, top, right, bottom, filename='1.png', lang='eng', engine='paddle'):
    pic = ImageGrab.grab(bbox=(left, top, right, bottom))
    pic.save(filename)
    content = ''
    if engine == 'paddle':
        res = ocr.ocr(filename)
        for line in res:
            content += line[1][0]
    print(content)
    return content


def find_enemy():
    print("向左")
    myKeyboard.press(keyboard.Key.up)
    time.sleep(1)
    myKeyboard.release(keyboard.Key.up)
    time.sleep(0.1)
    print("向右")
    myKeyboard.press(keyboard.Key.down)
    time.sleep(1.2)
    myKeyboard.release(keyboard.Key.down)
    time.sleep(0.1)


def operation(punish=False):
    time.sleep(1)
    print("按B 3次")
    for i in range(3):
        mypress('x')
        time.sleep(2)
        text = capture_content_to_recognizer(window, '总攻')
        if '总攻' in text or '攻击' in text or '撤退' in text:
            break
    myKeyboard.release('x')

    time.sleep(2)
    if punish is False:
        print("往上")
        mypress(keyboard.Key.up)
        time.sleep(1)
        myKeyboard.release(keyboard.Key.up)
    else:
        print("往下, 撤退")
        mypress(keyboard.Key.down)
        time.sleep(1)
        myKeyboard.release(keyboard.Key.down)

    attack_cnt = 0
    while True:
        attack_cnt += 1
        print(f"选择总攻:{attack_cnt}")
        mypress('z')
        time.sleep(1)
        if attack_cnt % 10 == 0:
            text = capture_content_to_recognizer(window, '周目')
            if '周目' in text or '兵营' in text or '支线' in text:
                break
        if attack_cnt > 500:
            pic = ImageGrab.grab(bbox=(0, 0, window.right, window.height))
            pic.save('error.png')
            raise RuntimeError('it took too long, issue happens')


def store_something():
    mypress('z')
    mypress(keyboard.Key.right)
    mypress('z')
    mypress(keyboard.Key.down)


def get_something():
    mypress('z')
    mypress(keyboard.Key.left)
    mypress(keyboard.Key.left)
    mypress('z')
    mypress(keyboard.Key.down)


if __name__ == "__main__":
    # while True:
    #     get_something()
    count = 0
    #test_capture()

    time.sleep(2)
    #test_recognize('sample')

    #window = pygetwindow.getActiveWindow()
    #text = capture_content_to_recognizer(window, '出现')
    #if '出' in text or '现' in text or '了' in text:
        #print('true')
    while True:
        window = pygetwindow.getActiveWindow()
        print(window.title)
        if '吞食天地' not in window.title:
            flag = False
            windows = pygetwindow.getWindowsWithTitle('吞食天地')
            for w in windows:
                if '吞食天地2重制污妖王版v4.2（Panny潘尼DD版）' in w.title:
                    flag = True
                    print('find app')
                    w.restore()
                    try:
                        w.activate()
                    except Exception as e:
                        print(e)
                    break
            if flag is False:
                print('can not find app')
                break
        j = 0
        lvbu_cnt = 0
        tianqianzhe = False
        while True:
            j += 1
            find_enemy()
            if j % 2 == 0:
                text = capture_content_to_recognizer(window, '出现')
                if '马忠' in text:
                    lvbu_cnt += 1
                if '金胖狐' in text:
                    lvbu_cnt += 10
                if "天" in text and "者" in text:
                    tianqianzhe = True
                if '出现' in text:
                    break
        try:
            operation(tianqianzhe)
        except Exception as e:
            print(e)
            break
        count += 1
        print(f"结束, count = {count}")
        if count % 100 == 0 or tianqianzhe is True:
            save(window)

        if count % 30 == 0 or lvbu_cnt > 2 or tianqianzhe is True:
            use_camp()
            lvbu_cnt = 0
            back_to_main(window)



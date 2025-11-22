import sys
import os
import atexit
import time
import threading
import RPi.GPIO as GPIO

current_file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_file_dir))
sys.path.append(parent_dir)
from common.common import key_down, key_up, type_text, release_all, sleep_random, key_click


#종료 시 동작 정의
def exit_print():
    print('프로그램이 종료됩니다!')
    release_all()
    time.sleep(0.2)

#종료 레지스터 등록
atexit.register(exit_print)

#Flag 선언
aFlag = True
bFlag = True
cFlag = True
dFlag = True

#변수 선언
ctrl    = "KEY_LEFTCTRL"
enter   = "ENTER"
win     = "GUI"
shift   = "KEY_LEFTSHIFT"
alt     = "KEY_LEFTALT"
right   = "KEY_RIGHT"
left    = "KEY_LEFT"
down    = "KEY_DOWN"
up      = "KEY_UP"


#A - 공격 유지
def task_A() :
    while True :
        if aFlag :
            key_down(ctrl, 0, 0, 0)
            sleep_random(1000, 0, 5*1000)
            key_up(ctrl, 0, 0, 0)
            sleep_random(0, 0, 300)
            key_click("KEY_S", 0, 0, 0)
            sleep_random(100, 0, 300)
        else :
            time.sleep(0.1)

#B - 점프 반복
def task_B() :
    while True :
        if bFlag :
            key_click(alt,0,0,100)
            key_click(alt,10,0,30)
            sleep_random(1000, 0, 100)

#C - 방향 유지, 변경
def task_C():
    arrorSelector = 0
    while cFlag :
        arrorSelector += 1
        if arrorSelector % 2 == 0 :
            arrow = right
        else :
            arrow = left

        key_down(arrow, 0,0,0)
        sleep_random(moveTime * 1000, 0, 1*1000)
        key_up(arrow, 0,0,0)
        sleep_random(0, 0, 300)

#D - 설치기 설치
def task_D():
    while dFlag :
        #60초에 한번씩 설치기 시작
        sleep_random(50 * 1000, 1 * 1000, 5 * 1000)

        global aFlag
        global bFlag
        global cFlag
        aFlag = False
        bFlag = False
        cFlag = False

        global thread_a, thread_b, thread_c
        thread_a.join()
        thread_b.join()
        thread_c.join()

        #모든 키 때기
        release_all()
        sleep_random(1 * 100, 0, 300)
        
        #공격키 누르기
        key_down(ctrl, 0, 0, 0)
        sleep_random(1 * 100, 0, 300)

        #오른쪽 점프
        key_down(right, 0, 0, 100)
        for i in range(3) :
            key_click(alt,0,0,100)
            key_click(alt,10,0,30)
            sleep_random(1000, 0, 100)
        key_up(right, 0, 0, 100)
        sleep_random(1 * 1000, 0, 300)
        
        #왼쪽 이동
        key_down(left, 0, 0, 100)
        sleep_random(1000, 0, 100)
        key_up(left, 0, 0, 100)
        sleep_random(100, 0, 300)
        

        #위로 점프
        key_down(up, 0, 0, 100)
        for i in range(2) :
            key_click(alt, 0, 0, 100)
            key_click(alt, 10, 0, 30)
            sleep_random(1700, 0, 100)
        key_up(up, 0, 0, 100)
        sleep_random(100, 0, 100)

        #X클릭
        key_up(ctrl, 0, 0, 300)
        key_click('KEY_X', 0, 0, 300)
        key_down(ctrl, 0, 0, 300)
        sleep_random(100, 0, 100)

        #왼쪽 이동
        key_down(left, 0, 0, 100)
        sleep_random(1000, 0, 200)
        key_up(left, 0, 0, 100)
        sleep_random(100, 0, 100)

        #shift 클릭
        key_up(ctrl, 0, 0, 300)
        key_click(shift, 0, 0, 300)
        key_down(ctrl, 0, 0, 300)
        sleep_random(100, 0, 100)

        #아래로 3번
        key_down(down, 0, 0, 100)
        for i in range(3) :
            key_click(alt,0,0,100)
            sleep_random(1700, 0, 100)
        key_up(down, 0, 0, 100)
        sleep_random(700, 0, 100)

        #공격키 때기
        key_up(ctrl, 0, 0, 300)
        sleep_random(100, 0, 100)

        #다시 반복 시작
        aFlag = True
        bFlag = True
        cFlag = True

        thread_a = threading.Thread(target=task_A)
        thread_b = threading.Thread(target=task_B)
        thread_c = threading.Thread(target=task_C)
        thread_a.start()
        thread_b.start()
        thread_c.start()


if __name__ == "__main__":
    print("메인 스레드 시작")

    thread_a = threading.Thread(target=task_A)
    thread_b = threading.Thread(target=task_B)
    thread_c = threading.Thread(target=task_C)
    thread_d = threading.Thread(target=task_D)

    # 1. 스레드를 시작합니다.
    thread_a.start()
    thread_b.start()
    thread_c.start()
    thread_d.start()
    


    # 2. 메인 스레드가 thread_a가 종료될 때까지 기다립니다.
    thread_a.join()
    thread_b.join()
    thread_c.join()
    thread_d.join()

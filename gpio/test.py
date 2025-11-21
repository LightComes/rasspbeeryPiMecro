import RPi.GPIO as GPIO
import time

# GPIO 모드 설정 (BCM 모드 사용: 핀 번호가 아닌 GPIO 번호를 사용)
GPIO.setmode(GPIO.BCM)

# 스위치가 연결된 GPIO 핀 번호
SWITCH_PIN = 18

# GPIO 18번 핀을 입력(IN)으로 설정
# 내부 풀다운 저항(pull-down resistor) 활성화
# 스위치가 눌리지 않으면 LOW(0V) 상태를 유지하도록 함
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print(f"GPIO {SWITCH_PIN} 스위치 상태 확인 중... (Ctrl+C로 종료)")

try:
    while True:
        # 핀의 현재 상태(값) 읽기
        if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            print("스위치 ON (눌림)")
        else:
            print("스위치 OFF (안 눌림)")

        # 0.1초 대기 (CPU 부하 줄이기)
        time.sleep(0.1)

except KeyboardInterrupt:
    # Ctrl+C 눌렀을 때 실행되는 부분
    print("프로그램 종료")

finally:
    # 종료 시 GPIO 설정 초기화 (권장)
    GPIO.cleanup()

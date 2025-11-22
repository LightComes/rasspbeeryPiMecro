import lgpio
import time
import subprocess
import RPi.GPIO as GPIO

# GPIO 핀 설정 (예시: GPIO 17번 핀 사용)
GPIO.setmode(GPIO.BCM)
SWITCH_PIN = 18

# 1. GPIO 칩 핸들(handle) 열기
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def kill_process_by_name(process_name):
    print(f"'{process_name}'을 포함하는 프로세스 검색 및 종료 시도...")
    
    try:
        # ssh 명령어 수행
        command = f"ps -ef | grep '{process_name}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        
        # 2. 결과 출력 라인 파싱
        output_lines = result.stdout.strip().split('\n')
        
        pidsList = []
        for line in output_lines:
            # grep 실행 과정에서 나오는 자기 자신은 제외
            if "grep" in line:
                continue

            if line.strip():
                # 각 라인에서 PID는 보통 두 번째 열에 있습니다.
                # 예시 라인 형식: UID   PID  PPID ... CMD
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    pidsList.append(pid)

        # 3. PID 목록으로 kill 명령 실행
        if pidsList:
            print(f"종료할 PID 목록: {pidsList}")
            for pid in pidsList:
                try:
                    # 'kill -9 PID' 명령 실행 (강제 종료)
                    subprocess.run(['kill', '-9', pid], check=True)
                    print(f"PID {pid} 종료 완료.")
                except subprocess.CalledProcessError:
                    print(f"PID {pid} 종료 실패.")
        else:
            print(f"'{process_name}'에 해당하는 실행 중인 프로세스가 없습니다.")

    except subprocess.CalledProcessError as e:
        print(f"명령 실행 중 오류 발생: {e.stderr}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")


try:
    print(f"스위치 {SWITCH_PIN}번 핀 테스트 시작. Ctrl+C로 종료.")

    macroName = "255_liman.py"
    macroPath = "/home/dsd2115/rasspbeeryPiMecro/macroScript/ren/" + macroName

    while True:
        # 핀 상태 읽기
        if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            #실행 중인 메크로 검사
            command = f"ps -ef | grep '{macroName}'"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            output_lines = result.stdout.strip().split('\n')
            pidsList = []
            for line in output_lines:
                # grep 실행 과정에서 나오는 자기 자신은 제외
                if "grep" in line:
                    continue

                if line.strip():
                    # 각 라인에서 PID는 보통 두 번째 열에 있습니다.
                    # 예시 라인 형식: UID   PID  PPID ... CMD
                    parts = line.split()
                    if len(parts) > 1:
                        pid = parts[1]
                        pidsList.append(pid)
            if not pidsList :
                subprocess.Popen(['sudo', 'python3', macroPath], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                # detached process로 실행되도록 설정 (옵션)
                start_new_session=True) 
            else :
                print("정상 가동 중")
        else:
            kill_process_by_name(macroName)
        time.sleep(1) # 0.5초마다 상태 확인

except KeyboardInterrupt:
    print("사용자 종료 요청.")

finally:
    # 종료 시 GPIO 설정 초기화 (권장)
    GPIO.cleanup()
    print("GPIO 정리 완료.")



# -*- coding: utf-8 -*-
from playsound import playsound
import schedule
import os, sys, time

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def volume_change():
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Get current volume 
    VolumeRangeDb = volume.GetVolumeRange()
    max_db, min_db = VolumeRangeDb[-1], VolumeRangeDb[0]

    vol = (max_db - min_db) * percent + min_db 
    if vol > 0: vol = 0
    volume.SetMasterVolumeLevel(vol, None)

def lunch():
    print('-----Music Start-----')
    print('-----11:25분은 점심시간-----')
    # volume_change()
    playsound(resource_path('./music/lunch.mp3'))

def getoffwork():
    print('-----Music Start-----')
    print('-----17:55분은 퇴근시간-----')
    # volume_change()
    playsound(resource_path('./music/getoffwork.mp3'))

def _init():
    schedule.every().day.at('11:25').do(lunch)
    schedule.every().day.at('17:55').do(getoffwork)

def run():
    _init()
    print('Schedule 실행 중...')

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print('프로그램 종료')
            sys.exit(0)

if __name__ == '__main__':
    global percent
    percent = 0.7   # 0.0(min) ~ 1.0(max)
    run()

# pyinstaller -F krri_alarm.py --hidden-import playsound:schedule:pycaw:comtypes:ctypes --add-data='./music/*;music' --add-data='./icon/*;icon' -i="icon/krri.ico" 
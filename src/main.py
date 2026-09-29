"""Connect an ESP32 running MicroPython to Wi-Fi and start WebREPL."""
import time

import network

from secrets import DNS, GATEWAY, IP, SUBNET, WIFI_PASSWORD, WIFI_SSID

WIFI_TIMEOUT_SECONDS = 20
from motor_config import DIR_PIN, STEP_PIN
from stepper import Stepper


def get_step() -> Stepper:
    print(f'creating stepper with: step_pin={STEP_PIN}, dir_pin={DIR_PIN}')
    micro = 32
    spr = 200 * micro
    st = Stepper(
        step_pin=STEP_PIN,
        dir_pin=DIR_PIN,
        # en_pin=en_pin,
        steps_per_rev=spr,
        speed_sps=100
        # invert_dir=False,
        # timer_id=-1,
    )
    st.speed_rps(0.5)
    return st


def print_pos(st):
    print(st.get_pos(), st.get_pos_deg(), st.get_pos_rad())


def rotate(st: Stepper, degrees: int = 45):
    print(f'rotating {degrees} degrees')
    st.target_deg(degrees)


def connect_wifi(static: bool = False):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        if static:
            wlan.ifconfig((IP, SUBNET, GATEWAY, DNS))
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        deadline = time.ticks_add(time.ticks_ms(), WIFI_TIMEOUT_SECONDS * 1000)

        while not wlan.isconnected() and time.ticks_diff(deadline, time.ticks_ms()) > 0:
            time.sleep_ms(250)

    if not wlan.isconnected():
        raise RuntimeError("Could not connect to Wi-Fi")

    print("Wi-Fi connected:", wlan.ifconfig()[0])
    return wlan


def do_it():
    print('doing it')
    st = get_step()
    print_pos(st)
    rotate(st, 30)


connect_wifi(static=True)

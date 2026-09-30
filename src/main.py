import time
from secrets import DNS, GATEWAY, IP, SUBNET, WIFI_PASSWORD, WIFI_SSID

import network

from button import Button
from config import DIR_PIN, MICROSTEPS_REV, SPEED_SPS, STEP_PIN, WIFI_TIMEOUT_SECONDS
from stepper import Stepper


def get_step() -> Stepper:
    print(
        f"creating stepper with: step_pin={STEP_PIN}, dir_pin={DIR_PIN}, steps/rev={MICROSTEPS_REV}, speed sps={SPEED_SPS}"
    )
    st = Stepper(
        step_pin=STEP_PIN,
        dir_pin=DIR_PIN,
        steps_per_rev=MICROSTEPS_REV,
        speed_sps=SPEED_SPS,
    )
    return st


def print_pos(st):
    print(st.get_pos(), st.get_pos_deg(), st.get_pos_rad())


def rotate(st: Stepper, degrees: int = 45):
    print(f"rotating {degrees} degrees")
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


def for_3_seconds(st):
    st.free_run(1)
    time.sleep(3)
    st.stop()


def do_it():
    print("doing it")
    st = get_step()
    print_pos(st)

    rotate(st, 30)


connect_wifi(static=True)
st = get_step()
print_pos(st)


def on_button_press():
    print("button pressed")
    rotate(st, 30)


button = Button(on_button_press)

from bus.bus_emulator import BusEmulator
from modules.efis import EFIS
from modules.autopilot import Autopilot
import time

def print_message(msg):
    print(f">> {msg}")

def main():
    bus = BusEmulator()
    bus.message_transmitted.connect(print_message)

    efis = EFIS(bus)
    ap = Autopilot(bus)

    efis.start()
    ap.start()

    print("🛰️ CLI Visualizer running (CTRL+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        efis.stop()
        ap.stop()
        efis.join()
        ap.join()
        print("Visualizer stopped.")

if __name__ == "__main__":
    main()

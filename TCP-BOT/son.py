import subprocess
import time
import sys
import platform
import os
import threading

SCRIPTS = ["bot.py"]   # jitni bhi scripts run karni ho
RESTART_DELAY = 5  # seconds
DNS_SERVER = "8.8.8.8"  # ya "1.1.1.1"

def set_dns():
    try:
        system = platform.system().lower()

        if "linux" in system or "darwin" in system:  # Linux/Mac
            print(f"[WATCHDOG] Setting DNS → {DNS_SERVER}")
            with open("/etc/resolv.conf", "w") as f:
                f.write(f"nameserver {DNS_SERVER}\n")

        elif "windows" in system:  # Windows
            print(f"[WATCHDOG] Setting DNS → {DNS_SERVER}")
            subprocess.run(
                ["netsh", "interface", "ip", "set", "dns", "name=Wi-Fi", "static", DNS_SERVER],
                shell=True
            )
        else:
            print("[WATCHDOG] Unknown OS → DNS not set")

    except Exception as e:
        print(f"[WATCHDOG] Failed to set DNS: {e}")

def run_script(script_name):
    set_dns()  # first time DNS set kar do
    while True:
        print(f"[WATCHDOG] Starting {script_name} ...")
        process = subprocess.Popen([sys.executable, script_name])

        process.wait()  # wait until script exits/crashes
        exit_code = process.returncode

        if exit_code == 0:
            print(f"[WATCHDOG] {script_name} exited normally (code 0). Restarting in {RESTART_DELAY} sec...")
        else:
            print(f"[WATCHDOG] {script_name} crashed (exit code {exit_code}). Restarting in {RESTART_DELAY} sec...")

        time.sleep(RESTART_DELAY)
        set_dns()  # har restart ke baad bhi DNS set karo

if __name__ == "__main__":
    threads = []
    for script in SCRIPTS:
        t = threading.Thread(target=run_script, args=(script,))
        t.daemon = True
        t.start()
        threads.append(t)

    # threads ko alive rakhne ke liye
    for t in threads:
        t.join()
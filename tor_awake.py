import subprocess
import time
import os

tor_exe_path = r"C://tor//tor//tor.exe"
torrc_path = r"C://tor//tor//torrc"  # Must not have .txt

def start_tor():
    print("[INFO] Starting Tor with custom torrc...")
    tor_process = subprocess.Popen(
        [tor_exe_path, "-f", torrc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stdout and stderr for simpler output
        text=True
    )
    return tor_process

tor_process = start_tor()

# Print logs as they come in
try:
    print("[INFO] Tor is running. Showing logs... Press CTRL+C to stop.")
    for line in tor_process.stdout:
        print(line.strip())
except KeyboardInterrupt:
    print("\n[INFO] Keyboard interrupt received. Shutting down Tor...")
finally:
    tor_process.terminate()
    tor_process.wait()
    print("[INFO] Tor has been shut down.")

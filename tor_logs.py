import subprocess

tor_exe_path = r"C://tor//tor//tor.exe"
torrc_path = r"C://tor//tor//torrc"

tor_process = subprocess.Popen(
    [tor_exe_path, "-f", torrc_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

for line in tor_process.stdout:
    print(line.strip())

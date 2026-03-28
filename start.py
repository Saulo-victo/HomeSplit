import subprocess
import sys
import time


def run_app():
    backend_process = subprocess.Popen(
        [sys.executable, '-m', 'fastapi', 'dev', 'main.py'])

    time.sleep(5)

    frontend_process = subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run', 'web/main_app.py'
    ])

    backend_process.wait()
    frontend_process.wait()


if __name__ == '__main__':
    run_app()

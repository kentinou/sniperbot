
from multiprocessing import Process
import os

def run_main_loop():
    os.system("python main_loop.py")

def run_tracker():
    os.system("python trade_tracker.py")

if __name__ == "__main__":
    Process(target=run_main_loop).start()
    Process(target=run_tracker).start()

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time
import threading

console = Console()

def task(task_id, duration):
    for i in range(duration):
        console.log(f"Task {task_id}: {i+1}/{duration}")
        time.sleep(1)
    console.log(f"Task {task_id} finished!")

def main():
    tasks = [
        threading.Thread(target=task, args=(1, 5)),
        threading.Thread(target=task, args=(2, 3)),
    ]

    for t in tasks:
        t.start()
    for t in tasks:
        t.join()

if __name__ == "__main__":
    main()
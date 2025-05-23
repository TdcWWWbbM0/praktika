import subprocess
from datetime import datetime
import sqlite3

conn = sqlite3.connect('sys_monitor.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    cpu REAL,
    memory REAL,
    disk REAL
)""")
conn.commit()

def run_wmic(command):
    try:
        output = subprocess.check_output(['wmic'] + command, text=True, stderr=subprocess.DEVNULL)
        return [line.strip() for line in output.strip().splitlines() if line.strip()]
    except:
        return []

def get_cpu():
    lines = run_wmic(['cpu', 'get', 'loadpercentage'])
    for line in lines:
        if line.isdigit():
            return float(line)
    return 0.0

def get_memory():
    lines = run_wmic(['OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize'])
    if len(lines) < 2:
        return 0.0
    parts = lines[1].split()
    if len(parts) != 2:
        return 0.0
    free_kb, total_kb = parts
    try:
        free = float(free_kb)
        total = float(total_kb)
        return round((total - free) / total * 100, 2)
    except:
        return 0.0

def get_disk():
    lines = run_wmic(['logicaldisk', 'where', "DeviceID='C:'", 'get', 'FreeSpace,Size'])
    if len(lines) < 2:
        return 0.0
    parts = lines[1].split()
    if len(parts) != 2:
        return 0.0
    free_str, size_str = parts
    try:
        free = float(free_str)
        size = float(size_str)
        return round((size - free) / size * 100, 2) if size > 0 else 0.0
    except:
        return 0.0

def save():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO stats (time, cpu, memory, disk) VALUES (?, ?, ?, ?)",
                (now, get_cpu(), get_memory(), get_disk()))
    conn.commit()
    print("Данные сохранены!")

def show():
    cur.execute("SELECT * FROM stats ORDER BY id")
    for row in cur.fetchall():
        print(f"{row[0]:<4} {row[1]:<19} {row[2]:<6.1f} {row[3]:<6.1f} {row[4]:<6.1f}")

while True:
    print("\n1 - Сохранить\n2 - Показать\n3 - Выход")
    cmd = input("Выберите: ").strip()
    if cmd == '1':
        save()
    elif cmd == '2':
        show()
    elif cmd == '3':
        break

conn.close()
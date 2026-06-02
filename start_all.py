"""
start_all.py - Khởi động toàn bộ 3 Nodes cùng lúc
Cách dùng: python start_all.py
"""
import subprocess
import sys
import time


NODES = [
    
    (5001, 'site1_database.db'),
    (5002, 'site2_database.db'),
    (5003, 'site3_database.db'),
]

processes = []

print("          KHỞI ĐỘNG HỆ THỐNG PHÂN TÁN")
for port, db in NODES:
    p = subprocess.Popen([sys.executable, 'app.py', str(port), db])     
    processes.append(p)
    print(f"  -> Node tại Port {port} (DB: {db}) đã khởi động.")
    time.sleep(0.5)  # Chờ nhẹ để tránh xung đột

print("\nTất cả 3 nodes đang chạy!")    
print("Nhấn Ctrl+C để dừng toàn bộ hệ thống.\n")

try:    
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\nĐang dừng tất cả nodes...")
    for p in processes:
        p.terminate()
    print("Đã dừng xong.")

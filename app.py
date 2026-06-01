from flask import Flask, jsonify
import sys
import requests
import threading
import time
from node_logic import generate_hash

app = Flask(__name__)

# Nhận cổng (port) và tên file database từ dòng lệnh khi khởi động
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
DB_NAME = sys.argv[2] if len(sys.argv) > 2 else 'site1_database.db'

# Danh sách địa chỉ của 3 máy trong mạng lưới
NODES = [
    "http://127.0.0.1:5001", 
    "http://127.0.0.1:5002", 
    "http://127.0.0.1:5003"
]

@app.route('/hash', methods=['GET'])
def get_hash():
    """API để các máy khác gọi vào xin mã băm của máy này"""
    current_hash = generate_hash(DB_NAME)
    return jsonify({"node_port": PORT, "hash": current_hash})

@app.route('/sync', methods=['GET'])
def check_sync():
    """API kích hoạt quá trình Đối soát (Reconciliation) toàn mạng"""
    hashes = {}
    for node_url in NODES:
        try:
            # Gửi yêu cầu qua mạng đến các máy khác để lấy mã băm
            response = requests.get(f"{node_url}/hash")
            data = response.json()
            hashes[node_url] = data['hash']
        except:
            hashes[node_url] = "OFFLINE"
    
    # Kiểm tra xem mã băm của cả 3 máy có giống hệt nhau không
    all_hashes = list(hashes.values())
    is_synced = all(h == all_hashes[0] for h in all_hashes) and "OFFLINE" not in all_hashes

    return jsonify({
        "status": "ĐỒNG BỘ (SYNCED)" if is_synced else "🚨 CẢNH BÁO: LỆCH DỮ LIỆU (DESYNC)!",
        "details": hashes
    })

def auto_hash_task():
    """Tự động tạo hash-chain mỗi 10 phút"""
    while True:
        time.sleep(600)  # 600 giây = 10 phút
        h = generate_hash(DB_NAME)
        print(f"[Tự động-10phút] Hash mới của {DB_NAME}: {h[:20]}...")

if __name__ == '__main__':
    print(f"Khởi động Node tại Port {PORT}, sử dụng Data: {DB_NAME}")
    
    # Chạy tiến trình nền (daemon) — sẽ tự tắt khi server dừng
    t = threading.Thread(target=auto_hash_task, daemon=True)
    t.start()
    print("Tiến trình tự động hash mỗi 10 phút đã được kích hoạt.")
    
    app.run(port=PORT)
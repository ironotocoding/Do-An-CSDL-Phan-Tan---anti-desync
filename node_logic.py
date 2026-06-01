import sqlite3
import hashlib

def add_transaction(db_name, product_id, action, amount):
    """Hàm này dùng để thực hiện 1 giao dịch nhập/xuất kho"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 1. Lưu vào lịch sử giao dịch (Transaction_Log)
    cursor.execute("INSERT INTO Transaction_Log (product_id, action, amount) VALUES (?, ?, ?)", (product_id, action, amount))
    
    # 2. Cập nhật số lượng trong kho hàng
    if action == 'XUAT':
        cursor.execute("UPDATE Product_Stock SET quantity = quantity - ? WHERE product_id = ?", (amount, product_id))
    else:
        cursor.execute("UPDATE Product_Stock SET quantity = quantity + ? WHERE product_id = ?", (amount, product_id))
        
    conn.commit()
    conn.close()
    print(f"Đã lưu giao dịch: {action} {amount} sản phẩm có ID {product_id}")

def generate_hash(db_name):
    """Tạo Hash-Chain: mỗi giao dịch được hash cùng với hash của giao dịch trước"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Lấy 100 giao dịch gần nhất, theo thứ tự thời gian (cũ -> mới)
    cursor.execute("SELECT * FROM Transaction_Log ORDER BY timestamp ASC LIMIT 100")
    transactions = cursor.fetchall()
    conn.close()

    # --- XÂY DỰNG HASH-CHAIN ---
    # Bắt đầu từ một giá trị gốc (genesis block)
    current_hash = "0" * 64
    for tx in transactions:
        # Hash mới = SHA256(hash_cũ + dữ liệu_giao_dịch)
        # Mỗi block phụ thuộc vào block trước -> không thể sửa 1 block mà không bị phát hiện
        data = current_hash + str(tx)
        current_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()

    print(f"Hash-Chain cuối của {db_name}:\n{current_hash}\n")
    return current_hash

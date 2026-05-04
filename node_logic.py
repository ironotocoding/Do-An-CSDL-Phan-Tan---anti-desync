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
    """Hàm này dùng để lấy lịch sử giao dịch và băm (hash) chúng lại"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Lấy 100 giao dịch gần nhất (đúng như yêu cầu đề bài)
    cursor.execute("SELECT * FROM Transaction_Log ORDER BY timestamp DESC LIMIT 100")
    transactions = cursor.fetchall()
    conn.close()

    # Ghép toàn bộ dữ liệu giao dịch thành 1 chuỗi chữ (string)
    data_string = str(transactions)

    # Đưa vào "máy xay" SHA-256 để tạo mã băm
    hash_object = hashlib.sha256(data_string.encode('utf-8'))
    hash_result = hash_object.hexdigest()

    print(f"Mã băm hiện tại của {db_name} là:\n{hash_result}\n")
    return hash_result

# Chạy thử nghiệm trên Site 1
if __name__ == "__main__":
    print("--- CHẠY THỬ NGHIỆM GIAO DỊCH ---")
    # Thử bán đi 5 cái Laptop Gaming (ID = 1)
    add_transaction('site1_database.db', 1, 'XUAT', 5)
    
    # Tạo và in ra mã băm để kiểm tra
    generate_hash('site1_database.db')
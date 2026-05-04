import sqlite3

def setup_database(db_name):
    # Kết nối (hoặc tạo mới nếu chưa có) file database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 1. Tạo bảng Kho hàng (Product_Stock)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product_Stock (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    # 2. Tạo bảng Lịch sử Giao dịch (Transaction_Log) - Dùng để tạo Hash sau này
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transaction_Log (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        action TEXT, 
        amount INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Thêm thử 2 sản phẩm mẫu vào kho
    cursor.execute("INSERT OR IGNORE INTO Product_Stock (product_id, product_name, quantity) VALUES (1, 'Laptop Gaming', 50)")
    cursor.execute("INSERT OR IGNORE INTO Product_Stock (product_id, product_name, quantity) VALUES (2, 'Chuột không dây', 200)")

    conn.commit()
    conn.close()
    print(f"Đã khởi tạo thành công database: {db_name}")

# Chạy hàm để tạo database cho Site 1
if __name__ == "__main__":
    setup_database('site1_database.db')
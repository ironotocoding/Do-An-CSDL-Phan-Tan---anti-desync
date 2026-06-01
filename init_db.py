import sqlite3

def setup_database(db_name):
    # Kết nối (hoặc tạo mới nếu chưa có) file database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Xóa sạch dữ liệu cũ (nếu có) để bắt đầu lại từ đầu
    cursor.execute('DROP TABLE IF EXISTS Product_Stock')
    cursor.execute('DROP TABLE IF EXISTS Transaction_Log')

    # 1. Tạo bảng Kho hàng (Product_Stock)
    cursor.execute('''
    CREATE TABLE Product_Stock (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    # 2. Tạo bảng Lịch sử Giao dịch (Transaction_Log) - Dùng để tạo Hash sau này
    cursor.execute('''
    CREATE TABLE Transaction_Log (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        action TEXT, 
        amount INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Thêm 20 sản phẩm mẫu vào kho
    products = [
        (1,  'Laptop Gaming ASUS ROG',     50),
        (2,  'Chuột không dây Logitech',   200),
        (3,  'Bàn phím cơ RGB',            150),
        (4,  'Màn hình 27 inch 4K',        40),
        (5,  'Tai nghe Sony WH-1000XM5',   80),
        (6,  'Ổ cứng SSD 1TB Samsung',     120),
        (7,  'RAM DDR5 16GB',              300),
        (8,  'Card màn hình RTX 4070',     25),
        (9,  'Webcam Full HD Logitech',    90),
        (10, 'Bộ sạc nhanh 65W',          250),
        (11, 'USB Hub 7 cổng',            180),
        (12, 'Ghế gaming DXRacer',         30),
        (13, 'Bàn nâng hạ điện',           20),
        (14, 'Loa Bluetooth JBL',         110),
        (15, 'Máy in HP LaserJet',         15),
        (16, 'Router WiFi 6 TP-Link',      60),
        (17, 'Điện thoại iPhone 15',       45),
        (18, 'Máy tính bảng iPad Air',     35),
        (19, 'Đồng hồ Apple Watch 9',      55),
        (20, 'Ổ cứng di động 2TB WD',     130),
    ]
    # 3. Hàm thêm dữ liệu mẫu
    for pid, name, qty in products:
        cursor.execute(
            "INSERT OR IGNORE INTO Product_Stock (product_id, product_name, quantity) VALUES (?, ?, ?)",
            (pid, name, qty)
        )

    conn.commit()
    conn.close()
    print(f"Đã khởi tạo thành công database: {db_name}")

# Tạo database cho cả 3 Sites
if __name__ == "__main__":
    for site_db in ['site1_database.db', 'site2_database.db', 'site3_database.db']:
        setup_database(site_db)
    print("\nKhởi tạo xong cả 3 Sites!")
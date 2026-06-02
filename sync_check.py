import shutil
import sqlite3
from node_logic import generate_hash, add_transaction

def reset_transactions():
    """Xóa sạch lịch sử giao dịch của site1 trước khi demo, tránh số liệu tích lũy"""
    conn = sqlite3.connect('site1_database.db')
    conn.execute("DELETE FROM Transaction_Log")
    conn.commit()
    conn.close()

def simulate_distributed_network():
    print("          BƯỚC 1: KHỞI TẠO MẠNG LƯỚI PHÂN TÁN (3 SITES)")
    # Xóa sạch giao dịch cũ để đảm bảo bắt đầu từ trạng thái sạch
    reset_transactions()
    # Copy file database của Site 1 ra làm 2 bản để tạo Site 2 và Site 3
    shutil.copyfile('site1_database.db', 'site2_database.db')
    shutil.copyfile('site1_database.db', 'site3_database.db')
    print("Đã tạo xong Site 2 và Site 3. Lúc này cả 3 máy giống hệt nhau.\n")

    print("          BƯỚC 2: CÔNG CỤ RECONCILIATION KIỂM TRA ĐỒNG BỘ")
    hash1 = generate_hash('site1_database.db')
    hash2 = generate_hash('site2_database.db')
    hash3 = generate_hash('site3_database.db')
    
    if hash1 == hash2 == hash3:
        print(" TRẠNG THÁI ỔN ĐỊNH: Dữ liệu cả 3 Site hoàn toàn đồng bộ!\n")
    
    print("          BƯỚC 3: HACKER MODE (TẠO LỖI DESYNC)")
    print("[Hacker đang chọn mục tiêu tấn công...]\n")

    # Chọn site (1/2/3 là giới hạn kỹ thuật, không phải rule nghiệp vụ)
    while True:
        site_choice = input("Chọn Site để tấn công (1, 2 hoặc 3): ").strip()
        if site_choice in ('1', '2', '3'):
            break
        print("  Chỉ có 3 site trong hệ thống. Thử lại.")

    db_map = {'1': 'site1_database.db', '2': 'site2_database.db', '3': 'site3_database.db'}
    target_db = db_map[site_choice]

    # Hiển thị danh sách sản phẩm để tham khảo (hacker có thể thấy được dữ liệu)
    conn = sqlite3.connect(target_db)
    rows = conn.execute("SELECT product_id, product_name, quantity FROM Product_Stock ORDER BY product_id").fetchall()
    conn.close()

    print("\n[Hacker đã truy cập được dữ liệu kho hàng của Site này:]")
    for pid, name, qty in rows:
        print(f"  ID {pid:>2}: {name} (Số lượng: {qty})")
    print()

    # Hacker nhập bất kỳ ID và số lượng nào — không bị giới hạn
    product_id = int(input("Nhập Product ID muốn chèn giao dịch lậu: ").strip())
    amount     = int(input("Nhập số lượng hàng lậu: ").strip())

    print(f"\n[Hacker đang tấn công Site {site_choice} — chèn {amount} hàng lậu vào ID={product_id}...]")
    add_transaction(target_db, product_id, 'NHAP_LAU', amount)
    print()

    
    print("          BƯỚC 4: HỆ THỐNG TỰ ĐỘNG PHÁT HIỆN SAI LỆCH")
    print("[Hệ thống dùng Lazy Replication: Đang chờ chu kỳ quét tự động 10 phút...]")
    import time
    for i in range(5, 0, -1):
        print(f"  ... Mô phỏng thời gian trôi nhanh: {i} ...")
        time.sleep(1)
        
    print("\n[Hệ thống tự động tỉnh dậy và kiểm tra mã băm toàn mạng...]")
    # Kiểm tra lại mã băm sau chu kỳ 10 phút
    new_hash1 = generate_hash('site1_database.db')
    new_hash2 = generate_hash('site2_database.db')
    new_hash3 = generate_hash('site3_database.db')


    if new_hash1 == new_hash2 == new_hash3:
        print("-> TRẠNG THÁI: Đồng bộ — Cả 3 site khớp nhau hoàn toàn.")
    else:
        print("->  CẢNH BÁO BẢO MẬT: ĐÃ PHÁT HIỆN SAI LỆCH DỮ LIỆU (STATE DIVERGENCE)!")

if __name__ == "__main__":
    simulate_distributed_network()  
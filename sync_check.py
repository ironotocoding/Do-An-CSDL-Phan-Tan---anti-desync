import shutil
from node_logic import generate_hash, add_transaction

def simulate_distributed_network():
    print("=== BƯỚC 1: KHỞI TẠO MẠNG LƯỚI PHÂN TÁN (3 SITES) ===")
    # Copy file database của Site 1 ra làm 2 bản để tạo Site 2 và Site 3
    shutil.copyfile('site1_database.db', 'site2_database.db')
    shutil.copyfile('site1_database.db', 'site3_database.db')
    print("Đã tạo xong Site 2 và Site 3. Lúc này cả 3 máy giống hệt nhau.\n")

    print("=== BƯỚC 2: CÔNG CỤ RECONCILIATION KIỂM TRA ĐỒNG BỘ ===")
    hash1 = generate_hash('site1_database.db')
    hash2 = generate_hash('site2_database.db')
    hash3 = generate_hash('site3_database.db')
    
    if hash1 == hash2 == hash3:
        print("-> TRẠNG THÁI ỔN ĐỊNH: Dữ liệu cả 3 Site hoàn toàn đồng bộ!\n")
    
    print("=== BƯỚC 3: HACKER MODE (TẠO LỖI DESYNC) ===")
    print("Một hacker vừa xâm nhập và bí mật sửa kho hàng ở Site 2...")
    # Cố tình tạo một giao dịch ảo ở Site 2 để làm lệch dữ liệu
    add_transaction('site2_database.db', 2, 'NHAP_LAU', 999)
    print("\n")
    
    print("=== BƯỚC 4: HỆ THỐNG PHÁT HIỆN SAI LỆCH ===")
    # Kiểm tra lại mã băm sau 10 phút (giả lập theo yêu cầu đề bài)
    new_hash1 = generate_hash('site1_database.db')
    new_hash2 = generate_hash('site2_database.db')
    new_hash3 = generate_hash('site3_database.db')
    
    if new_hash1 == new_hash2 == new_hash3:
        print("-> TRẠNG THÁI: Đồng bộ")
    else:
        print("-> 🚨 CẢNH BÁO BẢO MẬT: ĐÃ PHÁT HIỆN SAI LỆCH DỮ LIỆU (STATE DIVERGENCE)!")
        if new_hash1 != new_hash2:
            print("-> Hệ thống chỉ ra: Mã băm của Site 2 không khớp với mạng lưới.")
        if new_hash1 != new_hash3:
            print("-> Hệ thống chỉ ra: Mã băm của Site 3 không khớp với mạng lưới.")

if __name__ == "__main__":
    simulate_distributed_network()  
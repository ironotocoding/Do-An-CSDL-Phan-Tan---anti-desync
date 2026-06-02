import sqlite3
from node_logic import generate_hash

SITES = {
    '1': 'site1_database.db',
    '2': 'site2_database.db',
    '3': 'site3_database.db',
}

def get_transactions(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transaction_Log ORDER BY timestamp ASC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return rows

def find_culprit():
    print("        RECONCILIATION TOOL: TỰ ĐỘNG TÌM SITE BỊ TẤN CÔNG\n")

    # Bước 1: Tính hash-chain của cả 3 site
    hashes = {sid: generate_hash(db) for sid, db in SITES.items()}
    print("Hash-Chain hiện tại:")
    for sid, h in hashes.items():
        print(f"  Site {sid}: {h[:30]}...")

    # Bước 2: Tự xác định site nào bị lệch
    # Logic: site bị hack có hash khác với 2 site còn lại
    hacked_site = None
    clean_site  = None

    for sid, h in hashes.items():
        others = [hashes[o] for o in SITES if o != sid]
        if others[0] == others[1] and h != others[0]:
            # sid này khác, 2 cái kia giống nhau → sid bị hack
            hacked_site = sid
        elif h == others[0] or h == others[1]:
            clean_site = sid  # Lấy 1 site sạch để so sánh

    if hacked_site is None:
        # Kiểm tra nếu cả 3 đều giống nhau
        all_h = list(hashes.values())
        if all_h[0] == all_h[1] == all_h[2]:
            print("\n Tất cả 3 site đồng bộ hoàn toàn. Không có sai lệch.")
        else:
            print("\n  Không xác định được rõ ràng site nào bị hack (có thể nhiều site bị tấn công).")
        return

    print(f"\n PHÁT HIỆN: Site {hacked_site} bị tấn công! (hash khác với Site {clean_site})\n")

    # Bước 3: So sánh giao dịch để tìm thủ phạm
    good_txs   = get_transactions(SITES[clean_site])
    hacked_txs = get_transactions(SITES[hacked_site])

    print(f"   Site {clean_site} (sạch)  : {len(good_txs)} giao dịch")
    print(f"   Site {hacked_site} (bị hack): {len(hacked_txs)} giao dịch")

    differences = [tx for tx in hacked_txs if tx not in good_txs]

    if differences:
        print("\n GIAO DỊCH GÂY RA SAI LỆCH (STATE DIVERGENCE):")
        for diff in differences:
            print(f"   -> ID: {diff[0]} | Sản phẩm ID: {diff[1]} | Hành động: {diff[2]} | Số lượng: {diff[3]} | Thời gian: {diff[4]}")
    else:
        print("\n  Không tìm thấy giao dịch lạ (site bị hack có ÍT giao dịch hơn site sạch).")

if __name__ == "__main__":
    find_culprit()


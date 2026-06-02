# Anti-Desync: Replica Consistency Verification via Hash-Chains

> **Topic #110 — Category 11** | Môn: Cơ sở Dữ liệu Phân tán

## Mô tả hệ thống

Hệ thống mô phỏng một cơ sở dữ liệu phân tán với **3 replica** của bảng `Product_Stock` (Kho hàng điện tử 20 sản phẩm). Mục tiêu: phát hiện tự động khi một replica bị tấn công và truy tìm chính xác giao dịch giả mạo.

- **Privacy Math:** Hash-Chain SHA-256 — mỗi giao dịch được băm cùng hash của giao dịch trước. Bất kỳ thay đổi nào cũng làm vỡ toàn bộ chuỗi.
- **Distributed Context:** 3 nodes Flask độc lập giao tiếp qua HTTP/REST API, kiểm tra chéo mã băm lẫn nhau.
- **Security Logic:** Daemon thread tự động tính lại Hash-Chain mỗi 10 phút. Nếu hash khác nhau → báo động **State Divergence**.
- **Reconciliation:** Majority Voting xác định node bị tấn công + Set Subtraction trích xuất giao dịch lậu.

---

## Lý do thực hiện đồ án & Vấn đề giải quyết

Trong các hệ thống phân tán thực tế (như ngân hàng, chuỗi cung ứng) sử dụng kiến trúc **Full Replication**, dữ liệu được nhân bản ở nhiều máy chủ khác nhau để dự phòng rủi ro. 
Tuy nhiên, điều này đặt ra một bài toán bảo mật lớn (Byzantine Fault): **Làm sao để hệ thống biết chắc chắn dữ liệu ở tất cả các máy chủ đều giống hệt nhau?** 

Nếu một hacker hoặc quản trị viên biến chất bí mật chỉnh sửa số liệu thẳng trên ổ cứng của **một** máy chủ vật lý, hệ thống sẽ bị rẽ nhánh dữ liệu (State Divergence). Các lớp bảo mật vòng ngoài (như Tường lửa, Phân quyền API) sẽ hoàn toàn vô dụng vì hacker thao tác trực tiếp ở tầng Storage.

**Đồ án này ra đời để giải quyết triệt để bài toán đó bằng 3 cốt lõi:**
1. **Kiểm toán từ bên trong (Hash-Chain):** Băm toàn bộ lịch sử giao dịch thành chuỗi liên kết. Nếu ổ cứng bị sửa dù chỉ 1 ký tự, toàn bộ chuỗi băm sẽ sai lệch.
2. **Tự động hóa & Phi tập trung (Decentralized):** Không cần con người, các máy chủ tự động kiểm tra chéo lẫn nhau định kỳ mỗi 10 phút.
3. **Phân xử bằng đồng thuận (Majority Voting):** Dùng nguyên lý Bỏ phiếu đa số để tự động cô lập máy bị hack và trích xuất chính xác giao dịch giả mạo.

---

## Cài đặt

```bash
pip install flask requests
```

---

## Cấu trúc Project

```
Đồ Án Phân Tán/
├── init_db.py           # Khởi tạo 3 databases đồng nhất (20 sản phẩm mẫu)
├── node_logic.py        # Thuật toán Hash-Chain (SHA-256) + ghi giao dịch
├── app.py               # Flask server cho mỗi node: API /hash, /sync + daemon 10 phút
├── start_all.py         # Khởi động đồng loạt 3 nodes (port 5001, 5002, 5003)
├── sync_check.py        # Hacker Mode: tấn công + mô phỏng phát hiện tự động
├── find_culprit.py      # Reconciliation Tool: Majority Voting + tìm giao dịch lậu
├── README.md

```

> **Lưu ý:** Các file `site*.db` được tạo tự động khi chạy `init_db.py`, không có trong repo.

---

## Hướng dẫn Demo 

### Bước 1 — Khởi tạo (chạy 1 lần đầu)
```bash
python init_db.py
```
Tạo 3 database với 20 sản phẩm mẫu giống hệt nhau.

### Bước 2 — Bật hệ thống phân tán
```bash
python start_all.py
```
Khởi động 3 nodes Flask tại port 5001, 5002, 5003. Mỗi node có daemon thread tự động hash mỗi 10 phút.

### Bước 3 — Kiểm tra đồng bộ qua Web API
Mở trình duyệt hoặc dùng curl:
```bash
# Hash của Node 1
curl http://127.0.0.1:5001/hash

# Kiểm tra đồng bộ toàn mạng
curl http://127.0.0.1:5001/sync
```
Kết quả: `"status": "ĐỒNG BỘ (SYNCED)"` với hash 3 máy giống hệt nhau.

### Bước 4 — Hacker Mode (Tạo lỗi Desync)
```bash
python sync_check.py
```
- Chọn Site bị tấn công (1, 2, hoặc 3)
- Nhập Product ID và số lượng hàng lậu bất kỳ
- Script mô phỏng 10 phút trôi qua → báo động **🚨 STATE DIVERGENCE**

### Bước 5 — Reconciliation (Truy tìm thủ phạm)
```bash
python find_culprit.py
```
- Tự động xác định node nào bị hack (Majority Voting)
- Trích xuất chính xác giao dịch lậu (ID, số lượng, thời gian)

### Bước 6 — Demo Node Offline (Tùy chọn)
Mở `start_all.py`, comment dòng Site 3, chạy lại. Vào `http://127.0.0.1:5001/sync` để thấy Node 3 hiển thị `"OFFLINE"`.

---

## Nguyên lý Hash-Chain

```
genesis_hash = "000...000"  (64 chữ số 0)
hash_1 = SHA256(genesis_hash + giao_dịch_1)
hash_2 = SHA256(hash_1       + giao_dịch_2)
hash_3 = SHA256(hash_2       + giao_dịch_3)
```

Hacker chèn bất kỳ giao dịch nào → `hash_cũ` thay đổi → toàn bộ chuỗi hash phía sau bị vỡ → hệ thống phát hiện ngay lập tức.

---

## Threat Model

| Mối đe dọa | Giải pháp |
|---|---|
| Chèn giao dịch lậu | Hash-Chain phát hiện (Avalanche Effect) |
| Không biết node nào bị hack | Majority Voting (2/3 đồng thuận) |
| Node bị tắt đột ngột | API trả về `"OFFLINE"`, không báo nhầm SYNCED |
| Không biết giao dịch nào là giả | Set Subtraction trên Transaction_Log |

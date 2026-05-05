# nhom10-Tran-Nguyen_Minh_Thanh
A* Pathfinding in Python
Giới thiệu

Chương trình sử dụng thuật toán A* để tìm đường đi tối ưu trên bản đồ dạng lưới (grid).
Có hỗ trợ nhiều loại địa hình với chi phí khác nhau.

Mô tả bản đồ
Giá trị	Ý nghĩa	Chi phí
0	Ô trống	1
1	Vật cản	Không đi được
2	Bùn	3
3	Đá	5
Nguyên lý

Thuật toán sử dụng công thức:

f(n) = g(n) + h(n)
g(n): chi phí từ điểm bắt đầu
h(n): khoảng cách ước lượng đến đích (Manhattan)
f(n): tổng chi phí
Cách chạy

Cài thư viện:

pip install numpy matplotlib

Chạy chương trình:

python bt.py
Kết quả
Tìm được đường đi từ start đến goal
In ra số bước và tổng chi phí
Hiển thị đường đi trên console và biểu đồ
File chính
bt.py: chứa toàn bộ thuật toán và chạy chương trình
Ghi chú
Thuật toán đảm bảo tìm đường tối ưu nếu heuristic phù hợp
Có thể mở rộng thêm di chuyển chéo hoặc bản đồ lớn hơn

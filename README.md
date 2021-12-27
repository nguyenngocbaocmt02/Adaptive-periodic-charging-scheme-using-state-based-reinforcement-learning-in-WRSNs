# GraphConstruction

thư mục data chứa các file dữ liệu để chạy  
network chứa các file giả lập hệ thống  
optimizer chứa các thuật toán tối ưu bao gồm 2 lớp thuật toán là ondemand và offline  
iostream chứa các luồng đọc ghi dữ liệu  
main chứa các mã sử dụng hệ thống  
các tham số mạng được triển khai trong file Parameter trong network

hệ thống chạy dựa trên một hệ thống quản lý thời gian rời rạc simpy  
Cài đặt: !pip install simpy  
Các optimizer kế thừa từ 2 optimizer chính là ondemandoptimizer và offlineoptimizer(Cần cài đặt dựa trên việc kế thừa 2
lớp này để có thể tương thích với việc cài đặt mạng, 2 thuật toán đơn giản ví dụ cho việc cài đặt là các thuật toán
random)

việc thiết lập mạng và cài đặt hệ thống quản trị thời gian được viết trong các file runner thuộc thư mục main(hiện tại
có 3 file runner tương ứng với 3 thuật toán cài đặt trong đó 2 thuật toán random mẫu và 1 thuật toán GraphRL)  
thuật toán hiện tại cài đặt trong thư mục optimizer\offlineoptimizer\GraphRL, pha Fuzzy hiện tại chưa hoàn thiện nên
việc tính Esafe được dựa trên hàm giảm tuyến tính, file FuzzyCS có thể bỏ qua, Vertex và StatusGraph chứa class đỉnh và
đồ thị



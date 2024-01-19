import numpy as np
import matplotlib.pyplot as plt

def kalman_filter(x_hat_prev, sigma_x_hat_prev, z, sigma_v, sigma_w):
    # Bước Dự Báo
    # Cập nhật trạng thái dự đoán
    x_hat_pred = x_hat_prev
    
    # Cập nhật độ lệch chuẩn của trạng thái dự đoán
    sigma_x_hat_pred = sigma_x_hat_prev + sigma_v + 1/sigma_w
    
    # Hệ số Kalman
    K = sigma_x_hat_prev / (sigma_x_hat_prev + sigma_w)
    
    # Bước Dự Báo - Cập nhật trạng thái dự đoán và độ lệch chuẩn của nó
    x_hat = x_hat_pred + K * (z - x_hat_pred)
    sigma_x_hat = (1 - K) * sigma_x_hat_pred
    
    return x_hat, sigma_x_hat

# Số lượng giá trị ngẫu nhiên
num_values = 5

# Tạo mảng ngẫu nhiên từ phân phối chuẩn (Gaussian)
z_values = np.random.randn(num_values)

# Thử nghiệm với bộ lọc Kalman cho mỗi giá trị trong mảng z_values
x_hat_prev = 0
sigma_x_hat_prev = 1
sigma_v = 0.1
sigma_w = 0.1

# Lưu trữ kết quả
x_hat_results = []
sigma_x_hat_results = []

# Áp dụng bộ lọc Kalman cho từng giá trị z và lưu kết quả
for z in z_values:
    x_hat_prev, sigma_x_hat_prev = kalman_filter(x_hat_prev, sigma_x_hat_prev, z, sigma_v, sigma_w)
    x_hat_results.append(x_hat_prev)
    sigma_x_hat_results.append(sigma_x_hat_prev)

# Vẽ biểu đồ
time_steps = range(num_values)
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time_steps, x_hat_results, label='Trạng thái ước lượng')
plt.title('Trạng thái ước lượng qua thời gian')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time_steps, sigma_x_hat_results, label='Độ lệch chuẩn')
plt.title('Độ lệch chuẩn qua thời gian')
plt.legend()

plt.tight_layout()
plt.show()

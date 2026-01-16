import random
import math
import cmath

# 1. HÀM MỤC TIÊU
def objective_function(sol):
    """
    Hàm mục tiêu f1: Thiết kế búp sóng theo GLS.
    Mục tiêu: Min || A * w - v ||^2
    Input: sol là danh sách các GÓC PHA (radian).
    """
    
    # 1. Cấu hình giả lập
    M = len(sol)            # Số phần tử ăng-ten
    v_desired = 1.0 + 0j 
    
    # Ma trận lái A tại hướng 0 độ=
    A_row = [1.0 + 0j for _ in range(M)]
    
    # 2. Chuyển đổi từ Góc pha (sol) sang Trọng số phức (w)
    amplitude = 1.0 / math.sqrt(M)
    
    y_actual = complex(0, 0)
    for i in range(M):
        # w_i = amplitude * e^(j * phi_i)
        w_i = complex(amplitude * math.cos(sol[i]), amplitude * math.sin(sol[i]))
        y_actual += A_row[i] * w_i
        
    # 3. Tính sai số bình phương
    diff = y_actual - v_desired
    return (diff.real ** 2) + (diff.imag ** 2)

# Hàm fitness (Giữ nguyên)
def calculate_fitness(f_value):
    if f_value >= 0:
        return 1.0 / (1.0 + f_value)
    else:
        return 1.0 + abs(f_value)

if __name__ == "__main__":

    # 2. THAM SỐ & SỐ CHIỀU
    D = 4                # Số phần tử ăng-ten
    SN = 20
    food_number = SN // 2
    limit = 30
    max_cycle = 2000
    
    # Cập nhật miền tìm kiếm cho GÓC PHA (radian) [-pi, pi]
    LB = -math.pi
    UB = math.pi

    x = []
    f = [0.0] * food_number
    fit = [0.0] * food_number
    trial = [0] * food_number

    # KHỞI TẠO
    random.seed()
    for i in range(food_number):
        row = [random.uniform(LB, UB) for _ in range(D)]
        x.append(row)
        f[i] = objective_function(x[i])
        fit[i] = calculate_fitness(f[i])

    # Tìm best ban đầu
    best_solution = x[0][:]
    best_value = f[0]

    # Cập nhật best lần đầu
    for i in range(food_number):
        if f[i] < best_value:
            best_value = f[i]
            best_solution = x[i][:]

    # VÒNG LẶP CHÍNH qABC
    for cycle in range(1, max_cycle + 1):

        # --- Employed Bees (Ong Thợ) ---
        for i in range(food_number):
            
            v = x[i][:]
            j = random.randint(0, D - 1)
            phi = random.uniform(-1, 1)

            # CÔNG THỨC qABC
            v[j] = best_solution[j] + phi * (best_solution[j] - x[i][j])

            # Kiểm tra biên [-pi, pi]
            v[j] = max(LB, min(UB, v[j]))

            f_v = objective_function(v)
            fit_v = calculate_fitness(f_v)

            if fit_v > fit[i]:
                x[i] = v
                f[i] = f_v
                fit[i] = fit_v
                trial[i] = 0
            else:
                trial[i] += 1

        # --- Onlooker Bees (Ong Quan Sát) ---
        total_fit = sum(fit)
        for t in range(food_number):
            r = random.uniform(0, total_fit)
            acc = 0
            selected_i = 0
            for idx in range(food_number):
                acc += fit[idx]
                if acc >= r:
                    selected_i = idx
                    break
            
            i = selected_i
            
            # qABC: Ong quan sát cũng áp dụng cơ chế học tập từ Best Neighbor
            v = x[i][:]
            j = random.randint(0, D - 1)
            phi = random.uniform(-1, 1)

            # --- CÔNG THỨC qABC ---
            v[j] = best_solution[j] + phi * (best_solution[j] - x[i][j])
            
            # Kiểm tra biên
            v[j] = max(LB, min(UB, v[j]))

            f_v = objective_function(v)
            fit_v = calculate_fitness(f_v)

            if fit_v > fit[i]:
                x[i] = v
                f[i] = f_v
                fit[i] = fit_v
                trial[i] = 0
            else:
                trial[i] += 1

        # --- Scout Bees (Ong Trinh Sát) ---
        for i in range(food_number):
            if trial[i] > limit:
                x[i] = [random.uniform(LB, UB) for _ in range(D)]
                f[i] = objective_function(x[i])
                fit[i] = calculate_fitness(f[i])
                trial[i] = 0

        # --- Cập nhật Best Solution ---
        for i in range(food_number):
            if f[i] < best_value:
                best_value = f[i]
                best_solution = x[i][:]

    # IN KẾT QUẢ
    print(f"Best value found = {best_value}")
    print("Best solution (Phase angles):", end=" ")
    for val in best_solution:
        print(f"{val:.5f} ", end="")
    print()
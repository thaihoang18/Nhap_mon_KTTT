import random
import math
import cmath 

# 1. HÀM MỤC TIÊU
def objective_function(sol):
    """
    Hàm mục tiêu: Thiết kế búp sóng theo nguyên lý GLS.
    Mục tiêu: Min || A * w - v ||^2
    """
    
    # --- THÔNG SỐ GIẢ LẬP (Mô phỏng ví dụ Section 5.1 PDF) ---
    M = len(sol)  # Số phần tử ăng-ten (tương ứng số chiều D)
    
    A_row = [1.0 + 0j for _ in range(M)]
    v_desired = 1.0 + 0j
    
    # --- TÍNH TOÁN TRỌNG SỐ VÀ SAI SỐ ---
  
    amplitude = 1.0 / math.sqrt(M)
    w = []
    for phase in sol:
        # w = amp * (cos(phi) + j*sin(phi))
        val = complex(amplitude * math.cos(phase), amplitude * math.sin(phase))
        w.append(val)
        
    # 4. Tính đáp ứng thực tế: y = A * w
    y_actual = complex(0, 0)
    for k in range(M):
        y_actual += A_row[k] * w[k]
        
    # 5. Tính hàm mục tiêu (Sai số bình phương)
    diff = y_actual - v_desired
    f_val = (diff.real ** 2) + (diff.imag ** 2)
    
    return f_val

# Hàm fitness
def calculate_fitness(f_value):
    if f_value >= 0:
        return 1.0 / (1.0 + f_value)
    else:
        return 1.0 + abs(f_value)

if __name__ == "__main__":

    # 2. THAM SỐ THUẬT TOÁN
    D = 4                # Số phần tử ăng-ten (M=4)
    SN = 20
    food_number = SN // 2
    limit = 30
    max_cycle = 2000

    # Miền tìm kiếm cho góc pha: [-pi, pi] 
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

    for i in range(food_number):
        if f[i] < best_value:
            best_value = f[i]
            best_solution = x[i][:]

    # VÒNG LẶP CHÍNH ABC
    for cycle in range(1, max_cycle + 1):

        # --- Employed Bees (Ong Thợ) ---
        for i in range(food_number):
            while True:
                k = random.randint(0, food_number - 1)
                if k != i: break
            
            v = x[i][:]
            j = random.randint(0, D - 1)
            phi = random.uniform(-1, 1)

            # Công thức ABC chuẩn
            v[j] = x[i][j] + phi * (x[i][j] - x[k][j])
            
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
            while True:
                k = random.randint(0, food_number - 1)
                if k != i: break
            
            v = x[i][:]
            j = random.randint(0, D - 1)
            phi = random.uniform(-1, 1)

            v[j] = x[i][j] + phi * (x[i][j] - x[k][j])
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
    print(f"Best Error (Min Objective) = {best_value}")
    print("Best Phase Angles (radians):", end=" ")
    for val in best_solution:
        print(f"{val:.5f} ", end="")
    print()
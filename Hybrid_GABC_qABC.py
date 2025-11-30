import random
import math

# ==========================================
# 1. HÀM MỤC TIÊU
# ==========================================
def objective_function(sol):
    # Công thức: x_1.x_2 + x_3^2 + x_4^3
    # Ánh xạ: x1->sol[0], x2->sol[1], x3->sol[2], x4->sol[3]
    
    x1 = sol[0]
    x2 = sol[1]
    x3 = sol[2]
    x4 = sol[3]
    
    return (x1 * x2) + (x3 ** 2) + (x4 ** 3)

# Hàm fitness
def calculate_fitness(f_value):
    if f_value >= 0:
        return 1.0 / (1.0 + f_value)
    else:
        return 1.0 + abs(f_value)

if __name__ == "__main__":
    # ==========================================
    # 2. THAM SỐ & SỐ CHIỀU
    # ==========================================
    D = 4                # Vì công thức có x1, x2, x3, x4
    SN = 20
    food_number = SN // 2
    limit = 30
    max_cycle = 2000
    
    # --- THAM SỐ CHO HYBRID ---
    C = 1.5              # Hằng số điều khiển cho phần GABC
    
    LB = -10.0
    UB = 10.0

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

    # VÒNG LẶP CHÍNH HYBRID GABC - qABC
    for cycle in range(1, max_cycle + 1):

        # --- Employed Bees (Ong Thợ) ---
        for i in range(food_number):
            v = x[i][:]
            j = random.randint(0, D - 1)
            
            # Tham số ngẫu nhiên
            phi = random.uniform(-1, 1)  # Cho phần qABC
            psi = random.uniform(0, C)   # Cho phần GABC

            # --- CÔNG THỨC HYBRID GABC - qABC ---
            # v_{ij} = x_{best,j} + phi*(x_{best,j} - x_{ij}) + psi*(y_j - x_{ij})
            # Ở đây best_solution đóng vai trò là cả Best Neighbor (qABC) và Global Best (GABC)
            
            term_qabc = best_solution[j] + phi * (best_solution[j] - x[i][j])
            term_gabc = psi * (best_solution[j] - x[i][j])
            
            v[j] = term_qabc + term_gabc

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

        # --- Onlooker Bees (Ong Quan Sát) ---
        total_fit = sum(fit)
        for t in range(food_number):
            # Cơ chế Roulette Wheel
            r = random.uniform(0, total_fit)
            acc = 0
            selected_i = 0
            for idx in range(food_number):
                acc += fit[idx]
                if acc >= r:
                    selected_i = idx
                    break
            
            i = selected_i
            
            v = x[i][:]
            j = random.randint(0, D - 1)
            
            # Tham số ngẫu nhiên
            phi = random.uniform(-1, 1)
            psi = random.uniform(0, C)

            # --- CÔNG THỨC HYBRID GABC - qABC ---
            # Áp dụng tương tự cho Ong Quan Sát
            
            term_qabc = best_solution[j] + phi * (best_solution[j] - x[i][j])
            term_gabc = psi * (best_solution[j] - x[i][j])
            
            v[j] = term_qabc + term_gabc
            
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
    print("Best solution (x1, x2, x3, x4):", end=" ")
    for val in best_solution:
        print(f"{val:.5f} ", end="")
    print()
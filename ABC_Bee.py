# Your first line of Python code
import random
import math

# Hàm mục tiêu
def objective_function(sol):
    return sum(val * val for val in sol)

# Hàm fitness
def calculate_fitness(f_value):
    if f_value >= 0:
        return 1.0 / (1.0 + f_value)
    else:
        return 1.0 + abs(f_value)

if __name__ == "__main__":
    # Tham số thuật toán
    D = 5
    SN = 20
    food_number = SN // 2
    limit = 30
    max_cycle = 2000

    LB = -10.0
    UB = 10.0

    x = []
    f = [0.0] * food_number
    fit = [0.0] * food_number
    trial = [0] * food_number

    # 1. KHỞI TẠO
    random.seed()
    for i in range(food_number):
        row = [random.uniform(LB, UB) for _ in range(D)]
        x.append(row)
        f[i] = objective_function(x[i])
        fit[i] = calculate_fitness(f[i])

    # Tìm best ban đầu
    best_solution = x[0][:]
    best_value = f[0]

    # Cập nhật best lần đầu (Viết trực tiếp, không dùng hàm con)
    for i in range(food_number):
        if f[i] < best_value:
            best_value = f[i]
            best_solution = x[i][:]

    # 2. VÒNG LẶP CHÍNH ABC
    for cycle in range(1, max_cycle + 1):

        # --- Employed Bees ---
        for i in range(food_number):
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

        # --- Onlooker Bees ---
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

        # --- Scout Bees ---
        for i in range(food_number):
            if trial[i] > limit:
                x[i] = [random.uniform(LB, UB) for _ in range(D)]
                f[i] = objective_function(x[i])
                fit[i] = calculate_fitness(f[i])
                trial[i] = 0

        # --- Cập nhật Best Solution (SỬA LỖI TẠI ĐÂY) ---
        # Thay vì gọi hàm update_global_best(), ta viết vòng lặp trực tiếp
        for i in range(food_number):
            if f[i] < best_value:
                best_value = f[i]
                best_solution = x[i][:]

    # IN KẾT QUẢ
    print(f"Best value found = {best_value}")
    print("Best solution:", end=" ")
    for val in best_solution:
        print(f"{val} ", end="")
    print()
'''
Khởi tạo quần thể: Tạo N cá thể (mỗi cá thể là danh sách 8 vị trí quân xe, 1 quân trên mỗi hàng).

Fitness: Dùng heuristic (tổng Manhattan distance theo cột). Càng nhỏ càng tốt.

Chọn lọc: Tournament selection hoặc roulette.

Lai ghép (crossover): Trộn hai cha mẹ để tạo con.

Đột biến: Ngẫu nhiên thay đổi vị trí 1 quân trong 1 cá thể.

Lặp lại cho tới khi tìm ra goal hoặc đạt số thế hệ max.
'''


import tkinter as tk
import random

# ================== GOAL ==================
goal_cols = [0, 1, 2, 3, 5, 4, 7, 6]   # cột đích cho từng hàng
goal = [(r, goal_cols[r]) for r in range(8)]

# ================== heuristic (Manhattan theo cột) ==================
def heuristic(vt, goal):
    return sum(abs(c - gc) for (_, c), (_, gc) in zip(vt, goal))

# ================== Genetic Algorithm ==================
def genetic_algorithm(goal, pop_size=100, generations=500, mutation_rate=0.2):
    # khởi tạo ngẫu nhiên
    def random_individual():
        return [(r, random.randint(0, 7)) for r in range(8)]

    def fitness(ind):
        return heuristic(ind, goal)

    def crossover(p1, p2):
        cut = random.randint(1, 7)
        child = p1[:cut] + p2[cut:]
        return child

    def mutate(ind):
        r = random.randint(0, 7)
        c_new = random.randint(0, 7)
        ind[r] = (r, c_new)
        return ind

    # khởi tạo quần thể
    population = [random_individual() for _ in range(pop_size)]
    steps = []

    for gen in range(generations):
        # đánh giá
        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda x: x[1])
        best, best_fit = scored[0]
        steps.append((best[:], best_fit))

        if best == goal:
            print(f"Đạt mục tiêu với GA ở thế hệ {gen}!")
            break

        # chọn lọc (nửa tốt nhất)
        parents = [ind for ind, _ in scored[:pop_size // 2]]

        # tạo thế hệ mới
        children = []
        while len(children) < pop_size:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1[:], p2[:])
            if random.random() < mutation_rate:
                child = mutate(child)
            children.append(child)

        population = children

    return steps

# ================== GIAO DIỆN ==================
def Quan_Xe():
    global game

    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="MÔ TẢ GENETIC ALGORITHM", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=1, columnspan=6)
        for i in range(8):
            tk.Label(master, text=f"     {8 - i}", font=("Arial", 12)).grid(row=i + 1, column=0)
            tk.Label(master, text=f"     {8 - i}", font=("Arial", 12)).grid(row=i + 1, column=10)
            tk.Label(master, text="   ").grid(row=i + 1, column=9)
            tk.Label(master, text=B[i], font=("Arial", 12)).grid(row=9, column=i + 1)
            tk.Label(master, text=B[i], font=("Arial", 12)).grid(row=9, column=i + 11)
            for j in range(8):
                color = "#a7dcfa" if (i - j) % 2 == 0 else "#416072"
                tk.Label(master, width=cell_size[0], height=cell_size[1],
                         bg=color, relief="flat", bd=0).grid(row=i + 1, column=j + 1)
                tk.Label(master, width=cell_size[0], height=cell_size[1],
                         bg=color, relief="flat", bd=0).grid(row=i + 1, column=j + 11)

    def replace(row, col, X):
        if board_labels[row][col] is not None:
            try:
                board_labels[row][col].destroy()
            except Exception:
                pass
            board_labels[row][col] = None
        bg_color = "#a7dcfa" if (row - col) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text=X, font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=row + 1, column=col + 1)
        board_labels[row][col] = lbl

    def move(step=None):
        nonlocal current_step, paused
        if not all_logs:
            return
        if step is not None:
            current_step = step
        if paused:
            return
        if current_step >= len(all_logs):
            return

        current, h_val = all_logs[current_step]

        # xóa quân cũ
        for r in range(8):
            for c in range(8):
                if board_labels[r][c] is not None:
                    board_labels[r][c].destroy()
                    board_labels[r][c] = None

        # vẽ quân mới
        for (r, c) in current:
            replace(r, c, "♜")

        current_step += 1
        game.after(800, move)

    def play():
        nonlocal paused
        paused = False
        move()

    def pause():
        nonlocal paused
        paused = True

    def restart():
        nonlocal current_step, paused, all_logs
        all_logs = genetic_algorithm(goal)
        current_step = 0
        paused = False
        move(0)

    root.withdraw()
    try:
        game.destroy()
    except Exception:
        pass

    game = tk.Toplevel()
    game.geometry(f"1300x700+{(root.winfo_screenwidth() - 1300) // 2}+{(root.winfo_screenheight() - 700) // 2}")
    game.title("8 Quân Xe - Genetic Algorithm")

    draw_board(game)

    all_logs = genetic_algorithm(goal)

    global board_labels
    board_labels = [[None for _ in range(8)] for _ in range(8)]

    # vẽ trạng thái goal ở bên phải
    for (r, c) in goal:
        bg_color = "#a7dcfa" if (r - c) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text="♜", font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=r + 1, column=c + 1 + 10)

    btn_play = tk.Button(game, text="▶ Chạy", font=("Arial", 12, "bold"),
                         command=play, bg="#4CAF50", fg="white", width=11)
    btn_play.grid(row=11, column=1, padx=4, columnspan=2)

    btn_pause = tk.Button(game, text="⏸ Tạm dừng", font=("Arial", 12, "bold"),
                          command=pause, bg="#FF9800", fg="white", width=11)
    btn_pause.grid(row=11, column=3, padx=4, columnspan=2)

    btn_restart = tk.Button(game, text="🔄 Bắt đầu lại", font=("Arial", 12, "bold"),
                            command=restart, bg="#F44336", fg="white", width=11)
    btn_restart.grid(row=11, column=5, padx=4, columnspan=2)

    paused = False
    current_step = 0
    move(0)

    def close():
        try:
            game.destroy()
        except:
            pass
        try:
            root.destroy()
        except:
            pass
    game.protocol("WM_DELETE_WINDOW", close)

# ================== MAIN ==================
root = tk.Tk()
root.withdraw()
Quan_Xe()
root.mainloop()


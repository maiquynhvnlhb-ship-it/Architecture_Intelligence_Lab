import tkinter as tk
import heapq

# ================== GOAL ==================
goal_cols = [0, 1, 2, 3, 5, 4, 7, 6]
goal = [(r, goal_cols[r]) for r in range(8)]

# ================== HÀM TÍNH g(n): SỐ CONFLICT ==================
def conflict_cost(vt):
    conflicts = 0
    for i in range(len(vt)):
        for j in range(i+1, len(vt)):
            if vt[i][1] == vt[j][1]:  # cùng cột thì conflict
                conflicts += 1
    return conflicts

# ================== HÀM TÍNH h(n): heuristic (Manhattan distance) ==================
def cost_place_rook(vt, new_col, goal):
    row = len(vt)
    new_state = vt + [(row, new_col)]
    dist = 0
    for i, (r, c) in enumerate(new_state):
        gr, gc = goal[i]
        dist += abs(r - gr) + abs(c - gc)
    return dist

# ================== A* SEARCH ==================
def A_star(goal):
    pq = []
    heapq.heappush(pq, (0, 0, []))  # (f, g, state)
    visited = set()
    steps = []

    while pq:
        f, g, vt = heapq.heappop(pq)
        state_key = tuple(vt)
        if state_key in visited:
            continue
        visited.add(state_key)

        if len(vt) > 0:
            steps.append((vt[:], f))

        if vt == goal:
            return steps

        row = len(vt)
        if row < 8:
            for c in range(8):
                new_state = vt + [(row, c)]
                g_new = conflict_cost(new_state)   # g(n) = số conflict
                h = cost_place_rook(vt, c, goal)   # h(n) = heuristic
                f_new = g_new + h
                heapq.heappush(pq, (f_new, g_new, new_state))

    return steps

# ================== GIAO DIỆN ==================
def Quan_Xe():
    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="MÔ TẢ GSF TRONG BÀI TOÁN", font=("Arial", 15, "bold"),
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
        if board_labels[row][col]:
            board_labels[row][col].destroy()
        bg_color = "#a7dcfa" if (row - col) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text=X, font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=row + 1, column=col + 1)
        board_labels[row][col] = lbl

    def move(step=None):
        nonlocal current_step, paused
        if step is not None:
            current_step = step

        if paused:
            return
        if current_step >= len(all_logs):
            return

        current, cost = all_logs[current_step]

        # xóa quân cũ
        for r in range(8):
            for c in range(8):
                replace(r, c, "")

        # vẽ quân hiện tại
        for (r, c) in current:
            replace(r, c, "♜")



        current_step += 1
        game.after(1000, move)

    def play():
        nonlocal paused
        paused = False
        move()

    def pause():
        nonlocal paused
        paused = True

    def restart():
        nonlocal current_step, paused
        current_step = 0
        paused = False
        move(0)

    root.withdraw()
    global game
    try:
        game.destroy()
    except:
        pass

    game = tk.Toplevel()
    game.geometry(f"1300x700+{(root.winfo_screenwidth() - 1300) // 2}+{(root.winfo_screenheight() - 700) // 2}")
    game.title("8 Quân Xe - GSF")

    draw_board(game)
    all_logs = A_star(goal)

    global board_labels
    board_labels = [[None for _ in range(8)] for _ in range(8)]

    # hiển thị goal bên phải
    for (r, c) in goal:
        bg_color = "#a7dcfa" if (r - c) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text="♜", font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=r + 1, column=c + 1 + 10)


    # nút điều khiển
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
        game.destroy()
        root.destroy()
    game.protocol("WM_DELETE_WINDOW", close)


# ================== MAIN ==================
root = tk.Tk()
root.withdraw()
Quan_Xe()
root.mainloop()

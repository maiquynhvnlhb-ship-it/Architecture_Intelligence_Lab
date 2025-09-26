import tkinter as tk
import random

# ================== GOAL ==================
goal_cols = [0, 1, 2, 3, 5, 4, 7, 6]   # cột đích cho từng hàng
goal = [(r, goal_cols[r]) for r in range(8)]

# ================== heuristic (Manhattan theo cột) ==================
def heuristic(vt, goal):
    return sum(abs(c - gc) for (_, c), (_, gc) in zip(vt, goal))

# ================== Beam Search ==================
def beam_search(goal, beam_width=5, max_steps=500):
    def random_start():
        return [(r, random.randint(0, 7)) for r in range(8)]

    def neighbors(state):
        neighs = []
        for r in range(8):
            c_now = state[r][1]
            for c in range(8):
                if c != c_now:
                    new_state = state[:]
                    new_state[r] = (r, c)
                    neighs.append(new_state)
        return neighs

    steps = []
    frontier = [random_start()]  # danh sách trạng thái ban đầu

    for step in range(max_steps):
        scored = [(s, heuristic(s, goal)) for s in frontier]
        scored.sort(key=lambda x: x[1])
        best, best_h = scored[0]
        steps.append((best[:], best_h))

        if best == goal:
            print(f"Đạt mục tiêu với Beam Search ở bước {step}!")
            break

        # sinh tất cả neighbor của frontier
        all_candidates = []
        for s in frontier:
            all_candidates.extend(neighbors(s))

        # chọn beam_width trạng thái tốt nhất
        scored = [(s, heuristic(s, goal)) for s in all_candidates]
        scored.sort(key=lambda x: x[1])
        frontier = [s for s, _ in scored[:beam_width]]

    return steps

# ================== GIAO DIỆN ==================
def Quan_Xe():
    global game

    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="MÔ TẢ BEAM SEARCH", font=("Arial", 15, "bold"),
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
        all_logs = beam_search(goal)
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
    game.title("8 Quân Xe - Beam Search")

    draw_board(game)

    all_logs = beam_search(goal)

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

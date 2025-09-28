import tkinter as tk
import itertools
import random

# ================== MỤC TIÊU ==================
N = 8
goal_cols = [2, 1, 5, 3, 0, 4, 7, 6]
goal_tuple = tuple(goal_cols)

# ================== HEURISTIC ==================
def heuristic(state, goal=goal_tuple):
    return sum(abs(c - gc) for c, gc in zip(state, goal))

# ================== SINH TRẠNG THÁI BAN ĐẦU ==================
def initial_belief_states(sample_size=200):
    """Lấy mẫu ngẫu nhiên các hoán vị ban đầu"""
    all_states = list(itertools.permutations(range(N)))
    return random.sample(all_states, min(sample_size, len(all_states)))

def successors(state):
    """Trả về list các (action, result_state)"""
    neighs = []
    for r in range(N):
        c_now = state[r]
        for c in range(N):
            if c != c_now:
                lst = list(state)
                lst[r] = c
                neighs.append(((r, c), tuple(lst)))
    neighs.sort(key=lambda ac: heuristic(ac[1], goal_tuple))
    return neighs

# ================== GREEDY BELIEF-STATE SEARCH ==================
def greedy_belief_search(belief_states, goal=goal_tuple, max_steps_log=200):
    steps_log = []
    plan = []
    step = 0

    while belief_states and step < max_steps_log:
        # Chọn state tốt nhất theo heuristic
        best_state = min(belief_states, key=lambda s: heuristic(s, goal))
        steps_log.append(([(r, best_state[r]) for r in range(N)], heuristic(best_state, goal)))

        # Kiểm tra goal
        if best_state == goal:
            return steps_log, plan

        # Chọn action tốt nhất cho state đại diện
        actions = successors(best_state)
        if not actions:
            break

        best_action, _ = actions[0]
        plan.append(('move', best_action))

        # Cập nhật belief states theo action chọn
        new_belief = []
        for state in belief_states:
            for action, next_state in successors(state):
                if action == best_action:
                    new_belief.append(next_state)
        belief_states = new_belief
        step += 1

    return steps_log, plan


# ================== wrapper / GUI ==================
def run_greedy_wrapper(goal_param):
    belief_states = initial_belief_states(sample_size=200)
    return greedy_belief_search(belief_states, goal=goal_param, max_steps_log=200)

# ================== In cây kế hoạch dễ đọc ==================
def print_plan(plan, indent=0):
    space = "  " * indent
    if plan is None:
        print(space + "❌ Không tìm thấy kế hoạch")
    elif plan == []:
        print(space + "✅ Goal")
    elif isinstance(plan, list):
        for step in plan:
            _, action = step
            r, c = action
            print(f"{space}→ Hành động: di chuyển hàng {r} → cột {c}")
    else:
        print(space + repr(plan))

# ================== GUI ==================
def Quan_Xe():
    global game

    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="MÔ TẢ GREEDY BELIEF-STATE SEARCH", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=1, columnspan=6)
        for i in range(N):
            tk.Label(master, text=f"     {N - i}", font=("Arial", 12)).grid(row=i + 1, column=0)
            tk.Label(master, text=f"     {N - i}", font=("Arial", 12)).grid(row=i + 1, column=10)
            tk.Label(master, text="   ").grid(row=i + 1, column=9)
            tk.Label(master, text=B[i], font=("Arial", 12)).grid(row=N + 1, column=i + 1)
            tk.Label(master, text=B[i], font=("Arial", 12)).grid(row=N + 1, column=i + 11)
            for j in range(N):
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
        for r in range(N):
            for c in range(N):
                if board_labels[r][c] is not None:
                    board_labels[r][c].destroy()
                    board_labels[r][c] = None
        for (r, c) in current:
            replace(r, c, "♜")
        current_step += 1
        game.after(300, move)

    def play():
        nonlocal paused
        paused = False
        move()

    def pause():
        nonlocal paused
        paused = True

    def restart():
        nonlocal current_step, paused, all_logs
        all_logs, plan = run_greedy_wrapper(goal_tuple)
        print("\n===== Greedy Belief-State Plan =====")
        print_plan(plan)
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
    game.title("8 Quân Xe - GREEDY Belief-State Search")

    draw_board(game)

    all_logs, plan = run_greedy_wrapper(goal_tuple)
    print("\n===== Greedy Belief-State Plan =====")
    print_plan(plan)

    global board_labels
    board_labels = [[None for _ in range(N)] for _ in range(N)]

    for r, c in enumerate(goal_cols):
        bg_color = "#a7dcfa" if (r - c) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text="♜", font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=r + 1, column=c + 1 + 10)

    btn_play = tk.Button(game, text="▶ Chạy", font=("Arial", 12, "bold"),
                         command=play, bg="#4CAF50", fg="white", width=11)
    btn_play.grid(row=N + 3, column=1, padx=4, columnspan=2)

    btn_pause = tk.Button(game, text="⏸ Tạm dừng", font=("Arial", 12, "bold"),
                          command=pause, bg="#FF9800", fg="white", width=11)
    btn_pause.grid(row=N + 3, column=3, padx=4, columnspan=2)

    btn_restart = tk.Button(game, text="🔄 Bắt đầu lại", font=("Arial", 12, "bold"),
                            command=restart, bg="#F44336", fg="white", width=11)
    btn_restart.grid(row=N + 3, column=5, padx=4, columnspan=2)

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

import tkinter as tk
import random

# ================== MỤC TIÊU ==================
goal_cols = [2, 1, 5, 3, 0, 4, 7, 6]
goal_tuple = tuple(goal_cols)

# ================== HEURISTIC ==================
def heuristic(state, goal=goal_tuple):
    return sum(abs(c - gc) for c, gc in zip(state, goal))

# ================== SINH TRẠNG THÁI ==================
def random_start():
    return tuple(random.randint(0, 7) for _ in range(8))

def successors(state):
    """
    Trả về list các (action, result_state)
    - action: (row, new_col)
    - result_state: tuple trạng thái sau khi thực hiện action
    Sắp xếp theo heuristic(result_state) tăng dần
    """
    neighs = []
    for r in range(8):
        c_now = state[r]
        for c in range(8):
            if c != c_now:
                lst = list(state)
                lst[r] = c
                neighs.append(((r, c), tuple(lst)))
    # sort theo heuristic của state kết quả (ưu tiên hành động tốt hơn)
    neighs.sort(key=lambda ac: heuristic(ac[1], goal_tuple))
    # if branch_limit and len(neighs) > branch_limit:
    #     return neighs[:branch_limit]
    return neighs

# ================== AND–OR SEARCH CHUẨN ==================
def and_or_search(initial_state, goal=goal_tuple, max_depth=40, max_steps_log=800, branch_limit=12):
    """
    Trả về: (steps_log, plan)
    - steps_log: list of (visual_state_list, h) để GUI vẽ
    - plan: conditional plan (None nếu không tìm được)
    Plan representation:
      - [] : goal (đã đạt)
      - ('move', action, {result_state: plan_for_result, ...}) : conditional plan
    """
    steps_log = []

    # memoization: cache các state đã được xác định thành công/thất bại
    memo_success = {}  # state -> plan (khi state có plan)
    memo_fail = set()  # state đã biết thất bại

    def visual_state(state):
        return [(r, state[r]) for r in range(8)]

    def OR_SEARCH(state, path_set, depth):
        """
        OR node: chọn 1 action từ state sao cho AND-SEARCH(results(action)) thành công.
        Trả về plan nếu tìm được, ngược lại None.
        """
        # Log cho GUI (giới hạn số log)
        if len(steps_log) < max_steps_log:
            steps_log.append((visual_state(state), heuristic(state, goal)))

        # Goal test
        if state == goal:
            return []  # plan rỗng = success

        # Depth limit
        if depth > max_depth:
            return None

        # Cycle detection theo path hiện tại
        if state in path_set:
            return None

        # Nếu đã biết thất bại trước đó -> prune
        if state in memo_fail:
            return None

        # Nếu đã biết kế hoạch thành công → trả về trực tiếp
        if state in memo_success:
            return memo_success[state]

        # Thử từng hành động (OR: chọn action)
        actions = successors(state)
        for action, result_state in actions:
            # Với action này, lấy tập các kết quả (ở bài này deterministic -> danh sách 1 phần tử)
            results = [result_state]
            new_path = set(path_set)
            new_path.add(state)
            plan_for_action = AND_SEARCH(results, new_path, depth + 1)
            if plan_for_action is not None:
                # Thành công: lưu vào memo và trả về plan dạng ('move', action, dict_results->plan)
                plan = ('move', action, plan_for_action)
                memo_success[state] = plan
                return plan

        # Nếu không action nào thành công -> đánh dấu fail
        memo_fail.add(state)
        return None

    def AND_SEARCH(results, path_set, depth):
        """
        AND node: với 1 action có thể có nhiều possible results (non-deterministic).
        Phải tìm plan cho từng result. Nếu mọi result có plan, trả về dict mapping result->plan.
        Nếu có 1 result không có plan -> fail (None).
        """
        plans = {}
        for s in results:
            plan_s = OR_SEARCH(s, path_set, depth)
            if plan_s is None:
                return None
            plans[s] = plan_s
        return plans

    final_plan = OR_SEARCH(initial_state, set(), 0)
    return steps_log, final_plan

# ================== In cây kế hoạch dễ đọc ==================
def print_plan(plan, indent=0):
    space = "  " * indent
    if plan is None:
        print(space + "❌ Không tìm thấy kế hoạch")
    elif plan == []:
        print(space + "✅ Goal")
    elif isinstance(plan, tuple) and plan[0] == 'move':
        _, action, subplan = plan
        r, c = action
        print(f"{space}→ Hành động: di chuyển hàng {r} → cột {c}")
        if isinstance(subplan, dict):
            for res_state, p in subplan.items():
                print(f"{space}  Nếu kết quả = {res_state}:")
                print_plan(p, indent + 2)
        else:
            # unexpected shape nhưng vẫn in an toàn
            print_plan(subplan, indent + 1)
    elif isinstance(plan, dict):
        for s, p in plan.items():
            print(f"{space}[Kết quả trung gian {s}]")
            print_plan(p, indent + 1)
    else:
        print(space + repr(plan))

# ================== wrapper / GUI giữ nguyên tên ==================
def beam_search(goal_param, beam_width=5, max_steps=500):
    # giữ tên để GUI cũ gọi được; trả về same signature as and_or_search
    start = random_start()
    return and_or_search(start, goal=goal_param, max_depth=40, max_steps_log=max_steps, branch_limit=12)

# --- GUI phần còn lại giữ nguyên (giữ giao diện của bạn) ---
def Quan_Xe():
    global game

    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="MÔ TẢ AND–OR SEARCH", font=("Arial", 15, "bold"),
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
        for r in range(8):
            for c in range(8):
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
        all_logs, plan = run_and_or(goal_tuple)
        print("\n===== Conditional Plan (Cây điều kiện) =====")
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
    game.title("8 Quân Xe - AND–OR Search (Chuẩn)")

    draw_board(game)

    all_logs, plan = run_and_or(goal_tuple)
    print("\n===== Conditional Plan (Cây điều kiện) =====")
    print_plan(plan)

    global board_labels
    board_labels = [[None for _ in range(8)] for _ in range(8)]

    for r, c in enumerate(goal_cols):
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

# wrapper giữ interface
def run_and_or(goal_param):
    start = random_start()
    return and_or_search(start, goal=goal_param, max_depth=40, max_steps_log=800, branch_limit=12)

# ================== MAIN ==================
root = tk.Tk()
root.withdraw()
Quan_Xe()
root.mainloop()

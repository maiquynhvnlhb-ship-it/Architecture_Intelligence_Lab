import tkinter as tk

# ================== MỤC TIÊU ==================
goal_cols = [2, 1, 5, 3, 0, 4, 7, 6]
goal_tuple = tuple(goal_cols)

# ================== AND–OR SEARCH ==================
def goal_test(state, goal=goal_tuple):
    return state == tuple(goal)

def actions(state, row):
    N = len(state)
    used_cols = {c for c in state[:row] if c != -1}
    return [c for c in range(N) if c not in used_cols]

def result(state, row, col):
    new_state = list(state)
    new_state[row] = col
    return tuple(new_state)

def OR_Search(state, goal, path):
    if goal_test(state, goal):
        return []
    if state in path:
        return None
    if -1 not in state:
        return None

    row = state.index(-1)
    for a in actions(state, row):
        s = result(state, row, a)
        plan = AND_Search([s], goal, path + [state])
        if plan is not None:
            return [('move', (row, a), plan)]
    return None

def AND_Search(states, goal, path):
    all_plans = []
    for s in states:
        plan = OR_Search(s, goal, path)
        if plan is None:
            return None
        all_plans.append(plan)
    return all_plans

# ================== wrapper giữ interface cho GUI ==================
def and_or_search(initial_state, goal=goal_tuple):
    init_state = tuple(-1 for _ in range(8))
    plan = OR_Search(init_state, goal, [])

    # Tạo all_logs từ plan để GUI chạy animation
    all_logs = []
    xe = [-1] * 8

    def extract_steps(plan):
        steps = []
        if not plan:
            return []
        if isinstance(plan, list):
            for p in plan:
                steps.extend(extract_steps(p))
        elif isinstance(plan, tuple) and plan[0] == 'move':
            row, col = plan[1]
            xe[row] = col
            current_positions = [(r, c) for r, c in enumerate(xe) if c != -1]
            steps.append((current_positions, 0))
            steps.extend(extract_steps(plan[2]))
        return steps

    all_logs = extract_steps(plan)
    return all_logs, plan

def run_and_or(goal_param):
    start = tuple(-1 for _ in range(8))
    return and_or_search(start, goal=goal_param)

# ================== GUI ==================
def Quan_Xe():
    global game

    def draw_board(master, cell_size=(9, 4)):
        B = ["a","b","c","d","e","f","g","h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial",15,"bold"), fg="green").grid(row=0,column=11,columnspan=2)
        tk.Label(master, text="MÔ TẢ AND–OR SEARCH", font=("Arial",15,"bold"), fg="green").grid(row=0,column=1,columnspan=6)
        for i in range(8):
            tk.Label(master, text=f"     {8-i}", font=("Arial",12)).grid(row=i+1,column=0)
            tk.Label(master, text=f"     {8-i}", font=("Arial",12)).grid(row=i+1,column=10)
            tk.Label(master, text="   ").grid(row=i+1,column=9)
            tk.Label(master, text=B[i], font=("Arial",12)).grid(row=9,column=i+1)
            tk.Label(master, text=B[i], font=("Arial",12)).grid(row=9,column=i+11)
            for j in range(8):
                color = "#a7dcfa" if (i-j)%2==0 else "#416072"
                tk.Label(master,width=cell_size[0],height=cell_size[1],bg=color,relief="flat",bd=0).grid(row=i+1,column=j+1)
                tk.Label(master,width=cell_size[0],height=cell_size[1],bg=color,relief="flat",bd=0).grid(row=i+1,column=j+11)

    def replace(row,col,X):
        if board_labels[row][col] is not None:
            try:
                board_labels[row][col].destroy()
            except: pass
            board_labels[row][col]=None
        bg_color = "#a7dcfa" if (row-col)%2==0 else "#416072"
        lbl=tk.Label(game,text=X,font=("Arial",18,"bold"),fg="black",bg=bg_color,width=4,height=2,relief="ridge",bd=1)
        lbl.grid(row=row+1,column=col+1)
        board_labels[row][col]=lbl

    def move(step=None):
        nonlocal current_step, paused
        if not all_logs:
            return
        if step is not None:
            current_step=step
        if paused:
            return
        if current_step>=len(all_logs):
            return
        current,h_val=all_logs[current_step]
        for r in range(8):
            for c in range(8):
                if board_labels[r][c] is not None:
                    board_labels[r][c].destroy()
                    board_labels[r][c]=None
        for (r,c) in current:
            replace(r,c,"♜")
        current_step+=1
        game.after(300,move)

    def play():
        nonlocal paused
        paused=False
        move()
    def pause():
        nonlocal paused
        paused=True
    def restart():
        nonlocal current_step, paused, all_logs
        all_logs, _ = run_and_or(goal_tuple)
        current_step=0
        paused=False
        move(0)

    root.withdraw()
    try: game.destroy()
    except: pass
    game=tk.Toplevel()
    game.geometry(f"1300x700+{(root.winfo_screenwidth()-1300)//2}+{(root.winfo_screenheight()-700)//2}")
    game.title("8 Quân Xe - AND–OR Search (Chuẩn)")
    draw_board(game)

    all_logs, _ = run_and_or(goal_tuple)

    global board_labels
    board_labels=[[None for _ in range(8)] for _ in range(8)]

    # Vẽ mục tiêu bên phải
    for r,c in enumerate(goal_cols):
        bg_color = "#a7dcfa" if (r-c)%2==0 else "#416072"
        lbl=tk.Label(game,text="♜",font=("Arial",18,"bold"),fg="black",bg=bg_color,width=4,height=2,relief="ridge",bd=1)
        lbl.grid(row=r+1,column=c+1+10)

    btn_play=tk.Button(game,text="▶ Chạy",font=("Arial",12,"bold"),command=play,bg="#4CAF50",fg="white",width=11)
    btn_play.grid(row=11,column=1,padx=4,columnspan=2)
    btn_pause=tk.Button(game,text="⏸ Tạm dừng",font=("Arial",12,"bold"),command=pause,bg="#FF9800",fg="white",width=11)
    btn_pause.grid(row=11,column=3,padx=4,columnspan=2)
    btn_restart=tk.Button(game,text="🔄 Bắt đầu lại",font=("Arial",12,"bold"),command=restart,bg="#F44336",fg="white",width=11)
    btn_restart.grid(row=11,column=5,padx=4,columnspan=2)

    paused=False
    current_step=0
    move(0)

    def close():
        try: game.destroy()
        except: pass
        try: root.destroy()
        except: pass
    game.protocol("WM_DELETE_WINDOW",close)

# ================== MAIN ==================
root=tk.Tk()
root.withdraw()
Quan_Xe()
root.mainloop()

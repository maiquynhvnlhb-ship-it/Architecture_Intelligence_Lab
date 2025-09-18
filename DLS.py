import tkinter as tk

goal = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,6),(6,5),(7,7)]  # ví dụ
limit = len(goal)

def Quan_Xe():
    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="DLS VỚI CUT-OFF (8 QUÂN XE)",
                 font=("Arial", 15, "bold"), fg="green").grid(row=0, column=1, columnspan=8)

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

    # ---------------- DLS với cutoff ----------------
    def DLS_limit(vt, last_row, depth, limit):
        if len(vt) == limit:   # đủ 8 quân
            if vt == goal:
                steps.append((vt[:], "Goal"))
                return "success"
            else:
                steps.append((vt[:], "Cutoff"))
                return "cutoff"

        steps.append((vt[:], "Expand"))
        cutoff_occurred = False

        for r in range(last_row + 1, 8):
            for c in range(8):
                if all(c != cc for (_, cc) in vt):  # không trùng cột
                    result = DLS_limit(vt + [(r, c)], r, depth + 1, limit)
                    if result == "cutoff":
                        cutoff_occurred = True
                    elif result == "success":
                        return "success"
        return "cutoff" if cutoff_occurred else "failure"

    def DLS_steps(goal, limit):
        global steps
        steps = []
        DLS_limit([], -1, 0, limit)
        return steps

    def replace(row, col, X):
        if board_labels[row][col]:
            board_labels[row][col].destroy()
        bg_color = "#a7dcfa" if (row - col) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text=X, font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=row + 1, column=col + 1)
        board_labels[row][col] = lbl

    def show_step(step):
        current, status = all_steps[step]

        # clear bàn bên trái
        for r in range(8):
            for c in range(8):
                replace(r, c, "")

        # vẽ trạng thái hiện tại
        for (r, c) in current:
            replace(r, c, "♜")

        step_label.config(text=f"Bước: {step + 1}/{len(all_steps)} | Trạng thái: {status}")

    def play(step=0):
        # sử dụng biến global running, current_step
        global running, current_step
        if not running:
            return
        if step >= len(all_steps):
            running = False
            return
        current_step = step
        show_step(step)
        # tiếp tục gọi nếu vẫn đang chạy
        game.after(500, play, step + 1)

    def pause():
        global running
        running = False

    def restart():
        global running, current_step
        running = False
        current_step = 0
        show_step(0)

    # hàm khởi động (thay cho lambda + setattr)
    def start_play():
        global running
        running = True
        play(current_step)

    # GUI
    root.withdraw()
    global game
    try:
        game.destroy()
    except:
        pass

    game = tk.Toplevel()
    game.geometry(f"1250x750+{(root.winfo_screenwidth()-1250)//2}+{(root.winfo_screenheight()-750)//2}")
    game.title("8 Quân Xe (DLS với cutoff)")

    draw_board(game)

    global all_steps
    all_steps = DLS_steps(goal, limit)

    global board_labels
    board_labels = [[None for _ in range(8)] for _ in range(8)]

    # bàn phải (goal) — nếu bạn không muốn hiển thị goal, xóa khối này
    for (r, c) in goal:
        bg_color = "#a7dcfa" if (r - c) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text="♜", font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=r + 1, column=c + 1 + 10)

    global step_label
    step_label = tk.Label(game, text="Bước: 0", font=("Arial", 14), fg="red")
    step_label.grid(row=10, column=1, columnspan=8)

    # Nút điều khiển
    global running, current_step
    running = False
    current_step = 0

    btn_play = tk.Button(game, text="▶ Chạy", font=("Arial", 12, "bold"),
                         command=start_play,
                         bg="#4CAF50", fg="white", width=11)
    btn_play.grid(row=11, column=1, padx=4, columnspan=2)

    btn_pause = tk.Button(game, text="⏸ Tạm dừng", font=("Arial", 12, "bold"),
                          command=pause, bg="#FF9800", fg="white", width=11)
    btn_pause.grid(row=11, column=3, padx=4, columnspan=2)

    btn_restart = tk.Button(game, text="🔄 Bắt đầu lại", font=("Arial", 12, "bold"),
                            command=restart, bg="#F44336", fg="white", width=11)
    btn_restart.grid(row=11, column=5, padx=4, columnspan=2)

    show_step(0)  # hiển thị trạng thái ban đầu

    def close():
        game.destroy()
        root.destroy()
    game.protocol("WM_DELETE_WINDOW", close)


############ MAIN ############
root = tk.Tk()
root.withdraw()
Quan_Xe()
root.mainloop()

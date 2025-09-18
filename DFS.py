import tkinter as tk

# ================== GOAL ==================
goal = [0, 1, 2, 3, 5, 4, 7, 6]  # cột mục tiêu

# ================== DFS ==================
def DFS(goal):
    """Trả về tất cả các bước DFS (state)"""
    def check(vt, col):
        row = len(vt)
        for r, c in vt:
            if c == col:
                return False
        return True

    stack = [[]]  # stack cho DFS
    steps = []

    while stack:
        vt = stack.pop()  # lấy state cuối cùng
        if len(vt) > 0:
            steps.append(vt[:])
        # check goal
        if len(vt) == 8 and [c for r, c in vt] == goal:
            return steps
        row = len(vt)
        if row < 8:
            # push các nhánh mới vào stack **ngược thứ tự** để DFS đi từ c=0 lên c=7
            for c in reversed(range(8)):
                if check(vt, c):
                    stack.append(vt + [(row, c)])
    return steps

# ================== GIAO DIỆN ==================
def Quan_Xe():
    def draw_board(master, cell_size=(9, 4)):
        B = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tk.Label(master, text="MỤC TIÊU", font=("Arial", 15, "bold"),
                 fg="green").grid(row=0, column=11, columnspan=2)
        tk.Label(master, text="MÔ TẢ DFS TRONG BÀI TOÁN", font=("Arial", 15, "bold"),
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

        current = all_logs[current_step]

        # xóa quân cũ
        for r in range(8):
            for c in range(8):
                replace(r, c, "")

        # vẽ quân hiện tại
        for (r, c) in current:
            replace(r, c, "♜")

        lbl_step.config(text=f"Bước: {current_step + 1}/{len(all_logs)}")

        current_step += 1
        game.after(500, move)

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
    game.title("8 Quân Xe - DFS (tọa độ 2D)")

    draw_board(game)
    all_logs = DFS(goal)

    global board_labels
    board_labels = [[None for _ in range(8)] for _ in range(8)]

    # hiển thị goal bên phải
    for r, c in enumerate(goal):
        bg_color = "#a7dcfa" if (r - c) % 2 == 0 else "#416072"
        lbl = tk.Label(game, text="♜", font=("Arial", 18, "bold"),
                       fg="black", bg=bg_color, width=4, height=2,
                       relief="ridge", bd=1)
        lbl.grid(row=r + 1, column=c + 1 + 10)

    lbl_step = tk.Label(game, text="Bước: 0", font=("Arial", 14, "bold"), fg="red")
    lbl_step.grid(row=10, column=1, columnspan=6)

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

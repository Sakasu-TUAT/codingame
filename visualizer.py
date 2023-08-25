import customtkinter as ctk
import tkinter as tk
from othello_py import *
import subprocess
import sys
import time

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# オセロ盤面のサイズ
BOARD_SIZE = 8
NUM_SQUARE = 8
# プレイヤーを示す値
YOU = 1
COM = 2

dy = [0, 1, 0, -1, 1, 1, -1, -1]
dx = [1, 0, -1, 0, 1, -1, 1, -1]

# 色の設定
BOARD_COLOR_LIGHT = 'green' # 盤面の背景色
BOARD_COLOR_DARK = "dark green"
YOUR_COLOR = 'black' # あなたの石の色
COM_COLOR = 'white' # 相手の石の色
PLACABLE_COLOR = 'yellow' # 次に石を置ける場所を示す色


class OthelloBoard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 盤面の状態 0: 黒 1: 白 2: 合法手 3: 非合法手
        self.grid = [[vacant for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.grid[3][3] = "white"
        self.grid[3][4] = "black"
        self.grid[4][3] = "black"
        self.grid[4][4] = "white"
        self.YOUR_SCORE = 2
        self.COM_SCORE = 2

        self.YOUR_SCORE_var = tk.StringVar()
        self.YOUR_SCORE_var.set(f"白: {self.YOUR_SCORE}")
        
        self.COM_SCORE_var = tk.StringVar()
        self.COM_SCORE_var.set(f"黒: {self.COM_SCORE}")

        self.createWidgets()
        self.color = { # 石の色を保持する辞書
            YOU : YOUR_COLOR,
            COM : COM_COLOR
        }

        self.player = YOU # 次に置く石の色
        self.cell_size = 0
        self.total_cell_num = 4
        self.x_offset = 0
        self.y_offset = 0

        self.draw_board()
        self.draw_pieces()
        self.setEvents()

        self.playGame()


    def playGame(self) : 
        cpp_output = subprocess.check_output(["./a.out"])
        output_values = cpp_output.decode("utf-8").strip().split()
        x = int(output_values[0])
        y = int(output_values[1])

        self.showPlacable(self.getPlacable())

        print("Received values from C++:", y, x)
        self.after(1000, self.playPiece, y, x)

    def createWidgets(self):
        self.title("Othello")
        self.geometry("1100x800")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=3)

        self.boardFrame = ctk.CTkFrame(master=self, corner_radius=0, fg_color="#0e0b16")
        self.boardFrame.grid(row=0, column=0, rowspan = 1, sticky="nsew")
        self.boardFrame.rowconfigure(1, weight=1) # boardFrameのrow1にweightオプションを1に指定
        self.boardFrame.columnconfigure(0, weight=1) # boardFrameのcolumn0にweightオプションを1に指      
        
        self.canvas = ctk.CTkCanvas(master=self.boardFrame, bg="#0e0b16", highlightthickness=0)
        self.canvas.grid(row=1, column=0, rowspan=1, sticky="nsew")  

        title = ctk.CTkLabel(self.boardFrame, text="Othello", font=("Helvetica", 80))
        title.grid(row=0, column=0)
        self.sidebar_frame = ctk.CTkFrame(master=self,corner_radius=0, fg_color="#5f0f4e")
        self.sidebar_frame.grid(row=0, column=1,sticky="nsew")

        # self.scoreBoard = ctk.CTkLabel(self.sidebar_frame, text="Score", font=("Helvetica", 30)).grid(row=1, column=1, sticky="nsew")
        # 黒の石の数を表示するラベル
        self.your_score_label = ctk.CTkLabel(self.sidebar_frame, textvariable=self.YOUR_SCORE_var,  font=("Arial", 30), width=200, height=50)
        self.your_score_label.grid(row=5, column=2, padx=10, pady=10, rowspan = 1, columnspan=1)

        # 白の石の数を表示するラベル
        self.cpu_score_label = ctk.CTkLabel(self.sidebar_frame, textvariable=self.COM_SCORE_var, font=("Arial", 30), width=200, height=50)
        self.cpu_score_label.grid(row=8, column=2, padx=10, pady=10, rowspan = 1, columnspan=1)

    def setEvents(self):
        '''キャンバス上のマウスクリックを受け付ける'''
        self.canvas.bind('<ButtonPress>', self.click)

    def playPiece(self, y, x):
        '''石を置く'''
        if self.checkPlacable(y, x, self.color[self.player]):
            # 次に石を置けるマスであれば石を置く
            self.total_cell_num  += 1
            self.reverse(y, x, self.color[self.player])    
            self.draw_pieces()
            if self.player == YOU:
                self.player = COM
            else:
                self.player = YOU
            self.showPlacable(self.getPlacable())

        else:
            print("そこは置けません")

    def draw_board(self):
        self.canvas.update()
        canvas_width = self.canvas.winfo_width ()
        canvas_height = self.canvas.winfo_height ()
        print(canvas_width, canvas_height)
        self.cell_size = (min(canvas_width, canvas_height) - 100) / BOARD_SIZE
        print(self.cell_size)
        board_width = BOARD_SIZE * self.cell_size
        board_height = BOARD_SIZE * self.cell_size
        self.x_offset = (canvas_width - board_width) / 2
        self.y_offset = (canvas_height - board_height) / 2

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * self.cell_size + self.x_offset 
                y1 = row * self.cell_size + self.y_offset
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = BOARD_COLOR_LIGHT if (row + col) % 2 == 0 else BOARD_COLOR_DARK
                # print("Board: ", x1 // self.cell_size, y1 // self.cell_size, x2 // self.cell_size, y2 // self.cell_size)
                tag_name = 'square_' + str(y1 // self.cell_size) + '_' + str(x1 // self.cell_size)
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="white",
                    tags=tag_name
                )
    
    def draw_pieces(self):
        self.canvas.update()
        canvas_width = self.canvas.winfo_width ()
        canvas_height = self.canvas.winfo_height ()
        print(canvas_width, canvas_height)
        self.cell_size = (min(canvas_width, canvas_height) - 100) / BOARD_SIZE
        board_width = BOARD_SIZE * self.cell_size
        board_height = BOARD_SIZE * self.cell_size
        x_offset = (canvas_width - board_width) / 2
        y_offset = (canvas_height - board_height) / 2

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] != vacant:
                    x1 = x_offset + col * self.cell_size
                    y1 = y_offset + row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    color = "green" if (row + col) % 2 == 0 else "dark green"
                    # self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
                    self.canvas.create_oval(
                        x1 + self.cell_size * 0.2, y1 + self.cell_size * 0.2,
                        x2 - self.cell_size * 0.2, y2 - self.cell_size * 0.2,
                        fill=self.grid[row][col]
                    )

    o = othello()

    def click(self, event):
        '''盤面がクリックされた時の処理'''
        # if self.player != YOU:
        #     # COMが石を置くターンの時は何もしない
        #     return

        # クリックされたｘ位置がどのマスであるかを計算
        y = event.y // self.cell_size - 1 
        x = event.x // self.cell_size - 1
        self.playPiece(y, x)

    def showPlacable(self, placable):
        '''placableに格納された次に石が置けるマスの色を変更する'''
        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                x1 = self.x_offset + x * self.cell_size
                y1 = self.y_offset + y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                tag_name = 'square_' + str(y1 // self.cell_size) + '_' + str(x1 // self.cell_size)
                if (y, x) in placable:
                    self.canvas.itemconfig(tag_name, fill="dark blue")
                    print(y, x, "can place: blue")
                else: 
                    color = BOARD_COLOR_LIGHT if (y + x) % 2 == 0 else BOARD_COLOR_DARK
                    self.canvas.itemconfig(tag_name, fill=color)

    def getPlacable(self):
        '''次に置くことができる石の位置を取得'''
        placable = []
        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                if self.checkPlacable(y, x, color=self.color[self.player]):
                    placable.append((y, x))
        return placable


    def checkPlacable(self, y, x, color):
        y = int(y)
        x = int(x)

        if not self.is_inside_of_board(y, x):
            print('盤面外です')
            return False
        if  self.grid[y][x] == "black" or self.grid[y][x] == "white":
            print("すでに石が置かれています")
            return False
        
        for direction in range(8):
            ny = y
            nx = x
            cnt = 0
            for d in range (BOARD_SIZE - 1):
                ny += dy[direction]
                nx += dx[direction]
                if not self.is_inside_of_board(ny, nx):
                    break
                if self.grid[ny][nx] == vacant:
                    break
                #同じ色のマスが隣接している場合
                if self.grid[ny][nx] == color and cnt == 0: 
                    break
                if self.grid[ny][nx] == color:
                    print("ok: ", ny, nx, color)
                    return True
                cnt+=1
            
        return False


    def reverse(self, y, x, color):
        y = int(y)
        x = int(x)

        if not self.is_inside_of_board(y, x):
            print('盤面外です')
            return False
        if  self.grid[y][x] != vacant:
            print("すでに石が置かれています")
            return False
        
        for direction in range(8):
            ny = y
            nx = x
            canFlip = False
            cnt = 0
            for d in range (BOARD_SIZE - 1):
                ny += dy[direction]
                nx += dx[direction]
                if not self.is_inside_of_board(ny, nx):
                    break
                if self.grid[ny][nx] == vacant:
                    break
                #同じ色のマスが隣接している場合
                if self.grid[ny][nx] == color and cnt == 0: 
                    break
                if self.grid[ny][nx] == color:
                    canFlip = True
                    break
                cnt+=1
            
            if canFlip:
                print(ny, nx , "can flip")
                flipNum = 0
                while nx != x or ny != y:
                    flipNum += 1
                    self.grid[ny][nx] = color
                    ny-=dy[direction]
                    nx-=dx[direction]
                    self.grid[y][x] = color
                
                flipNum -=1 
                if color == self.color[YOU]:
                    self.YOUR_SCORE += flipNum
                    self.COM_SCORE -= flipNum
                elif color == self.color[COM]:
                    self.COM_SCORE += flipNum
                    self.YOUR_SCORE -= flipNum
   
            else:
                pass
                # print(ny, nx , "can't flip")

            # self.COM_SCORE = self.total_cell_num - self.YOUR_SCORE
        self.COM_SCORE+=(color == self.color[COM])
        self.YOUR_SCORE+=(color == self.color[YOU])
        print("black: ", self.YOUR_SCORE, "white: ", self.COM_SCORE)
        self.YOUR_SCORE_var.set(f"YOU: {self.YOUR_SCORE}")
        self.COM_SCORE_var.set(f"CPU: {self.COM_SCORE}")


    def is_inside_of_board(self, y, x):
        return 0 <= y < BOARD_SIZE and 0 <= x < BOARD_SIZE


if __name__ == "__main__":
    app = OthelloBoard()
    app.mainloop()
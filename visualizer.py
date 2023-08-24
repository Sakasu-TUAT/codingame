import customtkinter as ctk
from othello_py import *

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# オセロ盤面のサイズ
BOARD_SIZE = 8

class OthelloBoard(ctk.CTk):
    def __init__(self):
        super().__init__()

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
        
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        self.canvas.update()
        canvas_width = self.canvas.winfo_width ()
        canvas_height = self.canvas.winfo_height ()
        print(canvas_width, canvas_height)
        cell_size = (min(canvas_width, canvas_height) - 100) / BOARD_SIZE
        board_width = BOARD_SIZE * cell_size
        board_height = BOARD_SIZE * cell_size
        x_offset = (canvas_width - board_width) / 2
        y_offset = (canvas_height - board_height) / 2
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * cell_size + x_offset 
                y1 = row * cell_size + y_offset
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "green" if (row + col) % 2 == 0 else "dark green"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
    
    def draw_pieces(self):
        self.canvas.update()
        canvas_width = self.canvas.winfo_width ()
        canvas_height = self.canvas.winfo_height ()
        print(canvas_width, canvas_height)
        cell_size = (min(canvas_width, canvas_height) - 100) / BOARD_SIZE
        board_width = BOARD_SIZE * cell_size
        board_height = BOARD_SIZE * cell_size
        x_offset = (canvas_width - board_width) / 2
        y_offset = (canvas_height - board_height) / 2

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = x_offset + col * cell_size
                y1 = y_offset + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "green" if (row + col) % 2 == 0 else "dark green"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
                if (row + col) % 2 == 0:  # 黒い石を配置
                    self.canvas.create_oval(
                        x1 + cell_size * 0.2, y1 + cell_size * 0.2,
                        x2 - cell_size * 0.2, y2 - cell_size * 0.2,
                        fill="black"
                    )
                else:  # 白い石を配置
                    self.canvas.create_oval(
                        x1 + cell_size * 0.2, y1 + cell_size * 0.2,
                        x2 - cell_size * 0.2, y2 - cell_size * 0.2,
                        fill="white"
                    )

    o = othello()

    # def show_board(self):
        # global clicked, legal_buttons
        # for button in legal_buttons:
        #     button.place_forget()
        # legal_buttons = []
        # for y in range(hw):
        #     for x in range(hw):
        #         try:
        #             self.canvas.delete(str(y) + '_' + str(x))
        #         except:
        #             pass
        #         if self.o.grid[]


if __name__ == "__main__":
    app = OthelloBoard()
    app.mainloop()
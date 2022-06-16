import tkinter as tk
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
from second_page import *

class Start_Page():
    def __init__(self, win):
        # setup the window
        self.win = win
        self.frame = tk.Frame(self.win)
        self.frame.grid()
        
        # create a background picture in the window
        img_bak = Image.open('image/background_3.png').resize((800, 500))
        photo_bak = ImageTk.PhotoImage(img_bak)
        self.bak = tk.Canvas(self.frame, width = 800, height = 500)
        self.bak.grid()
        self.bak.create_image(0, 0, anchor=tk.NW, image = photo_bak)

        # create a button to go to next page
        self.button = tk.Button(self.frame, width = 8, height = 1, text = 'START', \
                                      font = ('Arial', 18, 'bold'), border=0, command = self.next_page)
        self.bak.create_window(610, 400, anchor=tk.NW, window=self.button)


        self.frame.mainloop()
        pass

    def next_page(self):
        self.frame.destroy()
        Second_Page(self.win)
        self.frame.quit()
        self.__init__(self.win)
        return

if __name__ == '__main__':
    win = tk.Tk()
    win.title('Exercise & Life')
    win.geometry('800x500')
    m = Start_Page(win)



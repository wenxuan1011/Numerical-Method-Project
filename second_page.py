import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import ImageTk, Image
from result_page import *
import re

class Second_Page():
    def __init__(self, win):
        # set parameters to check all inputs are entered or not 
        self.weight_check = False
        self.duration_check = False
        self.calories_check = False

        # set parameters to save the values of all inputs
        self.weight_value = 0
        self.intensity_value = None
        self.duration_value = 0
        self.calories_value = 0

        # setup the window
        self.win = win
        self.win.title('Exercise & Life')
        self.win.geometry('800x500')
        self.frame = tk.Frame(self.win)
        self.frame.grid()

        # create a background picture in the window
        img_bak = Image.open('image/background_4.png').resize((800, 500))
        photo_bak = ImageTk.PhotoImage(img_bak)
        self.bak = tk.Canvas(self.frame, width = 800, height = 500)
        self.bak.grid()
        self.bak.create_image(0, 0, anchor=tk.NW, image = photo_bak)

        # create a weight input
        self.weight_label = tk.Label(self.frame, text = 'weight :', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(470, 100, anchor=tk.NW, window = self.weight_label)
        self.weight_input = tk.Text(self.frame, width = 12, height = 1, font = ('Candara', 14), border = 2)
        self.bak.create_window(580, 100, anchor=tk.NW, window = self.weight_input)
        self.kg_label = tk.Label(self.frame, text = 'kg', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(710, 100, anchor=tk.NW, window = self.kg_label)

        # create a exercise intensity input
        self.intensity_label = tk.Label(self.frame, text = 'exercise intensity :', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(470, 160, anchor=tk.NW, window = self.intensity_label)
        self.intensity_combobox = ttk.Combobox(self.frame, width = 30, \
                values = ['Moderate intensity (from 3.1-6.0 METs)', 'Vigorous intensity (upper 6.0 METs)',\
                    'Moderate or Vigorous intensity'], font=('Candara', 12))
        self.intensity_combobox.current(0)
        self.bak.create_window(470, 200, anchor=tk.NW, window = self.intensity_combobox)

        # create a duration input
        self.duration_label = tk.Label(self.frame, text = 'duration :', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(470, 260, anchor=tk.NW, window = self.duration_label)
        self.duration_input = tk.Text(self.frame, width = 12, height = 1, font = ('Candara', 14), border = 2)
        self.bak.create_window(580, 260, anchor=tk.NW, window = self.duration_input)
        self.hr_label = tk.Label(self.frame, text = 'hours', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(710, 260, anchor=tk.NW, window = self.hr_label)

        # create a calories input
        self.calories_label = tk.Label(self.frame, text = 'calories : ', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(470, 320, anchor=tk.NW, window = self.calories_label)
        self.calories_input = tk.Text(self.frame, width = 12, height = 1, font = ('Candara', 14), border = 2)
        self.bak.create_window(580, 320, anchor=tk.NW, window = self.calories_input)
        self.cal_label = tk.Label(self.frame, text = 'Kcal', font = ('Candara', 14), bg = 'white')
        self.bak.create_window(710, 320, anchor=tk.NW, window = self.cal_label)

        ## create a button to go to next page
        self.button = tk.Button(self.frame, width = 8, height = 1, text = 'NEXT', \
                                      font = ('Arial', 18, 'bold'), border=0, command = self.next_page)
        self.bak.create_window(610, 400, anchor=tk.NW, window=self.button)

        self.frame.mainloop()
        pass

    def check_enter_or_not(self):
        self.weight_value = re.sub("\s", "", self.weight_input.get("1.0",'end-1c'))
        self.intensity_value = self.intensity_combobox.get()
        self.duration_value = re.sub("\s", "", self.duration_input.get("1.0",'end-1c'))
        self.calories_value = re.sub("\s", "", self.calories_input.get("1.0",'end-1c'))
        if(self.weight_value != ''):
            self.weight_check = True
        if(self.duration_value != ''):
            self.duration_check = True
        if(self.calories_value != ''):
            self.calories_check = True
        return

    def next_page(self):
        self.check_enter_or_not()
        if(self.weight_check == True and self.duration_check == True and self.calories_check == True):
            self.frame.destroy()
            print(self.duration_value)
            print(type(self.duration_value))
            Result_Page(self.win, self.weight_value, self.intensity_value, self.duration_value, self.calories_value)
            self.frame.quit()
        else:
            win = tk.Tk()
            win.title('Error')
            win.geometry('200x200')
            label = tk.Label(win, text = '尚有輸入未填寫', font = ('Arial', 14))
            label.place(x=50, y=50)
            win.mainloop()
        return

if __name__ == '__main__':
    win = tk.Tk()
    m = Second_Page(win)
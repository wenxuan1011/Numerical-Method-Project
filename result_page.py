import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import ImageTk, Image
import pandas as pd 
from GA import *

class Result_Page():
    def __init__(self, win, weight, intensity, duration, calories):
        # get the value from last page
        self.weight = weight
        self.intensity = intensity
        self.duration = duration
        self.calories = calories
        self.number_list, self.fitness = self.get_the_reuslt()
        self.data = pd.read_csv('exercises_METs.csv')

        # setup the window
        self.win = win
        self.win.title('Exercise & Life')
        self.win.geometry('800x500')
        self.frame = tk.Frame(self.win)
        self.frame.grid()

        # create a background picture in the window
        img_bak = Image.open('image/background_5.png').resize((800, 500))
        photo_bak = ImageTk.PhotoImage(img_bak)
        self.bak = tk.Canvas(self.frame, width = 800, height = 500)
        self.bak.grid()
        self.bak.create_image(0, 0, anchor=tk.NW, image = photo_bak)

        # create output labels
        if(self.number_list[0] != self.number_list[1]):
            self.output1_label = tk.Label(self.frame, text = self.data.iat[self.number_list[0], 0],\
                font = ('Candara', 14, 'bold'), bg = 'white')
            self.bak.create_window(190, 220, anchor=tk.NW, window = self.output1_label)
            self.output2_label = tk.Label(self.frame, text = self.data.iat[self.number_list[1], 0],\
                font = ('Candara', 14, 'bold'), bg = 'white')
            self.bak.create_window(190, 265, anchor=tk.NW, window = self.output2_label)

            # create output pictures in the window
            img_output2 = Image.open('image/'+str(self.data.iat[self.number_list[1], 2])+'.png').resize((210, 210))
            photo_output2 = ImageTk.PhotoImage(img_output2)
            self.bak.create_image(525, 220, anchor=tk.NW, image = photo_output2)
            img_output1 = Image.open('image/'+str(self.data.iat[self.number_list[0], 2])+'.png').resize((210, 210))
            photo_output1 = ImageTk.PhotoImage(img_output1)
            self.bak.create_image(430, 60, anchor=tk.NW, image = photo_output1)
        
        else:
            self.output_label = tk.Label(self.frame, text = self.data.iat[self.number_list[0], 0],\
                font = ('Candara', 14, 'bold'), bg = 'white')
            self.bak.create_window(190, 240, anchor=tk.NW, window = self.output_label)

            # create output pictures in the window
            img_output = Image.open('image/'+str(self.data.iat[self.number_list[0], 2])+'.png').resize((250, 250))
            photo_output = ImageTk.PhotoImage(img_output)
            self.bak.create_image(470, 120, anchor=tk.NW, image = photo_output)
        
        percent = round((float(self.fitness)/float(self.calories))*100, 2)
        self.fitness_label = tk.Label(self.frame, text = 'Error:   '+str(round(self.fitness, 2))+'   Kcal   ('+str(percent)+')%',\
            font = ('Candara', 14, 'bold'), bg = 'white')
        self.bak.create_window(190, 330, anchor=tk.NW, window = self.fitness_label)

        if(round(float(self.fitness)/float(self.calories), 2) > 0.1):
            self.suggest_label = tk.Label(self.frame, text = '( Please adjust your intensity, duration, or calories to fit your goal. )',\
                font = ('Candara', 11, 'bold'), bg = 'white')
            self.bak.create_window(155, 420, anchor=tk.NW, window = self.suggest_label)


        self.win.mainloop()
        pass

    def get_the_reuslt(self):
        number_list = []
        fitness, number_list = run_main(float(self.weight), self.intensity, float(self.duration), float(self.calories))
        return number_list, fitness

if __name__ == '__main__':
    win = tk.Tk()
    m = Result_Page(win)
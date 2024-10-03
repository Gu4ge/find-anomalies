import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys
import os


sys.path.insert(1, os.path.join(sys.path[0], '../Library'))
from save_data import save_data
from logic import *
from print import *
from windows import *

class StockMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("мониторинг")
        self.root.geometry("1000x1000")
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        label = ttk.Label(frame, text="Тикер:")
        label.pack(side=tk.LEFT, padx=5)

        self.entry = ttk.Entry(frame)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        label = ttk.Label(frame, text="Период:")
        label.pack(side=tk.LEFT, padx=5)
        
        list_period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        self.combobox_period = ttk.Combobox(frame, values=list_period, state='readonly')
        self.combobox_period.pack(side=tk.LEFT, padx=5)
        
        label = ttk.Label(frame, text="Интервал:")
        label.pack(side=tk.LEFT, padx=5)
        
        list_interval = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1w', '1mo', '3mo']
        self.combobox_interval = ttk.Combobox(frame, values=list_interval, state='readonly')
        self.combobox_interval.pack(side=tk.LEFT, padx=5)

        self.btn_update = ttk.Button(frame, text="Обновить", command=self.update_graph)
        self.btn_update.pack(side=tk.LEFT, padx=5)
        
        self.btn_instuction = ttk.Button(frame, text="Инструкция", command=instr_win)
        self.btn_instuction.pack(side=tk.LEFT, padx=5)
        
        # создание графика
        self.fig = Figure(figsize=(10, 5))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.fig_boxplots = None
        self.canvas_boxplots = None
        
    
    def update_graph(self):
        
        self.df_ticker = get_ticker(self.entry.get().upper(), self.combobox_period.get(), self.combobox_interval.get())
        
        # если недостаточно данных или акция не имеет определенный интервал или период
        if len(self.df_ticker) < 2:
            not_enough_data(self.ax, self.canvas, self.fig_boxplots, self.entry.get().upper())
        
        # Очистка графика
        self.ax.clear()
        
        print_graph(self.ax, self.df_ticker)
        

        # Вычисление границ
        bound = calculates_outliners(self.df_ticker['changes'])
        
        self.is_outliner = (self.df_ticker['changes'] < bound[0]) | (self.df_ticker['changes'] > bound[1])
        
        # создание датафрейма аномальных значений
        self.anomalies = pd.DataFrame
        
        # Отметка аномальных скачков
        if self.is_outliner.any():
            
            # занесение аномальных значений
            self.anomalies = self.df_ticker[self.is_outliner]
            
            # пометка аномальных значений на графике цены 
            self.ax.scatter(self.anomalies.index, self.anomalies['Close'], color='red', label='Аномалия')
            
            self.df_clean = self.df_ticker.copy()
            
            # замена аномальных значений на вычесленные отрезки
            self.df_clean.loc[self.is_outliner, 'changes'] = swap_anomaly(self.df_clean, self.is_outliner, 'changes', bound)

            # Создание боксплотов для сравнения с - без аномалий 
            self.fig_boxplots, self.canvas_boxplots = get_boxplots(self.fig_boxplots, self.df_clean, self.df_ticker, self.root, self.canvas_boxplots)
        else:  
            self.canvas_boxplots.get_tk_widget().destroy()
            
        self.ax.set_title(f"График продаж {self.entry.get().upper()}")
        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Цена $")
        self.ax.legend()

        self.canvas.draw()
        
        save_data(self.df_ticker, self.entry.get().upper(), self.combobox_period.get(), self.combobox_interval.get(), self.anomalies,)
        
        if self.is_outliner.any():
            # создание окна с аномалиями
            anomaly_win(self.anomalies, self.df_ticker, self.is_outliner)

if __name__ == '__main__':
    root = tk.Tk()
    app = StockMonitorApp(root)
    root.mainloop()

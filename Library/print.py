from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def not_enough_data(ax, canvas, fig_boxplots, name):
    ax.clear()
    ax.set_title(f"Недостаточно данных по тикеру {name}")
    canvas.draw()
    if fig_boxplots:
        fig_boxplots.clear()
        return
        
def print_graph(ax, df):

    # Построение графика цены
    ax.plot(df['Close'], label='Цена закрытия')
        
    # метка текущей цены закрытия акции
    ax.scatter(df.index[-1], df['Close'][-1], color='green', label=f"тек. цена {round(df['Close'][-1], 2)}")

# Создание боксплотов для сравнения с - без аномалий    
def get_boxplots(fig_boxplots, df_clean, df_ticker, root, canvas_boxplots):
    # Очистка бокслплотов аномалий
    if fig_boxplots:  
        canvas_boxplots.get_tk_widget().destroy()
    
    
    fig_boxplots, (ax1, ax2) = plt.subplots(sharey=True, nrows=1, ncols=2, figsize=(10, 5))
            
    ax1.boxplot(df_clean['changes'])
    ax1.set_title("Без аномалий")
    ax1.set_ylabel("Отклонение изменения цены %")

    ax2.boxplot(df_ticker['changes'])
    ax2.set_title("С аномалиями")

    fig_boxplots.suptitle("Сравнение изменений цены в процентах")
    
    canvas_boxplots = FigureCanvasTkAgg(fig_boxplots, master=root)
    canvas_boxplots.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return fig_boxplots, canvas_boxplots


    
    
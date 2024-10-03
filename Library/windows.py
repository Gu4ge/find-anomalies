import tkinter as tk
from tkinter import ttk

def instr_win():
    root = tk.Tk()
    root.title("Инструкция")
    
    instruction_text = (
        "1) В окне 'тикер' вводятся все возможные тикеры, которые можно найти на сайте Yahoo Finance "
        "(акции, криптовалюты и т.д.).\n"
        "2) В окне 'период' вводится необходимый период из предложенного списка.\n"
        "3) В окне 'интервал' вводится необходимый интервал из предложенного списка.\n"
        "4) Для появления или обновления графика нажать на кнопку 'Обновить'.\n"
        "Примечание: некоторые тикеры не поддерживают определенные периоды или интервалы. Все возможные комбинации смотрите на Yahoo Finance."
    )
    
    label = tk.Label(root, text=instruction_text, justify=tk.LEFT, wraplength=400)
    label.pack(padx=10, pady=10)
    
    root.mainloop()

def anomaly_win(df_anomalies, df, is_outliner):
    root = tk.Tk()
    root.title("Результаты Аномалий")
    
    # описание для аномалий
    text_widget = tk.Text(root, wrap='word', height=5, width=80)
    text_widget.pack(padx=10, pady=10)
    text_widget.insert(tk.END, f'Найдено {is_outliner.sum()} аномалий\n')
    text_widget.insert(tk.END, f'Вклад аномалий в процентном соотношении: {is_outliner.sum() / len(df):.2f}%\n')
    text_widget.insert(tk.END, f'самое большое верхнее отклонение: {df_anomalies.changes.max():.2f}%\n')
    text_widget.insert(tk.END, f'самое большое нижнее отклонение: {df_anomalies.changes.min():.2f}%')
    text_widget.config(state=tk.DISABLED)
    
    # таблица аномальных значений
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame)
    tree.pack(side='left', fill=tk.BOTH, expand=True)
    
    df_anomalies.reset_index(inplace=True)
    
    
    columns = list(df_anomalies.columns)
    tree['columns'] = columns
    tree.heading("#0", text="", anchor=tk.W)
    tree.column("#0", width=0, stretch=tk.NO)

    
    for col in columns:
        tree.heading(col, text=col, anchor=tk.W)
        tree.column(col, anchor=tk.W, width=100)

    
    for index, row in df_anomalies.iterrows():
        tree.insert("", tk.END, text=index, values=list(row))

    # прокрутка таблицы
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    root.mainloop()
    
    return
import tkinter as tk
from tkinter import messagebox, ttk

HISTORY_FILE = "calc_history.txt"

def add_digit(digit):
    if entry_display.get() == "0":
        entry_display.delete(0, tk.END)
    entry_display.insert(tk.END, digit)

def add_operation(op):
    current = entry_display.get()
    if current and not current[-1] in "+-*/%^&|":
        entry_display.insert(tk.END, op)

def calculate(event=None):
    try:
        expression = entry_display.get()
        result = eval(expression)
        save_history(expression, result)
        entry_display.delete(0, tk.END)
        entry_display.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Ошибка", "Неверное выражение!")
        
def clear():
    entry_display.delete(0, tk.END)
    entry_display.insert(0, "0")

def save_history(expression, result):
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"{expression} = {result}\n")

def show_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = file.readlines()
        history_text = "".join(history[-10:])
        messagebox.showinfo("История вычислений", history_text if history_text else "История пуста.")
    except FileNotFoundError:
        messagebox.showinfo("История вычислений", "История пуста.")

def clear_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        file.write("")
    messagebox.showinfo("История очищена", "Файл с историей успешно очищен.")

# Главное окно
root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x400")
root.resizable(False, False)

# Настройка стилей
style = ttk.Style()
style.configure("Calc.TButton", font=("Arial", 14))

# Дисплей калькулятора
entry_display = tk.Entry(root, font=("Arial", 24), justify="right")
entry_display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
entry_display.insert(0, "0")

# Создание кнопок
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+',
]

# Функции для кнопок
btn_params = {
    'padx': 5,
    'pady': 5,
    'sticky': "nsew"
}

# Создание основных кнопок
row = 1
col = 0
for button in buttons:
    cmd = lambda x=button: add_digit(x) if x.isdigit() or x == '.' else \
          calculate() if x == '=' else \
          add_operation(x)
    btn = tk.Button(root, text=button, command=cmd, font=("Arial", 14))
    btn.grid(row=row, column=col, **btn_params)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Дополнительные операции
extra_ops = ['C', '&', '|', '^', '**', '%']
for i, op in enumerate(extra_ops):
    cmd = lambda x=op: clear() if x == 'C' else add_operation(x)
    btn = tk.Button(root, text=op, command=cmd, font=("Arial", 14))
    btn.grid(row=row+1, column=i % 4, **btn_params)
    if i == 3:  # Переход на следующую строку после 4 кнопок
        row += 1

# История
history_frame = tk.Frame(root)
history_frame.grid(row=row+2, column=0, columnspan=4, pady=5)

history_btn = tk.Button(history_frame, text="История", command=show_history, 
                       font=("Arial", 12))
history_btn.grid(row=0, column=0, padx=5)

clear_history_btn = tk.Button(history_frame, text="Очистить историю", 
                            command=clear_history, font=("Arial", 12))
clear_history_btn.grid(row=0, column=1, padx=5)

# Настройка grid
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(7):
    root.grid_rowconfigure(i, weight=1)

# Привязка клавиши Enter к вычислению
root.bind("<Return>", calculate)

# Привязка цифровых клавиш
def key_press(event):
    if event.char.isdigit() or event.char in "+-*/.":
        if event.char.isdigit() or event.char == '.':
            add_digit(event.char)
        else:
            add_operation(event.char)
    elif event.char == '\r':  # Enter
        calculate()

root.bind("<Key>", key_press)

root.mainloop()

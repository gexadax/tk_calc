import tkinter as tk
from tkinter import messagebox, ttk

HISTORY_FILE = "calc_history.txt"

def calculate(event=None):
    try:
        a = int(entry1.get())
        b = int(entry2.get())
        op = operation_var.get()

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = "Ошибка: деление на ноль!" if b == 0 else a / b
        elif op == "&":
            result = a & b
        elif op == "|":
            result = a | b
        elif op == "^":
            result = a ^ b
        elif op == "**":
            result = a ** b
        elif op == "%":
            result = "Ошибка: деление на ноль!" if b == 0 else a % b
        else:
            result = "Неизвестная операция!"

        result_label.config(text=f"Результат: {result}")
        save_history(a, b, op, result)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные целые числа!")

def save_history(a, b, op, result):
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"{a} {op} {b} = {result}\n")

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

def clear_fields():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result_label.config(text="Результат:")

# Главное окно
root = tk.Tk()
root.title("Калькулятор")
root.geometry("320x260")
root.resizable(False, False)

# Ввод чисел
tk.Label(root, text="Число 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=5, pady=5)
entry1.focus()

tk.Label(root, text="Число 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=5, pady=5)

# Выбор операции
tk.Label(root, text="Операция:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
operation_var = tk.StringVar(value="+")
operation_menu = ttk.Combobox(root, textvariable=operation_var, values=["+", "-", "*", "/", "&", "|", "^", "**", "%"], state="readonly", width=5)
operation_menu.grid(row=2, column=1, padx=5, pady=5)

# Кнопки
btn_frame = tk.Frame(root)
btn_frame.grid(row=3, column=0, columnspan=2, pady=5)

btn_width = 14  # Фиксированная ширина кнопок

tk.Button(btn_frame, text="Вычислить", command=calculate, width=btn_width).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Очистить", command=clear_fields, width=btn_width).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="История", command=show_history, width=btn_width).grid(row=1, column=0, pady=5)
tk.Button(btn_frame, text="Удалить историю", command=clear_history, width=btn_width).grid(row=1, column=1, pady=5)

# Результат
result_label = tk.Label(root, text="Результат:", font=("Arial", 12, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Привязка Enter к вычислению
root.bind("<Return>", calculate)

root.mainloop()

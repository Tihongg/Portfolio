import tkinter as tk
from tkinter import messagebox
from main import model

def predict():
    year = entry.get()
    try:
        year = int(entry.get())
        predict = model.predict(year)
        formatted_predict = "{:,}".format(predict).replace(",", " ")
        entry_label = tk.Label(window, text=predict)
        prediction_label.config(text=f"Предсказание для {year}г.: {formatted_predict} чел.")
    except ValueError:
        prediction_label.config(text="Введите корректный год!")

window = tk.Tk()
window.title("Предсказатель")
window.geometry("300x150")

label = tk.Label(window, text="Введите год:")
label.pack(pady=5)

entry = tk.Entry(window)
entry.pack(pady=5)

button = tk.Button(window, text="Предсказать", command=predict)
button.pack(pady=5)

prediction_label = tk.Label(window, text="", fg="blue")
prediction_label.pack(pady=10)

window.mainloop()
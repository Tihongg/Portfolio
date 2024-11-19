import matplotlib.pyplot as plt
import numpy as np

def create_random_plots():
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))  # Создаём сетку 2x3 для графиков
    axs = axs.flatten()  # Преобразуем массив осей в одномерный массив для удобства итерации

    for ax in axs:
        random_data = np.random.random(10)  # Генерируем 10 случайных значений
        ax.plot(random_data)  # Строим график на текущей оси
        ax.set_title('Random Plot')  # Устанавливаем заголовок для каждого графика

    plt.tight_layout()  # Обеспечиваем плотное расположение графиков
    plt.show()  # Отображаем графики

create_random_plots()
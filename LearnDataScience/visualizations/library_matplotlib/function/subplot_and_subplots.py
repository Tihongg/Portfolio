import matplotlib.pyplot as plt
import numpy as np

# Функция subplot - дает возможность создать несколько графиков в одном окне
# Параметры subplot:
# 1. Колмчество строк графиков
# 2. Колмчество столбцов графиков
# 3. Индекс окна, в котором вы хотите создать график (изначально графика нету в окне)

# Легкий пример
plt.subplot(2, 3, 1)
plt.plot(np.random.random(10))
plt.clf()

# Для создания сразу всех графиков, можно придумать не сложную конструкцию
for i in range((2 * 3) + 1)[1:]:
    plt.subplot(2, 3, i)
    plt.plot(np.random.random(10))

plt.clf()

# Так же можно вывести графики немного иным образом, так, что бы на одной оси Y было 3 графика а на другом всего 1
plt.subplot(2, 3, 1)
plt.plot(np.random.random(10))

plt.subplot(2, 3, 2)
plt.plot(np.random.random(10))

plt.subplot(2, 3, 3)
plt.plot(np.random.random(10))

plt.subplot(2, 1, 2)
plt.plot(np.random.random(10))

plt.clf()

# Параметры subplot можно указывать и иным способом
plt.subplot(111)  # тоже самое что и (1, 1, 1)
plt.plot(np.random.random(10))
plt.clf()


# Функция subplots - Такие же возможности как и у subplot, но с другим подходом
# Subplots отличаеться тем, что она заранее создает все графики в окне, и возвращает лишь фигуру и ссылки на графики
# Параметры subplots:
# 1. nrows - Колмчество строк графиков
# 2. ncols - столбцов графиков

# Создание графиков
_, axes = plt.subplots(nrows=2, ncols=3)

# Для изменения графика нужно всего лишь обращаться к объектам axes
axes[0, 0].plot(np.random.random(10))
# axes[0, 1].plot(np.random.random(10))
# ...
# axes[1, 2].plot(np.random.random(10))
plt.clf()

# Давайте повторим нашу простую конструкциб по заполнению всех графиков с функцией subplot, только уже через suplots
figure, axes = plt.subplots(2, 3)
axes = axes.flatten()  # Преобразуем массив осей в одномерный массив для удобства итерации

for i in axes:
    i.plot(np.random.random(10))

figure.show()

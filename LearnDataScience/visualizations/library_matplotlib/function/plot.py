import matplotlib.pyplot as plt
import matplotlib

matplotlib.get_backend()  # Возвращает обьект, использующийся в качестве бекенда (для графиков), по умолчанию Tkinter
matplotlib.use("TkAgg")  # Изменяет бекенд

# Рассмотрите chart_structure.jpg, давайте разберем что обозначает каждая часть графика
# 1. Figure - Объект в котором происходит всё рисование
# 2. Axes - Кординатные оси
# 3. X axis label - Подпись кординаты X
# 4. Y axis label - Подпись кординаты Y
# 5. xmin - Минимальное значение x
# 6. xmax - Максимальное значение x
# 7. ymin - Минимальное значение y
# 8. ymax - Максимальное значение y
# 9. Legend - Описание графика
# 10. Grid - Сетка графика

# Начальные знания
plt.show()  # Показывает созданный график
plt.grid()  # Включение сетки на графике
plt.clf()  # очищает фигуру от графиков

# Функция plot - выполняет построение обычных двухмерных графиков
# -- Для просмотра графика используйте show(), сть есть clf() то используйте show() перед функцией очищения
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 2, 4, 6, 4, 2, 3, 1])  # Возвращает двумерный график с вектарами x и y (x не обязательный)
plt.clf()

plt.plot([1, 5, 5, 1, 1], [1, 1, 5, 5, 1])  # прямоугольник
plt.clf()

# Для отображения 2-ых графиков на 1-ой фигуре, в функцию plot можно предеавать 4 аргумента
plt.plot([1, 2, 6], [1, 4, 10], [1, 5, 6], [1, 6, 5])
plt.grid()
plt.clf()

# Или же отобразить несколько графиков можно ным способом
plt.plot([1, 2, 6], [1, 4, 10])
plt.plot([1, 5, 6], [1, 6, 5])
plt.grid()
plt.clf()

# Стиль лииии в графике можно менять, передавая его 3 параметром
plt.plot([1, 2, 3, 4, 5], linestyle='None')  # Пустой
plt.clf()

plt.plot([1, 2, 3, 4, 5], linestyle='solid')  # Прямая
plt.clf()

plt.plot([1, 2, 3, 4, 5], linestyle='dashed')  # Пунктир
plt.clf()

plt.plot([1, 2, 3, 4, 5], linestyle='dashdot')  # Пунктир с точкой
plt.clf()

plt.plot([1, 2, 3, 4, 5], linestyle='dotted')  # Точечный пунктир
plt.clf()

# Так же параметры можно менять через функцию setp
line = plt.plot([1, 2, 3, 4, 5], linestyle='None')
plt.setp(line, linestyle="solid")
plt.clf()

# Цвет графика можно поменять, передав параметр color (hex и rgb поддерживается)
plt.plot([1, 2, 3, 4, 5], linestyle='solid', color="green")
plt.clf()

# В точках изменения направления графика мы можем поставить маркеры, для этого нужно передать соответсвующий параметр - marker
# -- Все виды маркеров можно посмотреть на иозбражении type_markers.jpg + можно указать свой символ в таком формате '$символ$'
marker = plt.plot([1, 2, 1, 2, 1], linestyle='solid', color="green", marker="o")
plt.setp(marker, marker="$OK$")
plt.clf()

# Кроме этого, сам маркер имеет еще несколько свойств
plt.plot([1, 2, 1, 2, 1], linestyle='solid', color="green", marker="o", markerfacecolor="white") # markerfacecolor - изменяет внутренний цвет маркера
plt.clf()

plt.plot([1, 2, 1, 2, 1], linestyle='solid', color="green", marker="o", markeredgecolor="red") # markeredgecolor - изменяет наружный цвет маркера
plt.clf()

plt.plot([1, 2, 1, 2, 1], linestyle='solid', color="green", marker="o", markersize=15) # markersize - изменяет размер маркера
plt.clf()

# На фото Basic_parameters_plot.png можно узнать больше параметров у функции plot, на этом изучение функции plot оконченно


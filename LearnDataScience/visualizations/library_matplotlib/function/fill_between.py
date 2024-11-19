import matplotlib.pyplot as plt
import numpy as np

# Функция fill_between - заполняет цветом промежуток между любыми несколькими линиями или любыми двумя горизонтальными кривыми на 2D графике.
# -- Если вам непонятно что делает фукнция, посмотрите график plt.plot(x, y), и сравните его с ответом функции fill_between
x = [0, 3, 6, 9, 12, 15, 18]
y = [-5, 5, -5, 5, -5, 5, -5]
plt.fill_between(x, y)
plt.grid()
plt.clf()

# Так же функция имеет несколько параметров, давайте их разберем.
# 1. y2 - указывает значеним Y по которому делиться график (по умолчанию - 0)
plt.fill_between(x, y, y2=2)
plt.grid()
plt.clf()

# 2. color - Меняет цвет закраски
plt.fill_between(x, y, color="red")
plt.clf()

# 3. alpha - Меняет прозрачность цвета
plt.fill_between(x, y, alpha=0.5)
plt.clf()

# 4. where - Дает возможность установить условие для закраски
x = np.arange(-2*np.pi, 2*np.pi, 0.1)
y = np.cos(x)
plt.plot(x, y)  # Для видимости границ
plt.fill_between(x, y, where=[y > 0 for y in y], color="green", alpha=0.5)
plt.fill_between(x, y, where=[y < 0 for y in y], color="red", alpha=0.5)
plt.grid()
plt.clf()




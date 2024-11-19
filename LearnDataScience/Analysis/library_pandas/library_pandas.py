import pandas as pd
import numpy as np

read = pd.read_csv('clear_test.csv')

head = read.head()  # Возвращает внешний вид таблицу
print(head)
read.info()  # Выводит информацию о таблице
astype = read['Sex'].astype('bool')  # Меняет тип данных у столбца
describe = read.describe()  # Возвращает разные парметры столбца (mean, std и др.), есть параметр include - для посмотра статистики по нечисловым признакам
value_counts = read['Sex'].value_counts()  # Для категориальных (тип object) и булевых (тип bool) + параметр normalize=True - для просмотра относительных часттот (0.3, 0.4, 0.1, 0.2)
sort_values = read.sort_values(by='Sex', ascending=False).head()  # Сортировка по значениеям, ascending - по возростанию или убыванию
mean = read['Age'].mean()  # Среднее арефметическое строчек в столбце
Mean_sex_is_1 = read[read['Sex'] == True].mean()  # Среднее арефметическое всех строчек, у указанного столбца, если условию верное
loc = read.loc[0:5, 'PassengerId':'Sex']  # Обрезка таблицы по строчкам и столбцам
iloc = read.iloc[0:5, 0:3]  # Обрезка таблицы по строчкам и столбцам
one_row = read[:1]  # Обрезка по строкам ( получение 1 строки)
last_row = read[-1:]  # Обрезка по строкам ( получение последней строки)
apply_columns = read.apply(np.max)  # Применение функции к каждому столбцу
apply_rows = read.apply(np.max, axis=1)  # Применение функции к каждой строке
map = read['Sex'].map({0: False, 1: True})  # Замена значений в столбце по словарю
replace = read.replace({'Sex': {'No': False, 'Yes': True}})  # Замена значений по словарю в столбце
groupby = read.groupby(['Sex'])[['Age', 'Fare', 'Family']]  # Обьеденяет группы
crosstab = pd.crosstab(read['Sex'], read['Title_Mr.'])  # Показывает как наблюдения в нашей выборке распределены в контексте n признаков (в данном случа n = 2)
pivot_table = read.pivot_table(['Title_Miss.', 'Title_Mr.', 'Title_Mrs.'], ['PassengerId'], aggfunc='mean').head(-1)  # Отвечает за сводные таблицы
drop = read.drop([1, 2]).head()  # Удаление строчек (axis = 1, для удаление столбцов (нужно указание название столбцов)
dropna = read.dropna()  # Удаляет строчки, у которых заполнены не все столбцы

shape = read.shape  # Возвращает таблицу (кол-во строк & кол-во столбцов)
columns = read.columns  # Возвращает информацию об столбцах
info = read.info  # Возврощает таблицу в сокращенном формате

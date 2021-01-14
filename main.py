import csv
from datetime import datetime, timedelta
from math import sqrt
import pandas as pd


filepath = "data.csv"


def get_info(filepath):
    """
    скрипт, получает в качестве аргумента путь к CSV-файлу и выдает:
    - общий профит с точностью до цента
    - лучшие продукты по продажам, по количеству продаж и по прибыли соответственно
    - самые худшие продукты по продажам, по количеству продаж и по прибыли соответственно
    - средний срок доставки товара клиенту
    - стандартное отклонение от среднего срока доставки товара клиенту
    - посчитать и вывести в CSV-файл продажи, количество продаж и прибыль по каждому продукту
    """

    list_of_data = []
    # парсинг файла
    with open(filepath, "r") as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            list_of_data.extend([row])

    total_profit = 0
    best_sales = float(list_of_data[1][17].replace(',', '.'))
    best_quantity_product = []
    best_quantity = float(list_of_data[1][18].replace(',', '.'))
    best_sales_product = []
    best_profit = float(list_of_data[1][20].replace(',', '.'))
    best_profit_product = []

    worse_sales = float(list_of_data[1][17].replace(',', '.'))
    worse_sales_product = []
    worse_quantity = float(list_of_data[1][18].replace(',', '.'))
    worse_quantity_product = []
    worse_profit = float(list_of_data[1][20].replace(',', '.'))
    worse_profit_product = []

    for _ in range(1, len(list_of_data)):
        # общий профит
        total_profit += float(list_of_data[_][20].replace(',', '.'))
        # лучшие/худшие продукты по продажам
        if float(list_of_data[_][17].replace(',', '.')) > best_sales:
            best_sales = float(list_of_data[_][17].replace(',', '.'))
        if float(list_of_data[_][17].replace(',', '.')) < worse_sales:
            worse_sales = float(list_of_data[_][17].replace(',', '.'))
        # лучшие/худшие продукты по продажам
        if float(list_of_data[_][18].replace(',', '.')) > best_quantity:
            best_quantity = float(list_of_data[_][18].replace(',', '.'))
        if float(list_of_data[_][18].replace(',', '.')) < worse_quantity:
            worse_quantity = float(list_of_data[_][18].replace(',', '.'))
        # лучшие/худшие продукты по прибыли
        if float(list_of_data[_][20].replace(',', '.')) > best_profit:
            best_profit = float(list_of_data[_][20].replace(',', '.'))
        if float(list_of_data[_][20].replace(',', '.')) < worse_profit:
            worse_profit = float(list_of_data[_][20].replace(',', '.'))

    for _ in range(1, len(list_of_data)):
        if float(list_of_data[_][17].replace(',', '.')) == best_sales:
            best_sales_product.append(list_of_data[_])
        if float(list_of_data[_][18].replace(',', '.')) == best_quantity:
            best_quantity_product.append(list_of_data[_])
        if float(list_of_data[_][20].replace(',', '.')) == best_profit:
            best_profit_product.append(list_of_data[_])
        if float(list_of_data[_][17].replace(',', '.')) == worse_sales:
            worse_sales_product.append(list_of_data[_])
        if float(list_of_data[_][18].replace(',', '.')) == worse_quantity:
            worse_quantity_product.append(list_of_data[_])
        if float(list_of_data[_][20].replace(',', '.')) == worse_profit:
            worse_profit_product.append(list_of_data[_])


    print(f'total_profit: {round(total_profit,2)}')    # округление до цента

    print(f'best_sales: {best_sales} and {len(best_sales_product)} product(s) is: {best_sales_product}')
    print(f'best_quantity: {best_quantity} and {len(best_quantity_product)} product(s) is: {best_quantity_product}')
    print(f'best_profit: {best_profit} and {len(best_profit_product)} product(s) is: {best_profit_product}')

    print(f'worse_sales: {worse_sales} and {len(worse_sales_product)} product(s) is: {worse_sales_product}')
    print(f'worse_quantity: {worse_quantity} and {len(worse_quantity_product)} product(s) is: {worse_quantity_product}')
    print(f'worse_profit: {worse_profit} and {len(worse_profit_product)} product(s) is: {worse_profit_product}')

    # средний срок доставки товара клиенту
    dateFormatter = [r'%m/%d/%y', "%m.%d.%Y"]
    sum_delivery_time = 0

    for _ in range(1, len(list_of_data)):
        for ft in dateFormatter:
            try:
                order_date = datetime.strptime(list_of_data[_][2], ft)
            except:
                pass
            try:
                ship_date = datetime.strptime(list_of_data[_][3], ft)
            except:
                pass

        delivery_time = ship_date - order_date
        sum_delivery_time += int(delivery_time.total_seconds())
    average_delivery_time = sum_delivery_time/(len(list_of_data)-1)
    print(f'the average delivery time is {average_delivery_time / 86400} days')

    # стандартное отклонение
    difference = 0
    for _ in range(1, len(list_of_data)):
        for ft in dateFormatter:
            try:
                order_date = datetime.strptime(list_of_data[_][2], ft)
            except:
                pass
            try:
                ship_date = datetime.strptime(list_of_data[_][3], ft)
            except:
                pass

        delivery_time1 = ship_date - order_date
        difference += (delivery_time1.total_seconds() - average_delivery_time)**2
    standard_deviation = sqrt((difference)/(len(list_of_data) - 2))
    print(f'standard deviation: {standard_deviation/ 86400} days')


    # посчитать и вывести в CSV-файл продажи, количество продаж и прибыль по каждому продукту
    di = []
    res = []
    for _ in range(1, len(list_of_data)):
        di.append([list_of_data[_][13], float(list_of_data[_][17].replace(',', '.')), int(list_of_data[_][18].replace(',', '.')), float(list_of_data[_][20].replace(',', '.'))])
    print(di)

    res.append(di[0])
    # print(res)
    for _ in range(1, len(di)):
        # print(di[_][0])
        triger = True
        for i in range(len(res)):
            # print(res[i][0])
            if res[i][0] == di[_][0]:
                triger = False
                break
        if triger:
            res.append(di[_])
        else:
            res[i][1] += float(di[_][1])
            res[i][2] += int(di[_][2])
            res[i][3] += float(di[_][3])
    print(res)

    lst1 = [res[_][0] for _ in range(len(res))]
    lst2 = [res[_][1] for _ in range(len(res))]
    lst3 = [res[_][2] for _ in range(len(res))]
    lst4 = [res[_][3] for _ in range(len(res))]

    data = dict(Product_ID=lst1, Sales=lst2, Quantity=lst3, Profit=lst4)

    df = pd.DataFrame(data)

    df.to_csv('res.csv', sep=';', index=False)








get_info(filepath)


from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import urllib.request
import xml.dom.minidom
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def clicked():
    lblOut.configure(text="Я же просил...")
    name1 = valuta1.get()
    name2 = valuta2.get()
    name1_value = 0.0
    name2_value = 0.0
    name1_nominal = 0
    name2_nominal = 0

    for element in full_info:
        if element['Name'] == name1:
            name1_value = element['Value']
            name1_nominal = element['Nominal']
        if element['Name'] == name2:
            name2_value = element['Value']
            name2_nominal = element['Nominal']
    if txt.get() != "":
        number = float(txt.get())
    else:
        number = 0

    name1_value = float('.'.join(name1_value.split(',')))
    name2_value = float('.'.join(name2_value.split(',')))
    name1_nominal = int(name1_nominal)
    name2_nominal = int(name2_nominal)

    finale_num = number * name1_value / name1_nominal / name2_value * name2_nominal
    print(str(number) + " * " + str(name1_value) + " / " + str(name1_nominal) + " / "
          + str(name2_value) + " * " + str(name2_nominal) + " = " + str(finale_num))
    lblOut.configure(text="Результат: '" + str(finale_num) + "'")


def today_info(data_today):
    response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + data_today)
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    node_array = dom.getElementsByTagName("Valute")
    print(len(node_array))
    array_value = []
    z = 0
    for node in node_array:
        child_list = node.childNodes
        array_value.append({})
        for child in child_list:
            print(child.nodeName + ": " + child.childNodes[0].nodeValue)
            if str(child.nodeName) == "NumCode":
                array_value[z]['NumCode'] = child.childNodes[0].nodeValue
            if str(child.nodeName) == "CharCode":
                array_value[z]['CharCode'] = child.childNodes[0].nodeValue
            if str(child.nodeName) == "Nominal":
                array_value[z]['Nominal'] = child.childNodes[0].nodeValue
            if str(child.nodeName) == "Name":
                array_value[z]['Name'] = child.childNodes[0].nodeValue
            if str(child.nodeName) == "Value":
                array_value[z]['Value'] = child.childNodes[0].nodeValue
        print(str(array_value[z]) + "\n")
        z = z + 1
    return array_value


def clicked_2():
    arr_x = []
    arr_y = []
    name_value = valuta1_2.get()
    month = valuta2_2.get()
    month_num = 0
    for i in range(0, len(months)):
        if month == last_months[i]:
            month_num = i + 1
            break
    num_days = int(28 + (month_num + (month_num/8)) % 2 + 2 % month_num + 2 * (1 / month_num))
    for i in range(1, num_days + 1):
        arr_x.append(int(i))
    if month_num + 1 <= 10:
        month_num_string = "0" + str(month_num)
    else:
        month_num_string = str(month_num)
        print(month_num_string)
    for num_x in arr_x:
        if num_x + 1 <= 10:
            num_x_string = "0" + str(num_x)
        else:
            num_x_string = str(num_x)
        date = num_x_string + "/" + month_num_string + "/" + str(data_year_2)
        arr_y.append(last_year_info(date, name_value))

    print(arr_x)
    print(arr_y)

    fig.clear()
    plt.plot(arr_x, arr_y)
    plt.draw()
    return 0


def last_year_info(date, name):
    response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date)
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    node_array = dom.getElementsByTagName("Valute")
    float_num = 0
    for node in node_array:
        child_list = node.childNodes
        for child in child_list:
            if str(child.nodeName) == "Name":
                if child.childNodes[0].nodeValue == name:
                    for c in child_list:
                        if str(c.nodeName) == "Value":
                            float_num = c.childNodes[0].nodeValue
                            float_num = float('.'.join(float_num.split(',')))
                            break
                    break
    return float_num


# Настройка окна
window = Tk()
window.title("Конвертер валют")
window.geometry('800x700')

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

# 1 вкладка
# Получение данных
data_year = str(datetime.date.today().year)
data_month = str(datetime.date.today().month)
if len(data_month) < 2:
    data_month = "0" + data_month
data_day = str(datetime.date.today().day)
if len(data_day) < 2:
    data_day = "0" + data_day
data = data_day + "/" + data_month + "/" + data_year
full_info = today_info(data)

array_names = []
for element in full_info:
    array_names.append(element['Name'])

tab_control.add(tab1, text="Курсы валют")

valuta1 = Combobox(tab1)
valuta1['values'] = array_names
valuta1.current(16)
valuta1.grid(column=1, row=1)

valuta2 = Combobox(tab1)
valuta2['values'] = array_names
valuta2.current(18)
valuta2.grid(column=3, row=1)

txt = Entry(tab1, width=10)
txt.grid(column=1, row=3)

lblOut = Label(tab1, text="Результат: ")
lblOut.grid(column=3, row=3)

btn = Button(tab1, text="Конвертировать.", command=clicked)
btn.grid(column=5, row=1)

lbl1 = Label(tab1, text=' ')
lbl1.grid(column=0, row=0)
lbl1 = Label(tab1, text=' ')
lbl1.grid(column=0, row=2)
lbl1 = Label(tab1, text=' ')
lbl1.grid(column=2, row=1)
lbl1 = Label(tab1, text=' ')
lbl1.grid(column=4, row=1)

# 2 вкладка
# Получение данных
data_year_2 = datetime.date.today().year - 1
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
last_months = []
for i in range(0, len(months)):
    last_months.append(str(months[i] + " " + str(data_year_2)))

tab_control.add(tab2, text='График')

valuta1_2 = Combobox(tab2)
valuta1_2['value'] = array_names
valuta1_2.current(11)
valuta1_2.grid(column=0, row=0)

valuta2_2 = Combobox(tab2)
valuta2_2['value'] = last_months
valuta2_2.current(0)
valuta2_2.grid(column=0, row=2)

btn_2 = Button(tab2, text="График", command=clicked_2)
btn_2.grid(column=0, row=4)

matplotlib.use('TkAgg')
fig = plt.figure()
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
plot_widget = canvas.get_tk_widget()
plt.grid()
plot_widget.grid(row=6, column=1)

lbl2 = Label(tab2, text=' ')
lbl2.grid(column=0, row=1)
lbl2 = Label(tab2, text=' ')
lbl2.grid(column=0, row=3)
lbl2 = Label(tab2, text=' ')
lbl2.grid(column=0, row=5)

tab_control.pack(expand=1, fill='both')
window.mainloop()

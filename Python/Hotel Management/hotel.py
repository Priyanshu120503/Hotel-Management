import math
import tkinter
from tkinter import messagebox
import random
from datetime import date, datetime
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import time


def add_food(f):
    if f == '' or qty.get() == 0:
        return
    elif table.get() == 0:
        messagebox.showinfo(title='Invalid Table', message='Orders cannot be taken for Table 0')
    else:
        if selected_food.get(table.get()) and f in selected_food[table.get()]:
            idx = 0
            for item in order_list_box.get(0, len(selected_food[table.get()]) - 1):
                if f in item:
                    break
                idx += 1
            total.set(
                total.get() - int(order_list_box.get(idx)[30:33].strip()) * int(order_list_box.get(idx)[45:48].strip()))
            order_list_box.delete(idx)
            order_list_box.insert(idx, f'{f}{qty.get():3d}')
        else:
            order_list_box.insert(tkinter.END, f'{f}{qty.get():3d}')
            selected_food[table.get()] = [f] if not selected_food.get(table.get()) else selected_food[table.get()] + [f]
        total.set(total.get() + int(f[30:33].strip()) * qty.get())
        # print(selected_food)
        global added_food
        added_food = True
        global prev_table
        prev_table = table.get()
        global final_save
        final_save = False


def update_order_box():
    """ Returns True if a table is already active else returns False """
    # print('Inside update order')
    order_list_box.delete(0, order_list_box.size())
    # print('Cleared Order Box')
    # print(active_tables)
    # print(f'Prev table = {prev_table}      Cur Table={table.get()}')
    if table.get() in active_tables and not final_save:
        cur.execute(f'SELECT * FROM Orders WHERE Table_no = {table.get()}')
        p = cur.fetchall()[-1]
        c_id.set(p[0])
        for item in p[2].split(','):
            order_list_box.insert(order_list_box.size(), item)
        total.set(p[3])
        payment_mode.set(p[4])
        return True
    total.set(0)
    return False


def goto_table(t):
    ran_id = random.randint(2000000, 3000000)
    cur.execute('SELECT Id FROM Orders')
    while ran_id in [i[0] for i in cur.fetchall()]:
        ran_id = random.randint(2000000, 3000000)
    # while ran_id in cust_id_list:
    #     ran_id = random.randint(2000000, 3000000)
    global prev_table
    # if prev_table == table.get():
    #     # print('Inside 1st if')
    #     return
    chosen_table_var.set(t)
    if prev_table == 0 and table.get() > 0:
        # print('Inside 2nd if')
        c_id.set(ran_id)
        cust_id_list.append(ran_id)
        prev_table = table.get()
        return
    global added_food, removed_food
    if not added_food and not removed_food:
        pass
    else:
        update_database()
    # print('Above update database')
    # print('Below update database')
    if update_order_box():
        # print('Inside update order box if')
        pass
    else:
        # print('Inside update order box else')
        c_id.set(ran_id)
        cust_id_list.append(ran_id)
    added_food = False
    removed_food = False


def update_database():
    # cur.execute("""SELECT name FROM sqlite_master
    #     WHERE type='table';""")
    # tables_in_database = cur.fetchall()
    # if any([tables_in_database[i][0] == f'Table {table.get()}' for i in range(len(tables_in_database))]):
    #     pass
    # else:
    # cur.execute(f'CREATE TABLE \'Table {table.get()}\'(Id INTEGER, Date TEXT, Items TEXT, Total INTEGER)')
    global prev_table
    # print(f'Prev table = {prev_table}      Cur Table={table.get()}')
    if prev_table == 0:
        return
    # print(f'Prev table = {prev_table}      Cur Table={table.get()}')
    cur.execute(f'SELECT * FROM Orders WHERE Id = {c_id.get()}')
    if cur.fetchone():
        cur.execute(f'DELETE FROM Orders WHERE Id = {c_id.get()}')
        # cur.execute(f'UPDATE Orders SET Items = {",".join(order_list_box.get(0, order_list_box.size()-1))}, Total = {total.get()} WHERE Id = {c_id.get()}')
        active_tables.remove(prev_table)
        # print(active_tables)
    cur.execute(f'INSERT INTO Orders VALUES(?, ?, ?, ?, ?, ?)',
                (c_id.get(),
                 date_var.get(),
                 ','.join(order_list_box.get(0, order_list_box.size())),
                 total.get(),
                 payment_mode.get(),
                 prev_table))
    active_tables.append(prev_table)
    # print(active_tables)
    cur.execute(f'SELECT * FROM Orders')
    # print(cur.fetchall())
    con.commit()


def remove_food():
    idx = order_list_box.curselection()
    if idx:
        listing = order_list_box.get(idx[0])
        total.set(total.get() - int(listing[30:33].strip()) * int(listing[45:48].strip()))
        for item in selected_food[table.get()]:
            if item in listing:
                selected_food[table.get()].remove(item)
                break
        order_list_box.delete(idx[0])
        global removed_food
        removed_food = True


def save_and_clear():
    selected_food[table.get()] = []
    global final_save
    final_save = True
    goto_table(table.get())
    global added_food, removed_food
    added_food = False
    removed_food = False
    active_tables.remove(table.get())
    final_save = False


# def get_data():
#     months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
#               9: 'September', 10: 'October', 11: 'November', 12: 'December'}
#     if stats_table.get() > 0:
#         if any([v == 0 for v in [int(day.get()), month.get(), year.get()]]):
#             cur.execute(f'SELECT * FROM Orders WHERE Table_no={stats_table.get()}')
#         else:
#             if (year.get() % 4 == 0 and month.get() == 2 and int(day.get()) > 29) or \
#                     (month.get() in [4, 6, 9, 11] and int(day.get()) == 31) or \
#                     (year.get() % 4 != 0 and month.get() == 2 and int(day.get()) > 28):
#                 messagebox.showinfo(title='Error', message='Invalid Date')
#                 return
#             else:
#                 cur.execute(f'SELECT * FROM Orders WHERE Table_no={stats_table.get()} AND Date="{months[month.get()]} {day.get()}, {year.get()}"')
#         [# print(item) for item in cur.fetchall()]
#     else:
#         if any([v.get() == 0 for v in [day, month, year]]):
#             pass
#         elif (year.get() % 4 == 0 and month.get() == 2 and int(day.get()) > 29) or \
#                 (month.get() in [4, 6, 9, 11] and int(day.get()) == 31) or \
#                 (year.get() % 4 != 0 and month.get() == 2 and int(day.get()) > 28):
#             messagebox.showinfo(title='Error', message='Invalid Date')
#             return
#         else:
#             cur.execute(f'SELECT * FROM Orders WHERE Date="{months[month.get()]} {day.get()}, {year.get()}"')
#             [# print(item) for item in cur.fetchall()]
#     # print('-------------------------')
#     plot(Date=[f"{months[month.get()]} {day.get()}, {year.get()}", "December 05, 2022"])

def del_stats_frame():
    global stats_frame
    stats_frame.destroy()


def add_stats_frame():
    global chart_image, stats_label, selected_option, stats_options, stats_options_label, stats_options_dropdown, stats_frame, select_button
    stats_frame = tkinter.Frame(window, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT / 2, bg='#d4f2a0',
                                relief=tkinter.RAISED, bd=3)

    stats_label = tkinter.Label(stats_frame, text='Statictics', font=('Bookman Old Style', 30, 'normal'),
                                image=chart_image,
                                compound='right', bg='white')

    stats_options = ['Total Earning vs Date', 'Earning per Table vs Date', 'Payment Method']
    stats_options_label = tkinter.Label(stats_frame, text='Plot', font=('Courier', 15))
    stats_options_dropdown = tkinter.OptionMenu(stats_frame, selected_option, *stats_options)

    select_button = tkinter.Button(stats_frame, text='Select', font=('Arial', 15), command=get_data)

    stats_label.place(x=50, y=50)
    stats_options_label.place(x=380, y=50)
    stats_options_dropdown.place(x=450, y=50)
    select_button.place(x=50, y=300)
    stats_frame.place(x=0, y=SCREEN_HEIGHT / 2)


def get_data():
    # print('Inside Get data')
    # months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07',
    #           'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    del_stats_frame()
    # print('Below delete')
    add_stats_frame()
    # print('Below add')
    if selected_option.get() == 'Total Earning vs Date':
        from_stats_date_label = tkinter.Label(stats_frame, text='From', padx=20, font=LABEL_FONT)
        from_day = tkinter.StringVar()
        from_day.set('01')
        from_month = tkinter.StringVar()
        from_month.set('01')
        from_year = tkinter.IntVar()
        from_year.set('2022')
        from_month_dropdown = tkinter.OptionMenu(stats_frame, from_month, *['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
        from_year_dropdown = tkinter.OptionMenu(stats_frame, from_year, *[2022, 2023])
        from_day_dropdown = tkinter.OptionMenu(stats_frame, from_day, *(
                ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(i) for i in range(10, 32)]))
        from_forward_slash_label_1 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))
        from_forward_slash_label_2 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))

        to_stats_date_label = tkinter.Label(stats_frame, text='Till', padx=20, font=LABEL_FONT)
        to_day = tkinter.StringVar()
        to_day.set('01')
        to_month = tkinter.StringVar()
        to_month.set('01')
        to_year = tkinter.IntVar()
        to_year.set('2022')
        to_month_dropdown = tkinter.OptionMenu(stats_frame, to_month, *['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
        to_year_dropdown = tkinter.OptionMenu(stats_frame, to_year, *[2022, 2023])
        to_day_dropdown = tkinter.OptionMenu(stats_frame, to_day, *(
                ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(i) for i in range(10, 32)]))
        to_forward_slash_label_1 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))
        to_forward_slash_label_2 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))

        get_plot_button = tkinter.Button(stats_frame, text='Get Plot', font=('Arial', 15),
                                         command=lambda: plot(Date=np.arange(np.datetime64(
                                             f'{from_year.get()}-{from_month.get()}-{from_day.get()}'),
                                                np.datetime64(f'{to_year.get()}-{to_month.get()}-{to_day.get()}'))))

        from_stats_date_label.place(x=50, y=240)
        from_day_dropdown.place(x=150, y=240)
        from_month_dropdown.place(x=220, y=240)
        from_year_dropdown.place(x=290, y=240)
        from_forward_slash_label_1.place(x=200, y=235)
        from_forward_slash_label_2.place(x=270, y=235)

        to_stats_date_label.place(x=400, y=240)
        to_day_dropdown.place(x=480, y=240)
        to_month_dropdown.place(x=550, y=240)
        to_year_dropdown.place(x=620, y=240)
        to_forward_slash_label_1.place(x=530, y=235)
        to_forward_slash_label_2.place(x=600, y=235)

        get_plot_button.place(x=600, y=300)

    elif selected_option.get() == 'Earning per Table vs Date':
        stats_table_label = tkinter.Label(stats_frame, text="Table No.", padx=14, font=LABEL_FONT, relief=tkinter.RIDGE,
                                          bd=2)
        checkbutton_vars = [tkinter.IntVar() for _ in range(1, 10)]
        for (i, j) in zip(checkbutton_vars, range(1, 10)):
            i.set(0)
            temp = tkinter.Checkbutton(stats_frame, variable=i, text=f'{j}')
            temp.place(x=120+(j*50), y=150)

        stats_table_label.place(x=50, y=150)

        from_stats_date_label = tkinter.Label(stats_frame, text='From', padx=20, font=LABEL_FONT)
        from_day = tkinter.StringVar()
        from_day.set('01')
        from_month = tkinter.StringVar()
        from_month.set('01')
        from_year = tkinter.IntVar()
        from_year.set('2022')
        from_month_dropdown = tkinter.OptionMenu(stats_frame, from_month, *['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
        from_year_dropdown = tkinter.OptionMenu(stats_frame, from_year, *[2022, 2023])
        from_day_dropdown = tkinter.OptionMenu(stats_frame, from_day, *(
                ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(i) for i in range(10, 32)]))
        from_forward_slash_label_1 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))
        from_forward_slash_label_2 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))

        to_stats_date_label = tkinter.Label(stats_frame, text='Till', padx=20, font=LABEL_FONT)
        to_day = tkinter.StringVar()
        to_day.set('01')
        to_month = tkinter.StringVar()
        to_month.set('01')
        to_year = tkinter.IntVar()
        to_year.set('2022')
        to_month_dropdown = tkinter.OptionMenu(stats_frame, to_month, *['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
        to_year_dropdown = tkinter.OptionMenu(stats_frame, to_year, *[2022, 2023])
        to_day_dropdown = tkinter.OptionMenu(stats_frame, to_day, *(
                ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(i) for i in range(10, 32)]))
        to_forward_slash_label_1 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))
        to_forward_slash_label_2 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))

        get_plot_button = tkinter.Button(stats_frame, text='Get Plot', font=('Arial', 15),
                                         command=lambda: plot(Date=np.arange(np.datetime64(
                                             f'{from_year.get()}-{from_month.get()}-{from_day.get()}'),
                                             np.datetime64(f'{to_year.get()}-{to_month.get()}-{to_day.get()}')),
                                             Table=[i for (i, j) in zip(range(1, 10), checkbutton_vars) if j.get() == 1]))

        from_stats_date_label.place(x=50, y=240)
        from_day_dropdown.place(x=150, y=240)
        from_month_dropdown.place(x=220, y=240)
        from_year_dropdown.place(x=290, y=240)
        from_forward_slash_label_1.place(x=200, y=235)
        from_forward_slash_label_2.place(x=270, y=235)

        to_stats_date_label.place(x=400, y=240)
        to_day_dropdown.place(x=480, y=240)
        to_month_dropdown.place(x=550, y=240)
        to_year_dropdown.place(x=620, y=240)
        to_forward_slash_label_1.place(x=530, y=235)
        to_forward_slash_label_2.place(x=600, y=235)

        get_plot_button.place(x=600, y=300)
    elif selected_option.get() == 'Payment Method':
        cur.execute('SELECT "Payment Mode" FROM Orders')
        p = {}
        for i in [j[0] for j in cur.fetchall()]:
            p[i] = 1 if not p.get(i) else p[i] + 1
        # # print(p)
        get_plot_button = tkinter.Button(stats_frame, text='Get Plot', font=('Arial', 15),
                                         command=lambda: plot(Payment=p))
        get_plot_button.place(x=600, y=300)


def plot(**kwargs):
    # ------ Total Earning vs Date-------------------------
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    if 'Date' in kwargs.keys() and len(kwargs) == 1:
        # # print(kwargs['Date'])
        if len(kwargs['Date']) == 0:
            return
        dates_list = [t.item().strftime('%Y-%m-%d') for t in kwargs['Date']]
        # print(dates_list)
        dates_list = [f'{months[int(d[5:7])]} {d[8:]}, {d[:4]}' for d in dates_list]
        dates_tuple = tuple(dates_list + [''])
        # print(dates_tuple)
        cur.execute(f'SELECT Date, Total FROM Orders WHERE Date in {dates_tuple}')
        d = {}
        for (key, value) in cur.fetchall():
            d[key] = value if not d.get(key) else d[key] + value
        # print(d)
        fig, axs = plt.subplots(2)
        axs[0].bar(list(d.keys()), list(d.values()))
        axs[1].plot(list(d.keys()), list(d.values()))
        plt.xlabel('Date', size=15)
        plt.ylabel('Earning', size=15)
        fig.tight_layout(pad=1)
    # ---------- Earning on Table 't' vs Date -------------------
    elif 'Date' in kwargs.keys() and 'Table' in kwargs.keys() and len(kwargs) == 2:
        if len(kwargs['Date']) == 0 or len(kwargs['Table']) == 0:
            return
        dates_list = [t.item().strftime('%Y-%m-%d') for t in kwargs['Date']]
        dates_list = [f'{months[int(d[5:7])]} {d[8:]}, {d[:4]}' for d in dates_list]
        dates_tuple = tuple(dates_list + [''])

        table_data = {key: '' for key in kwargs['Table']}
        for table_no in kwargs['Table']:
            cur.execute(f'SELECT Date, Total FROM Orders WHERE Table_no={table_no} AND Date in {dates_tuple}')
            d = {}
            for (key, value) in cur.fetchall():
                d[key] = value if not d.get(key) else d[key] + value
            table_data[table_no] = d
        # print(table_data)
        req_tables = kwargs['Table']
        # print(req_tables)

        if len(req_tables) == 1:
            fig, axs = plt.subplots(1)
            axs.set_title(f'Table no. {req_tables[0]}')
            axs.bar(table_data[req_tables[0]].keys(), table_data[req_tables[0]].values(), width=0.5)
        elif len(req_tables) <= 3:
            fig, axs = plt.subplots(len(req_tables))
            for i in range(len(req_tables)):
                axs[i].set_title(f'Table no. {req_tables[i]}')
                axs[i].bar(table_data[req_tables[i]].keys(), table_data[req_tables[i]].values(), width=0.5)
        else:
            fig, axs = plt.subplots(math.ceil(len(req_tables) / 3), 3)
            t = 0
            for i in range(math.ceil(len(req_tables) / 3)):
                for j in range(3):
                    # print(t)
                    axs[i, j].set_title(f'Table no. {req_tables[t]}')
                    axs[i, j].bar(table_data[req_tables[t]].keys(), table_data[req_tables[t]].values(), width=0.5)
                    t += 1
                    if t == len(req_tables):
                        break
        fig.tight_layout(pad=1)
    elif 'Payment' in kwargs:
        plt.bar(list(kwargs['Payment'].keys()), list(kwargs['Payment'].values()))

    plt.show()


def time_update():
    time_now = datetime.now().strftime("%H:%M:%S")
    time_var.set(time_now)
    time_label.after(1000, time_update)


def confirm_close():
    res = tkinter.messagebox.askquestion(title='Exit Application', message='Do you really want to exit')
    if res == 'yes':
        window.destroy()


window = tkinter.Tk()
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight() - 70
window.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
window.title('Order Management')

con = sqlite3.connect('hotel_data.db')
cur = con.cursor()

added_food = False
removed_food = False
final_save = False

LABEL_FONT = ('Californian FB', 15, 'normal')

menu_frame = tkinter.Frame(window, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT / 2, bg='#a1fc03',
                           relief=tkinter.RAISED, bd=3)
stats_frame = tkinter.Frame(window, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT / 2, bg='#d4f2a0',
                            relief=tkinter.RAISED, bd=3)
bill_frame = tkinter.Frame(window, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT, bg='#ffb947', relief=tkinter.RAISED,
                           bd=3)

# ----------------Menu Frame-------------------

# Just add a tuple of (food_name, price) in the below list
food_name_price = [('Aloo Paraatha', 50), ('Paneer Paraatha', 100), ('Paneer Butter Masala', 150),
                   ('Chole Bhature', 120), ('Aloo Gobi Tandoori', 200), ('Hara Bhara Kabab', 215), ('Dal Makhani', 180),
                   ('Veg. Kofta', 200), ('Paneer Do Pyaza', 230), ('Paneer Masala', 230), ('Paneer Palak', 250),
                   ('Paneer Patiyala', 250), ('Roti', 20), ('Butter Roti', 30), ('Butter Naan', 60), ('Kulcha', 40),
                   ('Butter Kulcha', 50), ('Veg Pulav', 190), ('Veg. Biryani', 205), ('Jeera Rice', 125)]
foods = ['{:<30s}{:<15d}'.format(food[0], food[1]) for food in food_name_price]

selected_food = {0: []}
food = tkinter.StringVar()
menu_label = tkinter.Label(menu_frame, text="Select Dish", height=2)
menu_drop_down = tkinter.OptionMenu(menu_frame, food, *foods)
menu_drop_down.config(width=40)

qty = tkinter.IntVar()
qty_spinbox = tkinter.Spinbox(menu_frame, from_=0, to=10, textvariable=qty, width=2, font=('Arial', 15, 'normal'),
                              state='readonly')
# qty = qty_spinbox.get()

arrow_photo = tkinter.PhotoImage(file='images/free-green-arrow-right-icon_1.png')
arrow_button = tkinter.Button(menu_frame, image=arrow_photo, relief=tkinter.RAISED,
                              command=lambda: add_food(food.get()))

# food_label = tkinter.Label(menu_frame, textvariable=food)
name_label_2 = tkinter.Label(menu_frame, text='Mini Punjab', font=('Berlin Sans FB Demi', 60, 'normal'), width=10,
                             bg='#a1fc03', fg='Orange')
name_label_1 = tkinter.Label(menu_frame, text='Hotel', font=('Berlin Sans FB Demi', 60, 'normal'), width=10,
                             bg='#a1fc03', fg='Orange')

menu_label.place(x=80, y=250)
menu_drop_down.place(x=180, y=250)
qty_spinbox.place(x=480, y=250)
arrow_button.place(x=550, y=250)
# food_label.place(x=50, y=150)
name_label_1.place(x=115, y=40)
name_label_2.place(x=115, y=120)
# -------------------------------------------------

# ----------------Stats Frame---------------------------------
chart_image = tkinter.PhotoImage(file='images/bar_chart_1.png')
stats_label = tkinter.Label(stats_frame, text='Statictics', font=('Bookman Old Style', 30, 'normal'), image=chart_image,
                            compound='right', bg='white')

selected_option = tkinter.StringVar()
stats_options = ['Total Earning vs Date', 'Earning per Table vs Date', 'Payment Method']
selected_option.set(stats_options[0])
stats_options_label = tkinter.Label(stats_frame, text='Plot', font=('Courier', 15))
stats_options_dropdown = tkinter.OptionMenu(stats_frame, selected_option, *stats_options)

# stats_table_label = tkinter.Label(stats_frame, text="Table No.", padx=14, font=LABEL_FONT, relief=tkinter.RIDGE, bd=2)
# stats_table = tkinter.IntVar()
# stats_table.set(0)
# stats_table_drop_down = tkinter.OptionMenu(stats_frame, stats_table, *[i for i in range(0, 10)])
#
# stats_date_label = tkinter.Label(stats_frame, text='From', padx=20, font=LABEL_FONT)
# day = tkinter.StringVar()
# day.set('00')
# month = tkinter.IntVar()
# year = tkinter.IntVar()
# month_dropdown = tkinter.OptionMenu(stats_frame, month, *[i for i in range(0, 13)])
# year_dropdown = tkinter.OptionMenu(stats_frame, year, *[2022, 2023])
# day_dropdown = tkinter.OptionMenu(stats_frame, day, *(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(i) for i in range(10, 32)]))
# forward_slash_label_1 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))
# forward_slash_label_2 = tkinter.Label(stats_frame, text='/', bg='#d4f2a0', font=('Arial', 25))

select_button = tkinter.Button(stats_frame, text='Select', font=('Arial', 15), command=get_data)

stats_label.place(x=50, y=50)
stats_options_label.place(x=380, y=50)
stats_options_dropdown.place(x=450, y=50)
# stats_table_label.place(x=50, y=150)
# stats_table_drop_down.place(x=180, y=150)
# stats_date_label.place(x=50, y=240)
# day_dropdown.place(x=180, y=240)
# month_dropdown.place(x=250, y=240)
# year_dropdown.place(x=320, y=240)
# forward_slash_label_1.place(x=230, y=235)
# forward_slash_label_2.place(x=300, y=235)
select_button.place(x=50, y=300)
# ------------------------------------------------------------

# -----------------Bill Frame------------------------
cust_id_label = tkinter.Label(bill_frame, text='Customer Id ', font=LABEL_FONT, relief=tkinter.RIDGE, bd=2)
c_id = tkinter.IntVar()
c_id.set(0)
cust_id_list = []
cust_id = tkinter.Label(bill_frame, textvariable=c_id, font=LABEL_FONT, padx=4, relief=tkinter.GROOVE, bd=2)

table_label = tkinter.Label(bill_frame, text="Table No.", padx=14, font=LABEL_FONT, relief=tkinter.RIDGE, bd=2)
tables = [i for i in range(1, 10)]
table = tkinter.IntVar()
table.set(0)
prev_table = 0
table_drop_down = tkinter.OptionMenu(bill_frame, table, *tables)
active_tables = []
arrow_button_2 = tkinter.Button(bill_frame, image=arrow_photo, relief=tkinter.RAISED,
                                command=lambda: goto_table(table.get()))

chosen_table_var = tkinter.IntVar()
chosen_table = tkinter.Label(bill_frame, textvariable=chosen_table_var, padx=5, pady=10, font=LABEL_FONT)
chosen_table_label = tkinter.Label(bill_frame, text='Working on Table no.', wraplength=120, font=LABEL_FONT)

today = date.today()
d = today.strftime("%B %d, %Y")
date_var = tkinter.StringVar()
date_var.set(d)
date_label = tkinter.Label(bill_frame, text="Date", padx=34, font=LABEL_FONT, relief=tkinter.RIDGE, bd=2)
today_date_label = tkinter.Label(bill_frame, textvariable=date_var, font=LABEL_FONT, relief=tkinter.GROOVE, bd=2)

time_var = tkinter.StringVar()

time_now = datetime.now().strftime("%H:%M:%S")
time_var.set(time_now)

time_label = tkinter.Label(bill_frame, text="Time", width=10, font=LABEL_FONT, relief=tkinter.RIDGE, bd=2)
current_time_label = tkinter.Label(bill_frame, textvariable=time_var, font=LABEL_FONT, relief=tkinter.GROOVE, bd=2)

order_label = tkinter.Label(bill_frame, font=('Courier', 15, 'normal'),
                            text='{0:<30s}{1:15s}{2:5s}'.format("Name", "Price", "Qty."))
order_list_box = tkinter.Listbox(bill_frame, width=50, height=16, bg='white', relief=tkinter.GROOVE, bd=5,
                                 selectmode=tkinter.SINGLE, activestyle='dotbox', font=('Courier', 15, 'normal'))

total = tkinter.IntVar()
total_text_label = tkinter.Label(bill_frame, text="Total", font=('Bodoni MT', 15, 'normal'), relief=tkinter.RIDGE)
total_label = tkinter.Label(bill_frame, textvariable=total, font=('Bodoni MT', 15, 'normal'), width=4)

# To add the order data to the database
add_button = tkinter.Button(bill_frame, text='Add', command=update_database, font=LABEL_FONT)

save_and_clear_button = tkinter.Button(bill_frame, text='Save and Clear Table', command=save_and_clear, font=LABEL_FONT)

payment_mode_label = tkinter.Label(bill_frame, text="Payment Mode", font=LABEL_FONT)
payment_options = ['Cash', 'Credit/Debit Card', 'UPI', 'Online Payment']
payment_mode = tkinter.StringVar()
payment_mode.set('Cash')
payment_dropdown = tkinter.OptionMenu(bill_frame, payment_mode, *payment_options)
payment_dropdown.config(width=15)

# Whenever a food is clicked in the order frame and remove is used. Remove that from the frame.
delete_button = tkinter.Button(bill_frame, text='Remove', command=remove_food, font=LABEL_FONT)

close_button = tkinter.Button(bill_frame, text="Close", command=confirm_close, font=LABEL_FONT)

cust_id_label.place(x=50, y=50)
cust_id.place(x=170, y=50)

table_label.place(x=50, y=90)
table_drop_down.place(x=170, y=90)
arrow_button_2.place(x=230, y=90)
chosen_table_label.place(x=500, y=50)
chosen_table.place(x=620, y=55)

date_label.place(x=50, y=130)
today_date_label.place(x=170, y=130)
time_label.place(x=450, y=130)
current_time_label.place(x=580, y=130)
order_label.place(x=50, y=200)
order_list_box.place(x=50, y=230)
total_text_label.place(x=340, y=620)
total_label.place(x=410, y=620)
payment_mode_label.place(x=50, y=670)
payment_dropdown.place(x=190, y=670)
delete_button.place(x=580, y=670)
add_button.place(x=50, y=720)
save_and_clear_button.place(x=280, y=720)
close_button.place(x=600, y=720)
# ----------------------------------------------------
menu_frame.place(x=0, y=0)
stats_frame.place(x=0, y=SCREEN_HEIGHT / 2)
bill_frame.place(x=SCREEN_WIDTH / 2, y=0)

time_update()
window.mainloop()

# Add -> to add the order to table
#
#
# Goto table

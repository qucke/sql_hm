import tkinter as tk
from tkinter import ttk, messagebox

from queries import (
    get_products,
    make_purchase,
    get_report
)


cart = []


class ShopGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Магазин")
        self.root.geometry("900x600")

        self.create_widgets()
        self.load_products()

    def create_widgets(self):

        columns = (
            "ID",
            "Название",
            "Категория",
            "Цена",
            "Склад"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Label(
            control_frame,
            text="Количество"
        ).grid(row=0, column=0)

        self.quantity_entry = tk.Entry(control_frame)
        self.quantity_entry.grid(row=0, column=1)

        tk.Button(
            control_frame,
            text="Добавить",
            command=self.add_to_cart
        ).grid(row=0, column=2)

        tk.Button(
            control_frame,
            text="Купить",
            command=self.buy
        ).grid(row=0, column=3)

        self.cart_list = tk.Listbox(
            self.root,
            height=8
        )

        self.cart_list.pack(fill=tk.BOTH)

        report_frame = tk.Frame(self.root)
        report_frame.pack(pady=10)

        tk.Label(
            report_frame,
            text="Дата YYYY-MM-DD"
        ).grid(row=0, column=0)

        self.report_entry = tk.Entry(report_frame)
        self.report_entry.grid(row=0, column=1)

        tk.Button(
            report_frame,
            text="Отчет",
            command=self.show_report
        ).grid(row=0, column=2)

    def load_products(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = get_products()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_to_cart(self):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected, "values")

        product_id = int(values[0])
        name = values[1]
        price = float(values[3])
        stock = int(values[4])

        quantity = int(self.quantity_entry.get())

        if quantity > stock:
            messagebox.showerror(
                "Ошибка",
                "Недостаточно товара"
            )
            return

        cart.append(
            (product_id, price, quantity)
        )

        self.cart_list.insert(
            tk.END,
            f"{name} x {quantity}"
        )

    def buy(self):

        if not cart:
            return

        check_id, total_sum = make_purchase(cart)

        messagebox.showinfo(
            "Покупка",
            f"Чек №{check_id}\n"
            f"Сумма: {total_sum}"
        )

        cart.clear()
        self.cart_list.delete(0, tk.END)

        self.load_products()

    def show_report(self):

        date_value = self.report_entry.get()

        sales, revenue = get_report(date_value)

        report_window = tk.Toplevel(self.root)
        report_window.title("Отчет")

        text = tk.Text(report_window)
        text.pack(fill=tk.BOTH, expand=True)

        text.insert(tk.END, "Продажи:\n\n")

        for row in sales:
            text.insert(
                tk.END,
                f"{row[0]} : {row[1]} шт.\n"
            )

        text.insert(
            tk.END,
            f"\nВыручка: {revenue}"
        )
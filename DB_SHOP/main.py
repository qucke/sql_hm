import tkinter as tk

from config_db import create_tables
from queries import add_test_data
from gui import ShopGUI


create_tables()
add_test_data()

root = tk.Tk()

app = ShopGUI(root)

root.mainloop()
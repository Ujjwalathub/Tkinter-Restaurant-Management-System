import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

# ----------------------------
# Backend Classes
# ----------------------------

class MenuItem:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} (₹{self.price:.2f})"

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = {}  # item_id: quantity
        self.total_amount = 0.0
        self.is_completed = False

    def add_item(self, menu_item, quantity):
        self.items[menu_item.item_id] = self.items.get(menu_item.item_id, 0) + quantity
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = 0.0
        for item_id, quantity in self.items.items():
            menu_item = restaurant_system.get_menu_item(item_id)
            if menu_item:
                self.total_amount += menu_item.price * quantity

    def complete_order(self):
        self.is_completed = True

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"
        return f"Order {self.order_id} - {status} - ₹{self.total_amount:.2f}"

class RestaurantSystem:
    def __init__(self):
        self.menu = {}
        self.orders = {}
        self.next_item_id = 1
        self.next_order_id = 1

    def add_menu_item(self, name, price):
        item = MenuItem(self.next_item_id, name, price)
        self.menu[self.next_item_id] = item
        self.next_item_id += 1
        return item

    def get_menu(self):
        return list(self.menu.values())

    def get_menu_item(self, item_id):
        return self.menu.get(item_id)

    def create_order(self):
        order = Order(self.next_order_id)
        self.orders[self.next_order_id] = order
        self.next_order_id += 1
        return order

    def get_orders(self):
        return list(self.orders.values())

    def get_order(self, order_id):
        return self.orders.get(order_id)

# Global system
restaurant_system = RestaurantSystem()

# ----------------------------
# GUI Code
# ----------------------------

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")

        self.menu_frame = ttk.LabelFrame(root, text="Menu Management")
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.order_frame = ttk.LabelFrame(root, text="Order Management")
        self.order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.build_menu_section()
        self.build_order_section()

    def build_menu_section(self):
        self.menu_list = tk.Listbox(self.menu_frame, width=40, height=10)
        self.menu_list.grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(self.menu_frame, text="Name:").grid(row=1, column=0)
        self.menu_name_entry = ttk.Entry(self.menu_frame)
        self.menu_name_entry.grid(row=1, column=1)

        ttk.Label(self.menu_frame, text="Price:").grid(row=2, column=0)
        self.menu_price_entry = ttk.Entry(self.menu_frame)
        self.menu_price_entry.grid(row=2, column=1)

        ttk.Button(self.menu_frame, text="Add Item", command=self.add_menu_item).grid(row=3, column=0, columnspan=2, pady=5)

        self.refresh_menu()

    def build_order_section(self):
        self.order_list = tk.Listbox(self.order_frame, width=40, height=10)
        self.order_list.grid(row=0, column=0, columnspan=2)

        ttk.Button(self.order_frame, text="New Order", command=self.create_order).grid(row=1, column=0, pady=5)
        ttk.Button(self.order_frame, text="Add Item to Order", command=self.add_item_to_order).grid(row=1, column=1, pady=5)
        ttk.Button(self.order_frame, text="Complete Order", command=self.complete_order).grid(row=2, column=0, columnspan=2, pady=5)

        self.refresh_orders()

    def refresh_menu(self):
        self.menu_list.delete(0, tk.END)
        for item in restaurant_system.get_menu():
            self.menu_list.insert(tk.END, f"ID {item.item_id}: {item.name} - ₹{item.price:.2f}")

    def refresh_orders(self):
        self.order_list.delete(0, tk.END)
        for order in restaurant_system.get_orders():
            self.order_list.insert(tk.END, str(order))

    def add_menu_item(self):
        name = self.menu_name_entry.get().strip()
        try:
            price = float(self.menu_price_entry.get())
            if price <= 0 or not name:
                raise ValueError
            restaurant_system.add_menu_item(name, price)
            self.menu_name_entry.delete(0, tk.END)
            self.menu_price_entry.delete(0, tk.END)
            self.refresh_menu()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid name and positive price.")

    def create_order(self):
        restaurant_system.create_order()
        self.refresh_orders()

    def add_item_to_order(self):
        if not restaurant_system.orders:
            messagebox.showinfo("No Orders", "Please create an order first.")
            return
        try:
            order_index = self.order_list.curselection()[0]
            order = restaurant_system.get_orders()[order_index]
            menu_index = self.menu_list.curselection()[0]
            menu_item = restaurant_system.get_menu()[menu_index]

            qty = int(tk.simpledialog.askstring("Quantity", f"Enter quantity for {menu_item.name}:"))
            if qty <= 0:
                raise ValueError
            order.add_item(menu_item, qty)
            self.refresh_orders()
        except IndexError:
            messagebox.showerror("Selection Error", "Please select an order and a menu item.")
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Quantity", "Please enter a valid positive integer for quantity.")

    def complete_order(self):
        try:
            order_index = self.order_list.curselection()[0]
            order = restaurant_system.get_orders()[order_index]
            order.complete_order()
            messagebox.showinfo("Order Completed", f"Order {order.order_id} marked as completed.")
            self.refresh_orders()
        except IndexError:
            messagebox.showerror("Selection Error", "Please select an order to complete.")

# ----------------------------
# Start the Application
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()

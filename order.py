from tkinter import messagebox, ttk, Tk, Label, Button, Frame, StringVar, IntVar


def order_page():
    # Main window for placing orders
    root = Tk()
    root.geometry("600x500")
    root.title("Restaurant Order Management")

    # Frame for order placement
    order_frame = Frame(root)
    order_frame.pack(pady=20)

    # Label for instructions
    Label(order_frame, text="Select Menu Item and Place Your Order", font=("Helvetica", 14)).pack(pady=10)

    # Treeview to display menu items
    tree = ttk.Treeview(order_frame, columns=("item_id", "item_name", "price", "available"), show="headings")
    tree.heading("item_id", text="Item ID")
    tree.heading("item_name", text="Item Name")
    tree.heading("price", text="Price")
    tree.heading("available", text="Available")
    tree.pack()

    # Fetch menu items from database and populate Treeview
    def fetch_menu_items():
        cur = con.cursor()
        cur.execute("SELECT item_id, item_name, price, available FROM MenuItems WHERE available = 'Y'")
        items = cur.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for item in items:
            tree.insert('', 'end', values=item)

    fetch_menu_items()

    # Entry fields for customer details
    customer_name_var = StringVar()
    Label(order_frame, text="Customer Name").pack(pady=5)
    customer_name_entry = ttk.Entry(order_frame, textvariable=customer_name_var)
    customer_name_entry.pack()

    quantity_var = IntVar(value=1)
    Label(order_frame, text="Quantity").pack(pady=5)
    quantity_entry = ttk.Entry(order_frame, textvariable=quantity_var)
    quantity_entry.pack()

    # Place order function
    def place_order(con):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a menu item to order.")
            return
        item_values = tree.item(selected_item, 'values')
        item_id = item_values[0]
        item_name = item_values[1]
        price = item_values[2]
        quantity = quantity_var.get()
        customer_name = customer_name_var.get()

        if not customer_name:
            messagebox.showwarning("Input Error", "Please enter the customer name.")
            return

        # Insert order into database
        try:
            cur = con.cursor()
            # Insert customer if not exists
            cur.execute("INSERT INTO Customer (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=VALUES(name)", (customer_name,))
            con.commit()

            # Get customer ID
            cur.execute("SELECT customer_id FROM Customer WHERE name = %s", (customer_name,))
            customer_id = cur.fetchone()[0]

            # Insert order
            cur.execute("INSERT INTO Orders (customer_id, total_amount) VALUES (%s, %s)", (customer_id, price * quantity))
            con.commit()

            # Get last order ID
            cur.execute("SELECT LAST_INSERT_ID()")
            order_id = cur.fetchone()[0]

            # Insert order item
            cur.execute("INSERT INTO OrderItems (order_id, item_id, quantity) VALUES (%s, %s, %s)", (order_id, item_id, quantity))
            con.commit()

            messagebox.showinfo("Success", f"Order placed for {quantity} x {item_name} by {customer_name}.")
            customer_name_entry.delete(0, 'end')
            quantity_var.set(1)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Button to place order
    Button(order_frame, text="Place Order", command=place_order).pack(pady=20)

    root.mainloop()
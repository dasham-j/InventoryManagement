import customtkinter as ctk
import pandas as pd
import os
from tkinter import ttk
import tkinter.messagebox as messagebox

# CSV file path

def load_bill_call():
    CSV_FILE = 'bill.csv'

    # Create the CSV file if it doesn't exist
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Item ID', 'Item Name', 'Quantity', 'Price'])
        df.to_csv(CSV_FILE, index=False)

    # Load the inventory data
    def load_inventory_data():
        return pd.read_csv(CSV_FILE)

    # Save the inventory data
    def save_inventory_data(df):
        df.to_csv(CSV_FILE, index=False)

    # Add an item to the bill
    def add_to_bill():
        item_id = entry_id.get()
        item_name = entry_name.get()
        quantity = entry_quantity.get()
        price = entry_price.get()

        if not item_id or not item_name or not quantity or not price:
            messagebox.showinfo("Input Error", "All fields are required")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be an integer and price must be a float")
            return

        # Insert into treeview for the bill
        total_price = quantity * price
        tree.insert("", "end", values=(item_id, item_name, quantity, price, total_price))
        update_total_bill()

        clear_fields()

    # Calculate and update the total bill
    def update_total_bill():
        total = 0
        for child in tree.get_children():
            total += float(tree.item(child, 'values')[4])
       

    # Reset the bill
    def reset_bill():
        for row in tree.get_children():
            tree.delete(row)
        update_total_bill()

    def clear_fields():
        entry_id.delete(0, ctk.END)
        entry_quantity.delete(0, ctk.END)
        entry_name.delete(0, ctk.END)
        entry_price.delete(0, ctk.END)

    # Print bill (simulated here)
    def print_bill():
        bill_details = []
        for child in tree.get_children():
            item = tree.item(child)['values']
            bill_details.append(item)
        
        # This is where you would implement actual print functionality or save as PDF, etc.
        messagebox.showinfo("Print Bill", f"Bill details: {bill_details}")
    global content_frame
    
    
    # Destroy the current content_frame
    content_frame.destroy()
    
    # Create a new content frame for bill_call.py contents
    content_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    frame_form_and_buttons = ctk.CTkFrame(content_frame, corner_radius=10)
    frame_form_and_buttons.pack(fill="x", padx=10, pady=10)

    # Create the form frame on the left
    frame_form = ctk.CTkFrame(frame_form_and_buttons, corner_radius=10)
    frame_form.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Create the buttons frame on the right with 15% width
    frame_buttons = ctk.CTkFrame(frame_form_and_buttons, corner_radius=10)
    frame_buttons.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Configure grid to make the form frame take 85% of the width and the buttons frame 15%
    frame_form_and_buttons.grid_columnconfigure(0, weight=8)  # Adjust the weight for correct distribution
    frame_form_and_buttons.grid_columnconfigure(0, weight=2)

    # Configure grid layout for frame_form
    frame_form.grid_columnconfigure(0, weight=1)  # Label column
    frame_form.grid_columnconfigure(1, weight=2)  # Entry column (adjust weight as needed)

    font_settings = "Arial", 17, "bold"
    ent_height = 35

    # Create input fields in the form frame
    ctk.CTkLabel(frame_form, text="Item ID:", font=font_settings).grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_id = ctk.CTkEntry(frame_form, font=font_settings, height=ent_height)
    entry_id.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(frame_form, text="Item Name:", font=font_settings).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_name = ctk.CTkEntry(frame_form, font=font_settings, height=ent_height)
    entry_name.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(frame_form, text="Quantity:", font=font_settings).grid(row=2, column=0, sticky="w", padx=10, pady=10)
    entry_quantity = ctk.CTkEntry(frame_form, font=font_settings, height=ent_height)
    entry_quantity.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(frame_form, text="Price:", font=font_settings).grid(row=3, column=0, sticky="w", padx=10, pady=10)
    entry_price = ctk.CTkEntry(frame_form, font=font_settings, height=ent_height)
    entry_price.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

    button_height = 70

    # Add buttons to the buttons frame and stack them vertically with larger size
    ctk.CTkButton(frame_buttons, text="Add to Bill", font=font_settings, command=add_to_bill, height=button_height).grid(row=0, column=1, padx=7, pady=15, sticky="ew")
    ctk.CTkButton(frame_buttons, text="Reset Bill", font=font_settings, command=reset_bill, height=button_height).grid(row=1, column=1, padx=7, pady=15, sticky="ew")
    ctk.CTkButton(frame_buttons, text="Print Bill", font=font_settings, command=print_bill, height=button_height).grid(row=0, column=0, padx=7, pady=15, sticky="ew")

    # Create a treeview for displaying the bill
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#356aa1", foreground="white", font=("Arial", 17, "bold"))
    s.configure('Treeview', font=("Arial", 16, "bold"), rowheight=30)
    tree_frame = ctk.CTkFrame(content_frame, corner_radius=10)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=("Item ID", "Item Name", "Quantity", "Price", "Total"), show="headings", style="Treeview", height=15)
    tree.heading("Item ID", text="Item ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Total", text="Total")
    tree.pack(fill="both", expand=True)

def load_inventory():
    CSV_FILE = 'inventory.csv'

    # Create the CSV file if it doesn't exist
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Item ID', 'Item Name', 'Quantity'])
        df.to_csv(CSV_FILE, index=False)

    # Load the inventory data
    def load_data():
        return pd.read_csv(CSV_FILE)

    # Save the inventory data
    def save_data(df):
        df.to_csv(CSV_FILE, index=False)

    def validation():
        item_id = str(entry_id.get()).upper()
        item_name = str(entry_name.get()).upper()
        quantity = entry_quantity.get().upper()
        

        if not item_name or not quantity :
            messagebox.showinfo("Input Error", "Enter Item Name And Quantity")
            return False
        if not item_id:
            item_id=" "
        if item_id.isdigit():
            item_id=int(item_id)
            
        
            
        
        if not quantity.isdigit():
            messagebox.showinfo("Input Error","Avoid using alphabets or symbols in quantity section")
            return False
        
        if not item_name.isalpha():
            messagebox.showinfo("Input Error", "Plz Avoid Using Numbers or Symbols In  Item Name Section")
            return False
        
        return item_id,item_name,quantity

    def validation_del():
        item_id = str(entry_id.get()).upper()
        item_name = str(entry_name.get()).upper()
        
        if not item_id:
            item_id=" "
            if not item_name:
                messagebox.showinfo("Input Error", "Enter Item Name or Id to Delete the Data")
                return False
            
            
            
            if not item_name.isalpha():
                messagebox.showinfo("Input Error", "Plz Avoid Using Numbers or Symbols In  Item Name Section")
                return False
            
            return item_name,1,str(item_id)
        else: 
            if not item_name:
                messagebox.showinfo("Input Error", "Enter Item Name Please")
                return False
            
            
            
            return item_id,0,item_name

    # Add a new item to the inventory
    def add_item():
        item = validation()
        if item:
            df = load_data()
            
            exists = not df[(df['Item ID'] == str(item[0])) & (df['Item Name'] == item[1])].empty

            if exists:
                if(item[0]==" "):
                    messagebox.showinfo("Input Error", "Item with this Name already exists")
                else:   
                    messagebox.showinfo("Input Error", "Item with this ID already exists")
            else:    
                new_row = pd.DataFrame([{'Item ID': item[0], 'Item Name': item[1], 'Quantity': item[2]}])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                load_table()

    # Delete an item from the inventory
    def delete_item():
        item = validation_del()
        if item:
            delt=False
            if item[1]==0:
                df = load_data()
                
                
                if (not df[(df['Item Name'] == item[2]) & (df['Item ID'] == str(item[0]))].empty):
                    delt=True
                df=df.drop(df[(df['Item ID'] == str(item[0])) & (df['Item Name'] == item[2])].index)
                save_data(df)
                load_table()
                
                
            elif item[1]==1:
                df = load_data()
                if (not df[(df['Item Name'] == item[0]) & (df['Item ID'] == str(item[2]))].empty):
                    delt=True
                df=df.drop(df[(df['Item Name'] == str(item[0])) & (df['Item ID'] == str(item[2]))].index)
                save_data(df)
                load_table()
                
            if not delt:        
                messagebox.showinfo("Selection Error", "item not found")
        
    # Update an item in the inventory
    def update_item():
        
        item=validation()
        
        
        df = load_data()
        exists = not df[(df['Item Name'] == item[1]) & (df['Item ID'] == str(item[0]))].empty
        df.loc[(df['Item ID'] == str(item[0])) & (df['Item Name'] == item[1]), ['Quantity']] = [item[2]]
        save_data(df)
        load_table()
        if not exists:
            messagebox.showinfo("Selection Error", "item not found")
            
    def clear_fields():
        entry_id.delete(0, ctk.END)
        entry_quantity.delete(0, ctk.END)
        entry_name.delete(0, ctk.END)
        entry_price.delete(0, ctk.END)

        

    # Load the data into the table
    def load_table():
        for row in tree.get_children():
            tree.delete(row)

        df = load_data()
        for index, row in df.iterrows():
            tree.insert("", "end", values=(row['Item ID'], row['Item Name'], row['Quantity']))
    global content_frame
    
    
    # Destroy the current content_frame
    content_frame.destroy()
    # Create the main content frame
    content_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Create a frame to hold both form and buttons
    frame_form_and_buttons = ctk.CTkFrame(content_frame, corner_radius=10)
    frame_form_and_buttons.pack(fill="x", padx=10, pady=10)

    # Create the form frame on the left
    frame_form = ctk.CTkFrame(frame_form_and_buttons, corner_radius=10)
    frame_form.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Create the buttons frame on the right with 15% width
    frame_buttons = ctk.CTkFrame(frame_form_and_buttons, corner_radius=10)
    frame_buttons.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Configure grid to make the form frame take 85% of the width and the buttons frame 15%
    frame_form_and_buttons.grid_columnconfigure(0, weight=50)
    frame_form_and_buttons.grid_columnconfigure(0, weight=20)

    # Configure grid layout for frame_form
    frame_form.grid_columnconfigure(0, weight=1)  # Label column
    frame_form.grid_columnconfigure(0, weight=2)  # Entry column (adjust weight as needed)

    font_settings="Arial",17,"bold"
    ent_height=35
    # Create input fields in the form frame
    ctk.CTkLabel(frame_form, text="Item ID:",font=font_settings).grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_id = ctk.CTkEntry(frame_form,font=font_settings,height=ent_height)
    entry_id.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(frame_form, text="Item Name:",font=font_settings).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_name = ctk.CTkEntry(frame_form,font=font_settings,height=ent_height)
    entry_name.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(frame_form, text="Quantity:",font=font_settings).grid(row=2, column=0, sticky="w", padx=10, pady=10)
    entry_quantity = ctk.CTkEntry(frame_form,font=font_settings,height=ent_height)
    entry_quantity.grid(row=2, column=1, padx=20, pady=5, sticky="ew")


    button_height = 70

    # Add buttons to the buttons frame and stack them vertically with larger size
    ctk.CTkButton(frame_buttons, text="Add Item",font=font_settings, command=add_item,height=button_height).grid(row=0, column=1, padx=7, pady=15, sticky="ew")
    ctk.CTkButton(frame_buttons, text="Delete Item",font=font_settings, command=delete_item,height=button_height).grid(row=1, column=1, padx=7,pady=15, sticky="ew")
    ctk.CTkButton(frame_buttons, text="Update Item",font=font_settings,command=update_item,height=button_height).grid(row=0, column=0,padx=7 , pady=15, sticky="ew")
    ctk.CTkButton(frame_buttons, text="Clear",font=font_settings, command=clear_fields,height=button_height).grid(row=1, column=0,padx=7, pady=15, sticky="ew")

    # Create a treeview for displaying the inventory
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#356aa1",foreground="white",font=("Arial",17,"bold"))
    s.configure('Treeview', font=("Arial", 16,"bold"), rowheight=30)
    tree_frame = ctk.CTkFrame(content_frame, corner_radius=10)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(tree_frame, columns=("Item ID", "Item Name", "Quantity"), show="headings", style="Treeview",height=15)

    tree.heading("Item ID", text="Item ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")

    tree.pack(fill="both", expand=True)

    # Load the initial data
    load_table()
    
# Create the main window
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Inventory Management System")
root.geometry("1024x600")
root.minsize(1024, 600)
s = ttk.Style()
button_height = 70

font_settings2="Arial",20,"bold"
# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True)

# Create the navigation bar frame
nav_frame = ctk.CTkFrame(main_frame, width=160, corner_radius=10, fg_color="#333")
nav_frame.pack(side="left", fill="y", padx=10, pady=10)

# Configure grid layout for nav_frame
nav_frame.grid_rowconfigure((0, 1, 2), weight=1)
nav_frame.grid_columnconfigure(0, weight=1)

# Navigation bar buttons

ctk.CTkButton(nav_frame, text="STOCK",font=font_settings2 , corner_radius=10,height=170,command=load_inventory).grid(row=0, column=0, padx=10, pady=2, sticky="ew")
ctk.CTkButton(nav_frame, text="BILL",font=font_settings2, corner_radius=10,height=170,command=load_bill_call).grid(row=1, column=0, padx=10, pady=2, sticky="ew")
ctk.CTkButton(nav_frame, text="STOCK",font=font_settings2, corner_radius=10,height=170).grid(row=2, column=0, padx=10, pady=2, sticky="ew")

content_frame = ctk.CTkFrame(main_frame, corner_radius=10)
content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Run the application
root.mainloop()


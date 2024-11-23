import customtkinter as ctk
import pandas as pd
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
tam=0
import time
import keyboard
from datetime import datetime
from CTkScrollableDropdown import *  

# Get the current date and time
now = datetime.now()
# CSV file path for inventory
CSV_FILE = 'inventory.csv'
CSV_FILE2 = 'History.csv'
num=['1','2','3','4','5','6','7','8','9','0']

# Create the CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    messagebox.showinfo("Input Error", "No data Found")
    
if not os.path.exists(CSV_FILE2):
    df = pd.DataFrame(columns=['Date','Bill Id','Customer Name','Phone Number','Item Id', 'Item Name', 'Quantity', 'Price','Total Price of Item','Total Amt. To Pay','Amt. Received','Pending Amt.'])
    df.to_csv(CSV_FILE2, index=False)
    
# Load the inventory data
def load_inventory_data():
    return pd.read_csv(CSV_FILE)

def update_tree(*args):
    # Clear the Treeview if there's an existing item
    for item in summary_treeview.get_children():
        summary_treeview.delete(item)
    current_columns2 = list(summary_treeview["columns"])
    
    if len(args)<2:
        summary_treeview.insert("", "end", values=(args[0]))
        
    else:
        summary_treeview.insert("", "end", values=(args[0],args[1],args[2]))
    


def save_inventory_data(df):
    df.to_csv(CSV_FILE, index=False)

# Add an item to the bill
def add_to_bill():
    flag=0
    item_id = combo_id.get().upper().replace(" ","")
    item_name = entry_name.get().upper().replace(" ","")
    quantity = entry_quantity.get()
    price = entry_price.get()
    

    if not item_id or not item_name or not quantity or not price:
        messagebox.showinfo("Input Error", "Fill all the fields properly")
        return

    try:
        price = float(price)
        valp.configure(text="")
        flag=1
    except ValueError:
        entry_price.delete(0, ctk.END)
        valp.configure(text="Please input numeric \nvalues only.", text_color="red")

    for i in price,quantity:
        if i==" ":
            i=''
    
    if flag==1:
        global tam
        
        fl=update_item(tam)
        tam=fl[1]
        
        if fl[0] == 0:
            total_price = int(quantity) * price
            tam=tam+total_price
            add_row_to_treeview(item_id, item_name, quantity, price, total_price)
            clear_fields()
        update_tree(f"₹{tam:.2f}")
        
        
        
    else:
        pass

# Add a row to the treeview
def add_row_to_treeview(item_id, item_name, quantity, price, total_price):
    
    treeview.insert("", "end", values=(item_id, item_name, quantity, f"₹{price:.2f}", f"₹{total_price:.2f}"))

        
    

# Calculate and update the total bill
def print_bill():
    current_columns = list(treeview["columns"])
    
    if not current_columns[0]=='Item ID':
        messagebox.showinfo("Input Error", "Unable to print: A bill is already open.")
    else:    
        if not treeview.get_children():
            messagebox.showinfo("Input Error", "There are no items to add to the bill.")
         
        else:
            dt = datetime.now()
            dt = str(dt.strftime("%Y-%m-%d %H:%M"))
            year = str(now.year)[-2:]
            month = f"{now.month:02}"
            dialog = ctk.CTkToplevel(root)
            dialog.title("Enter Details")
            dialog.geometry("350x170")
            dialog.resizable(False, False)
            dialog.attributes("-topmost", True)
            dialog.attributes("-type", "splash")
            
            dialog.grab_set()  # Prevents interaction with the main window until dialog is closed
            window_width = 350
            window_height = 180
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = (screen_width // 3) - (window_width // 3)
            y = (screen_height // 4) - (window_height // 4)
            dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")


            # Label
            label = ctk.CTkLabel(dialog, text="Name:",font=font_settings)
            label.grid(pady=(15,5),row=0,column=0,padx=(20,2))

            # Entry widget
            input_var = ctk.StringVar()
            entry = ctk.CTkEntry(dialog, textvariable=input_var, width=200,font=font_settings)
            entry.grid(pady=(15,5),row=0,column=1,padx=15)
            
            label = ctk.CTkLabel(dialog, text="Number:",font=font_settings)
            label.grid(pady=(5,5),row=1,column=0,padx=(20,2))

            # Entry widget
            input_var2 = ctk.StringVar()
            entry1 = ctk.CTkEntry(dialog, textvariable=input_var2, width=200,font=font_settings)
            
            entry1.grid(pady=(5,5),row=1,column=1,padx=15)
            
            label = ctk.CTkLabel(dialog, text="Amt. Paid:",font=font_settings)
            label.grid(pady=(5,5),row=2,column=0,padx=(20,2))
            input_var3 = ctk.StringVar()
            entry2 = ctk.CTkEntry(dialog, textvariable=input_var3, width=200,font=font_settings)
            
            entry2.grid(pady=(5,2),row=2,column=1,padx=15)
            def submit():
                name=entry.get().lower()
                number=entry1.get()
                amt=entry2.get()
                try:
                    num=int(number)
                    amt=float(amt)
                    if len(number)!=10:
                        messagebox.showinfo("Input Error", "Incomplete number. Please provide a valid, complete number.")
                    else:
                        df = pd.read_csv(CSV_FILE2)
                        dfi = pd.read_csv(CSV_FILE)
                        if df.empty:
                            bid="KTM"+year+month+"00"
                        else:
                            
                            num=int((df.iloc[-2, 1])[7:])
                            
                            bid = f"KTM{year}{month}{num + 1:02}"
                        rem_amt=tam-amt
                        # Collect all rows from the Treeview
                        all_rows = []
                        for item in treeview.get_children():
                            row = treeview.item(item)["values"]
                            new_row = {
                                'Date': dt,
                                'Bill Id': bid,
                                'Customer Name': name,
                                'Phone Number': number,
                                'Item Id': row[0],
                                'Item Name': row[1],
                                'Quantity': row[2],
                                'Price': row[3],
                                'Total Price of Item': row[4],
                                'Total Amt. To Pay': f"₹{tam:.2f}",
                                'Amt. Received': f"₹{amt:.2f}",
                                'Pending Amt.': f"₹{rem_amt:.2f}"
                            }
                            all_rows.append(new_row)
                            qt = dfi.loc[(dfi['Item Name'].str.upper() == row[1].upper()) & (dfi['Item ID'].str.upper() == row[0].upper()), 'Quantity'].values[0]
                            qt=int(qt)-int(row[2])
                            dfi.loc[(dfi['Item Name'].str.upper() == row[1].upper()) & (dfi['Item ID'].str.upper() == row[0].upper()), ['Quantity']] = [qt]
                            save_inventory_data(dfi)
                        new_df = pd.DataFrame(all_rows)
                        df = pd.concat([df, new_df])

                       
                        df.to_csv(CSV_FILE2, index=False, encoding='utf-8-sig')
                        
                        empty_row = pd.DataFrame([[""] * len(df.columns)], columns=df.columns)
                        empty_row.to_csv(CSV_FILE2, mode='a', header=False, index=False)
                        dialog.destroy()
                        reset_bill() 
                except:
                    messagebox.showinfo("Input Error", "Please enter valid numeric values only in the number and amount sections.")
            ctk.CTkButton(dialog, text="Confirm", font=font_settings, command=submit,width=100).grid(row=3, column=1, padx=(3,5), pady=8)
        
# Reset the bill
def reset_bill():
    columns = ("Item ID","Item Name","Quantity","Price","Total")
    columns2=("Amount")
    current_columns = list(treeview["columns"])
    current_columns2 = list(summary_treeview["columns"])
    if not current_columns[0]=='Item ID':
        response = messagebox.askyesno("Confirmation", f"Do you want to reset the bill? This will erase all unsaved data.")
        if response:
            for row in treeview.get_children():
                treeview.delete(row)
            treeview.configure(columns=columns)
            for col in columns:
                treeview.heading(col, text=col)
            
                
            for row in summary_treeview.get_children():
                summary_treeview.delete(row)
            
            
            summary_treeview.configure(columns=columns2)    
               
            
            
            treeview.column("Item ID", anchor="center", width=80, stretch=True)
            treeview.column("Item Name", anchor="center", width=100, stretch=True)
            treeview.column("Quantity", anchor="center", width=100, stretch=True)
            treeview.column("Price", anchor="center", width=100, stretch=True)
            treeview.column("Total", anchor="center", width=100, stretch=True)
            
            summary_treeview.heading("Amount", text="Total Amount")
            
            
            summary_treeview.column("Amount", anchor="center", width=120, stretch=True)
            
        
    else:    
        for row in treeview.get_children():
            treeview.delete(row)
        global tam
        tam=0
        for row in summary_treeview.get_children():
            summary_treeview.delete(row)    
    

# Clear input fields
def clear_fields():
    d=load()
    
    cid=combo_id.get()
    nm=entry_name.get()
 
    combo_id._entry.delete(0, "end")
    entry_name._entry.delete(0, "end")
    entry_quantity.delete(0, ctk.END)
    entry_price.delete(0, ctk.END)
    valn.configure(text="Enter valid \nItem Name", text_color="gray")
    valn.grid_configure(padx=(0,20))
    val.configure(text="Enter ID", text_color="gray")
    val.grid_configure(padx=(0, 35))
    valq.configure(text="")
    item_ids = d[0].tolist()
    
    update_combobox(item_ids)

def update_item(tam):
    flag = 0
    item_id = combo_id.get().upper().replace(" ","")
    
    quantity = entry_quantity.get()
    price = entry_price.get()
    column_0_values = []
    for item in treeview.get_children():  # Get all row IDs
         if str(item_id) == (treeview.item(item)["values"][0]):
             flag = 1
             response = messagebox.askyesno("Confirmation", f"do you want to update the price or quantity of {item_id}?")
             if response:
                 v = list(treeview.item(item)["values"])  
                 v[2] = str(quantity)  
                 v[3] = f"₹{float(price):.2f}"
                 total_price = int(quantity) * int(price)
                 
                 tam=int(tam)-int(float(v[4].replace("₹", "")))+total_price
                 
                 v[4] = f"₹{float(total_price):.2f}"
                 
                 
                 treeview.item(item, values=v)
                 
             else:
                 pass
    return flag,tam

def update_qt_n_price():
    d=load()
    flag=0
    item_id = combo_id.get().upper().replace(" ","")
    item_name = entry_name.get().upper().replace(" ","")
    qty = entry_quantity.get()
    price = entry_price.get()
    if not item_id=="" and not item_name=="" and not qty=="" and not price=="" :
        if not treeview.get_children():
            messagebox.showinfo("Input Error", "No Item Added To Bill")
            
        else:
            for item in treeview.get_children():  # Get all row IDs
                 if str(item_id) == (treeview.item(item)["values"][0]):
                     flag=1
                 
            if flag==1:
                add_to_bill()
                clear_fields()
            else:
                messagebox.showinfo("Input Error", "No data available to update for the specified Item ID.")

    else:
        messagebox.showinfo("Input Error", "Fill all the fields properly")
        
    
    
        
        
    

def load():
    df = load_inventory_data()
    return df['Item ID'].astype(str),df['Item Name'].astype(str),df
d=load()
def update_combobox(items):
    """ Function to update the combo box values dynamically. """
    combo_id.configure(values=items)
    
def update_comboboxn(items):
    """ Function to update the combo box values dynamically. """
    entry_name.configure(values=items)
def quantity_check():
    
    d=load()
    df=d[2]
    qt = df.loc[(df['Item Name'].str.upper() == entry_name.get().upper().replace(" ","")) & 
                    (df['Item ID'].str.upper() == combo_id.get().upper().replace(" ","")), 'Quantity'].values[0]
    
    if qt==0:
        valq.grid_configure(padx=(0,15))
        valq.configure(text="Out Of Stock", text_color="red")
        entry_quantity.configure(state="disabled")
        entry_price.configure(state="disabled")
        return False
    else:
        valq.configure(text="Avl. Quanity: "+ str(qt), text_color="green")
        valq.grid_configure(padx=(0,15))
        return qt
    
def validate_input(box,validip,element,ename):
    
    
    d=load()
    df=d[2]
    if ename=="valn" and combo_id.get()=="":
        combo_id.set(' ')
        val.configure(text="")
        
    if box in validip.str.upper().tolist():
        
        if ename=="val":
            itnm = not df.loc[(df['Item Name'].str.upper() == entry_name.get().upper().replace(" ","")) & (df['Item ID'].str.upper() == combo_id.get().upper().replace(" ",""))].empty
            if itnm:
                entry_quantity.configure(state="normal")
                element.configure(text="Valid ID", text_color="green")
                element.grid_configure(padx=(0, 35))
                quantity_check()
            element.configure(text="Valid ID", text_color="green")
            element.grid_configure(padx=(0, 35))
            
            
        if ename=="valn":
            
            itn = not df.loc[(df['Item Name'].str.upper() == entry_name.get().upper().replace(" ","")) & (df['Item ID'].str.upper() == combo_id.get().upper().replace(" ",""))].empty
            
            if itn:
                
                entry_quantity.configure(state="normal")
                element.configure(text="Valid Name", text_color="green")
                element.grid_configure(padx=(0, 23))
                qc=quantity_check()
                return qc
            element.configure(text="Valid Name", text_color="green")
            element.grid_configure(padx=(0, 35))    
                
            
            
        
    else:
        element.configure(text="Invalid", text_color="red")
        element.grid_configure(padx=(0,35))

def search(var):
    entry_quantity.delete(0, ctk.END)
    entry_price.delete(0, ctk.END)
    valq.configure(text="")
    search_value = combo_id.get().upper()
    search_value=search_value.replace(" ","")
        
    if search_value == "":
        # Show all item IDs if search is empty
        item_ids = d[0].tolist()
        val.configure(text="Enter ID", text_color="gray")
        val.grid_configure(padx=(0, 35))
        
    else:
        # Filter item IDs based on the search value
        item_ids = d[0].tolist()
        item_ids = [item_id for item_id in item_ids if search_value in item_id.upper()]
        
        validate_input(search_value.upper(),d[0],val,"val")
        
        
    # Update the combo box with filtered results
    
    update_combobox(item_ids)
def add_column_to_start():
    
    current_columns = list(treeview["columns"])
    current_columns2 = list(summary_treeview["columns"])
    if not current_columns[0]=='Bill ID':
        billcol = "Bill ID"
        cname="Customer Name"
        
        
        updated_columns = [billcol]+[cname] + current_columns
        treeview["columns"] = updated_columns
             
    else:
        pass
    
    if len(current_columns2)<2:
        amrcv = "Amt. Received"
        pmt="Pending Amt."
        
        
        updated_columns2 = current_columns2+[amrcv]+[pmt] 
        summary_treeview["columns"] = updated_columns2
        
    
    
        
    
    treeview.heading("Bill ID", text="Bill ID")
    treeview.heading("Customer Name", text="Customer Name")
    treeview.heading("Item ID", text="Item ID")
    treeview.heading("Item Name", text="Item Name")
    treeview.heading("Quantity", text="Quantity")
    treeview.heading("Price", text="Price")
    treeview.heading("Total", text="Total")
    treeview.column("Bill ID", anchor="center", width=100, stretch=True)
    treeview.column("Customer Name", anchor="center", width=150, stretch=True)
    treeview.column("Item ID", anchor="center", width=80, stretch=True)
    treeview.column("Item Name", anchor="center", width=100, stretch=True)
    treeview.column("Quantity", anchor="center", width=100, stretch=True)
    treeview.column("Price", anchor="center", width=100, stretch=True)
    treeview.column("Total", anchor="center", width=100, stretch=True)
    
    summary_treeview.heading("Amount", text="Total Amount")
    summary_treeview.heading("Amt. Received", text="Amt. Received")
    summary_treeview.heading("Pending Amt.", text="Pending Amt.")
    
    summary_treeview.column("Amount", anchor="center", width=100, stretch=True)
    summary_treeview.column("Amt. Received", anchor="center", width=100, stretch=True)
    summary_treeview.column("Pending Amt.", anchor="center", width=100, stretch=True)
    
def searchn(var):
    entry_quantity.delete(0, ctk.END)
    entry_price.delete(0, ctk.END)
    valq.configure(text="")
    search_value = entry_name.get().upper()
    search_value=search_value.replace(" ","")
    
    if search_value == "":
        # Show all item IDs if search is empty
        item_ns = d[1].tolist()
        valn.configure(text="Enter valid \nItem Name", text_color="gray")
        valn.grid_configure(padx=(0,20))
    else:
        # Filter item IDs based on the search value
        item_ns = d[1].tolist()
        item_ns = [item_n for item_n in item_ns if search_value in item_n.upper()]
        validate_input(search_value.upper(),d[1],valn,"valn")
    # Update the combo box with filtered results
        
    update_comboboxn(item_ns)
    
def on_item_selected(var):
    """ Function triggered when an item is selected in the combo box. """
    selected_item = combo_id.get()
    selected_item=selected_item.replace(" ","")
    df=d[2]
    
    validate_input(selected_item.upper(),d[0],val,"val")
    # Fetch corresponding item details (for example, Item Name)
    selected_item_info = df[df['Item ID']  == selected_item]['Item Name'].values
    entry_name.set(selected_item_info[0])
    entry_quantity.delete(0, ctk.END)
    entry_price.delete(0, ctk.END)
    validate_input(entry_name.get().upper(),d[1],valn,"valn")
def on_item_selectedn(var):
    """ Function triggered when an item is selected in the combo box. """
    selected_item = entry_name.get()
    selected_item=selected_item.replace(" ","")
    df=d[2]
    validate_input(selected_item.upper(),d[1],valn,"valn")
    entry_quantity.delete(0, ctk.END)
    
    selected_item_info = df[df['Item Name']  == selected_item]['Item ID'].values
    combo_id.set(selected_item_info[0])
    entry_quantity.delete(0, ctk.END)
    entry_price.delete(0, ctk.END)
    validate_input(selected_item.upper(),d[1],valn,"valn")
    

def open_bill():
    
    df=pd.read_csv(CSV_FILE2)
    iterate=df['Bill Id'].astype(str)
    iterate1=df['Customer Name'].astype(str)
    iterate2=df['Date'].astype(str)
    values=[]
    bids=[]
    for i in range(len(iterate)):
        if iterate[i]=="nan":
            vl=f"{iterate2[i-1]} : {iterate1[i-1].upper()}"
            bids.append(iterate[i-1])
            values.append(vl)
           
    def populate_items(frame, query=""):
        for widget in frame.winfo_children():
            widget.destroy()
    
        # Filter values
        filtered_values = [v for v in values if query.lower() in v.lower()]
        
        # Check if no items match
        if not filtered_values:
            ctk.CTkLabel(frame, text="No items found", anchor="center").pack(
                pady=5, fill="x"
            )
        else:
            
            for value in filtered_values:
                ctk.CTkButton(frame, text=value,anchor="w",font=font_settings2,fg_color="#2b2b2b",hover_color="#206aa4",command=lambda v=value: select_value(v)).pack(
                    pady=2, fill="x"
                )
    dropd = ctk.CTkToplevel(root)
    
    dropd.title("SELECT BILL")
     
    
    dropd.resizable(False, False)
    dropd.attributes("-topmost", True)
    dropd.attributes("-type", "splash")
    
    dropd.grab_set()  
    window_width = 400
    window_height = 200
    screen_width = dropd.winfo_screenwidth()
    screen_height = dropd.winfo_screenheight()
    x = (screen_width // 3) - (window_width // 3)
    y = (screen_height // 4) - (window_height // 4)
    dropd.geometry(f"{window_width}x{window_height}+{x}+{y}")
    search_var = ctk.StringVar(value="Search By Name or Date")
    # Search entry
    def clear_default_text(event):
        if search_var.get() == "Search By Name or Date":
            search_var.set("")
    entry = ctk.CTkEntry(dropd, textvariable=search_var,width=330,font=font_settings2)
    entry.pack(pady=10, padx=10)
    entry.bind("<FocusIn>", clear_default_text)      
    # Scrollable frame
    frame = ctk.CTkScrollableFrame(dropd, width=300, height=90)
    frame.pack(pady=5, padx=10)

    # Bind search bar to filter items
    search_var.trace_add("write", lambda *args: populate_items(frame, search_var.get()))
    populate_items(frame)
    
    def select_value(value):
        all_rows = []
        selected_value.set(value)
        value[19:]
        count=0
        for i in range(len(values)):
            if str(values[i])==str(value):
                bid=bids[i]
                response = messagebox.askyesno("Confirmation", f'Do you want to open the Bill with Bill Id "{bids[i]}" and Customer Name: {value[19:]}?')
                if response:
                    for item in treeview.get_children():
                        treeview.delete(item)
                    add_column_to_start()    
                    for i, row in df.iterrows():
                        if row['Bill Id']==bid:
                            ttam=row['Total Amt. To Pay']
                            amrcv=row['Amt. Received']
                            pmt=row['Pending Amt.']
                            if count == 0:
                                treeview.insert("", "end",values=(bid,row['Customer Name'].upper(),row['Item Id'], row['Item Name'], int(row['Quantity']), row['Price'], row['Total Price of Item']))
                                
                                count+=1
                                
                            else:
                                
                                treeview.insert("", "end",values=(" "," ",row['Item Id'], row['Item Name'], int(row['Quantity']), row['Price'], row['Total Price of Item']))
                            
                            
                            update_tree(ttam,amrcv,pmt)
                    dropd.destroy()      
                else:
                    pass
                            
    selected_value = ctk.StringVar(value="Select Item")
    
    
def qt_check(var):
    if combo_id.get().upper()=="" or entry_name.get().upper()=="" :
        valq.configure(text="Please Enter the Item \nName and Item ID first.", text_color="red")
        entry_quantity.delete(0, ctk.END)
        entry_price.delete(0, ctk.END)
        entry_price.configure(state="disabled")
        
    
    else:
        qt=validate_input(entry_name.get().upper().replace(" ",""),d[1],valn,"valn")
        
        if qt:
            qti=entry_quantity.get()
            entry_price.configure(state="normal")
            try:
                for i,x in enumerate(qti):
                    if x == " ":
                        qti.insert(i,'')
                        
                if qti=='':
                    pass
                    
                else:
                    qti=int(qti)
                    if (qt-qti)<0:
                        valq.configure(text="Insufficient Stock: "+ str(qt), text_color="red")
                        entry_price.delete(0, ctk.END)
                        entry_price.configure(state="disabled")
                        
            except:
                entry_quantity.delete(0, ctk.END)
                valq.configure(text="Please input numeric \nvalues only.", text_color="red")
                entry_price.delete(0, ctk.END)
                entry_price.configure(state="disabled")
            
        
        else:
            entry_quantity.delete(0, ctk.END)
            valq.configure(text="Item ID does not \nmatch the Name.", text_color="red")
            entry_price.delete(0, ctk.END)
            entry_price.configure(state="disabled")
        
# Create the main window
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Bill Calculator")
root.geometry("1024x600")
root.minsize(800, 400)

# Decreased font size
font_settings = ("Arial", 17, "bold")
font_settings2 = ("Arial", 15, "bold")
# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True)

# Create the navigation bar frame
nav_frame = ctk.CTkFrame(main_frame, width=160, corner_radius=10, fg_color="#333")
nav_frame.pack(side="left", fill="y", padx=10, pady=10)

# Navigation bar buttons with smaller height
ctk.CTkButton(nav_frame, text="STOCK", font=font_settings, corner_radius=10, height=120).pack(padx=10, pady=2, fill="x")
ctk.CTkButton(nav_frame, text="BILL", font=font_settings, corner_radius=10, height=120).pack(padx=10, pady=2, fill="x")

# Create the main content frame
content_frame = ctk.CTkFrame(main_frame, corner_radius=10)
content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Create a frame to hold both forms
frame_forms_and_buttons = ctk.CTkFrame(content_frame, corner_radius=10)
frame_forms_and_buttons.pack(fill="both", padx=10, pady=5)
frame_forms_and_buttons.grid_columnconfigure(0, weight=1)
frame_forms_and_buttons.grid_columnconfigure(1, weight=1)
# Create the first form frame on the left
frame_form_left = ctk.CTkFrame(frame_forms_and_buttons, corner_radius=10)
frame_form_left.grid(row=0, column=0, padx=(10, 5), pady=7, sticky="nsew")

# Create the second form frame on the right
frame_form_right = ctk.CTkFrame(frame_forms_and_buttons, corner_radius=10)
frame_form_right.grid(row=0, column=1, padx=(5, 10), pady=7, sticky="nsew")

# Adjusting the column configuration to allocate space accordingly


# Configure grid layout for frame_form_left
frame_form_left.grid_rowconfigure((0, 1, 2, 3), weight=1)  
frame_form_left.grid_columnconfigure(0, weight=1)           
frame_form_left.grid_columnconfigure(1, weight=1)           

# Configure grid layout for frame_form_right
frame_form_right.grid_rowconfigure((0, 1, 2, 3), weight=1)
frame_form_right.grid_columnconfigure(0,weight=1)

# Adding labels with full-width expansion in frame_form_left
val = ctk.CTkLabel(frame_form_left, text="Enter ID", font=("Arial",14,"bold"), text_color="gray")
val.grid(row=0, column=1,padx=(0,33), pady=2,sticky="e")

valn = ctk.CTkLabel(frame_form_left, text="Enter valid \nItem Name", font=("Helvetica",14,"bold"), text_color="gray")
valn.grid(row=1, column=1, padx=(0,23), pady=2,sticky="e")

valq = ctk.CTkLabel(frame_form_left, text="", font=("Helvetica", 14, "bold"), text_color="gray")
valq.grid(row=2, column=1, padx=(0,10), pady=2,sticky="e")
valp = ctk.CTkLabel(frame_form_left, text="", font=("Helvetica", 14, "bold"))
valp.grid(row=3, column=1, padx=(0,10), pady=2,sticky="e")
# Bind resize event to frame to adjust font and wrapping on resize

# Create input fields in the left form frame
ctk.CTkLabel(frame_form_left, text="Item ID:", font=font_settings, anchor="w").grid(row=0, column=0, sticky="w", padx=17, pady=10)
combo_id = ctk.CTkComboBox(frame_form_left,values=d[0],corner_radius=10, height=30,width=150,command=on_item_selected)
combo_id.grid(row=0, column=1,padx=(15,120), pady=1,sticky="w")
combo_id.set('')
combo_id.bind('<KeyRelease>',search)


ctk.CTkLabel(frame_form_left, text="Item Name:", font=font_settings, anchor="w").grid(row=1, column=0, sticky="w", padx=17, pady=10)
entry_name =ctk.CTkComboBox(frame_form_left,values=d[1],corner_radius=10, height=30,width=150,command=on_item_selectedn)
entry_name.grid(row=1, column=1, padx=(15,120), pady=1,sticky="w")
entry_name.set('')
entry_name.bind('<KeyRelease>',searchn)

ctk.CTkLabel(frame_form_left, text="Req. Quantity:", font=font_settings, anchor="w").grid(row=2, column=0, sticky="w", padx=17, pady=10)
entry_quantity = ctk.CTkEntry(frame_form_left, font=font_settings, height=30,width=100)
entry_quantity.grid(row=2, column=1, padx=(15,120), pady=1,sticky="w")
entry_quantity.bind('<KeyRelease>', qt_check)

ctk.CTkLabel(frame_form_left, text="Price:", font=font_settings, anchor="w").grid(row=3, column=0, sticky="w", padx=17, pady=10)
entry_price = ctk.CTkEntry(frame_form_left, font=font_settings, height=30,width=100)
entry_price.grid(row=3, column=1, padx=15, pady=(1,0), sticky="w")

# Add buttons below the input fields in the left frame
ctk.CTkButton(frame_form_left, text="Add to Bill", font=font_settings, command=add_to_bill, height=40,width=270).grid(row=4, column=0, padx=(10,5), pady=(0, 5), sticky="w")
ctk.CTkButton(frame_form_left, text="Update Price or Quantity", font=font_settings, command=update_qt_n_price, height=40,width=275).grid(row=4, column=1, padx=(5,10), pady=(0, 5), sticky="e")
ctk.CTkButton(frame_form_left, text="Clear", font=font_settings, command=clear_fields, height=40,width=275).grid(row=5, column=1, padx=(5,10), pady=(2, 5), sticky="e")

ctk.CTkButton(frame_form_left, text="Reset Bill", font=font_settings, command=reset_bill, height=40,width=270).grid(row=5, column=0, padx=(10,5), pady=(2, 5), sticky="w")

# Create input fields in the right form frame
'''ctk.CTkLabel(frame_form_right, text="Bill Id:", font=font_settings, anchor="w").grid(row=0, column=0, sticky="w", padx=17, pady=10)
entry_billid = ctk.CTkEntry(frame_form_right, font=font_settings, height=30)
entry_billid.grid(row=0, column=1, padx=(15,120), pady=5, sticky="w")

ctk.CTkLabel(frame_form_right, text="Customer Name:", font=font_settings, anchor="w").grid(row=1, column=0, sticky="w", padx=17, pady=10)
entry_cname = ctk.CTkEntry(frame_form_right, font=font_settings, height=30)
entry_cname.grid(row=1, column=1, padx=15, pady=5, sticky="ew")

ctk.CTkLabel(frame_form_right, text="Phone Number:", font=font_settings, anchor="w").grid(row=2, column=0, sticky="w", padx=17, pady=10)
entry_cnum = ctk.CTkEntry(frame_form_right, font=font_settings, height=30)
entry_cnum.grid(row=2, column=1, padx=15, pady=5, sticky="ew")

ctk.CTkLabel(frame_form_right, text="Amount Paid:", font=font_settings, anchor="w").grid(row=3, column=0, sticky="w", padx=17, pady=10)
entry_amount = ctk.CTkEntry(frame_form_right, font=font_settings, height=30)
entry_amount.grid(row=3, column=1, padx=15, pady=5, sticky="ew")'''
ctk.CTkButton(frame_form_right, text="Print Bill", font=font_settings, command=print_bill,height=50).grid(padx=15, pady=(10,5),sticky="nsew")
ctk.CTkButton(frame_form_right, text="Open Bill", font=font_settings, command=open_bill,height=50).grid(padx=15, pady=(5,5),sticky="nsew")
ctk.CTkButton(frame_form_right, text="Update Bill", font=font_settings, command=open_bill,height=50).grid(padx=15, pady=(5,5),sticky="nsew")
ctk.CTkButton(frame_form_right, text="Return Item", font=font_settings, command=clear_fields,height=50).grid(padx=15, pady=(5,10),sticky="nsew")

# Create a frame to contain both treeviews and the total area
s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview.Heading', background="#356aa1", foreground="white", font=("Arial", 17, "bold"))
s.configure('Treeview', font=("Arial", 15, "bold"), rowheight=30)
frame_treeview_and_total = ctk.CTkFrame(content_frame, corner_radius=10,fg_color="#333")
frame_treeview_and_total.pack(fill="both", padx=5, pady=2, expand=True)

# Create a treeview for displaying bill items
treeview = ttk.Treeview(frame_treeview_and_total,columns=("Item ID", "Item Name", "Quantity", "Price", "Total"),show="headings",style="Treeview",height=4)
treeview.heading("Item ID", text="Item ID")
treeview.heading("Item Name", text="Item Name")
treeview.heading("Quantity", text="Quantity")
treeview.heading("Price", text="Price")
treeview.heading("Total", text="Total")

# Make the treeview columns stretch with the window
treeview.column("Item ID", anchor="center", width=100, stretch=True)
treeview.column("Item Name", anchor="center", width=100, stretch=True)
treeview.column("Quantity", anchor="center", width=100, stretch=True)
treeview.column("Price", anchor="center", width=100, stretch=True)
treeview.column("Total", anchor="center", width=100, stretch=True)

treeview.pack(fill="both", padx=10, pady=(5, 10), expand=True)
frame_treeview_and_total.grid_rowconfigure(1, weight=1)
frame_treeview_and_total.grid_columnconfigure(0, weight=1)

summary_treeview = ttk.Treeview(frame_treeview_and_total, columns=( "Amount"), show="headings", height=1)

summary_treeview.heading("Amount", text="Total Amount")


summary_treeview.column("Amount", anchor="center", width=120)


summary_treeview.pack(side="right", fill="y", pady=(0, 5),padx=10)

root.mainloop()


 









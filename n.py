def delete_and_shift_up(row_id, columns_to_delete):
    rows = list(treeview.get_children())
    
    # Ensure row_id exists
    if row_id not in rows:
        print(f"Row ID {row_id} does not exist.")
        return

    # Get the index of the target row
    target_index = rows.index(row_id)

    # Start processing from the target row to the last row
    for i in range(target_index, len(rows) - 1):
        current_row_id = rows[i]
        next_row_id = rows[i + 1]

        # Get values of the current and next rows
        current_values = list(treeview.item(current_row_id, "values"))
        next_values = list(treeview.item(next_row_id, "values"))

        # Replace the current row's target columns with the next row's values
        for col_index in columns_to_delete:
            current_values[col_index] = next_values[col_index]

        # Update the current row
        treeview.item(current_row_id, values=current_values)

    # Clear the target columns in the last row
    last_row_id = rows[-1]
    last_values = list(treeview.item(last_row_id, "values"))
    for col_index in columns_to_delete:
        last_values[col_index] = ""
    treeview.item(last_row_id, values=last_values)

    # Delete the last row
    treeview.delete(last_row_id)

# Updated logic for ensuring safe access to rows
rows = list(treeview.get_children())
flag2 = 0

for i in rows:
    row_values = treeview.item(i, "values")
    if str(item_id) == (row_values[2]):  # Ensure row exists and matches condition
        rw = i
        break
else:
    rw = None  # No matching row found

if rw is not None:  # Proceed only if a valid row is found
    v[4] = str(quantity)
    v[5] = f"₹{float(price):.2f}"
    total_price = int(quantity) * int(price)

    tam = int(tam) - int(float(v[6].replace("₹", ""))) + total_price

    v[6] = f"₹{float(total_price):.2f}"

    delete_and_shift_up(rw, [2, 3, 4, 5, 6, 7])
else:
    print(f"No row found with item ID {item_id}.")

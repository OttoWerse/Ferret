from tkinter import *

# Initialize row counter
current_row = 1



def GUI(list):
    # Fix pythons weirdness with namespaces
    global current_row
    current_row = 1
    # Create a list for tuples of entry fields
    tuples = []


    def add_row(key="", value=""):
        # Fix pythons weirdness with namespaces
        global current_row

        # Create entry field for the key
        key_entry_field = Entry(root)
        key_entry_field.insert(END, key)
        key_entry_field.grid(row=current_row)
        # Create entry field for the value
        value_entry_field = Entry(root)
        value_entry_field.insert(END, value)
        value_entry_field.grid(row=current_row, column=1)
        # Add entry field references to list
        tuples.append((key_entry_field, value_entry_field))

        # If the current row is not the first one
        if current_row > 1:
            # Create a function to delete the current row of a button
            def delete_row():
                tuples.remove((key_entry_field, value_entry_field))
                key_entry_field.destroy()
                value_entry_field.destroy()
                row_button.destroy()
            # Assign the function to the button in that row
            row_button = Button(root, text="-", command=delete_row)
        else:
            # Assign the function to add a row (only for the first button)
            row_button = Button(root, text="+", command=add_row)

        row_button.grid(row=current_row, column=2)

        # Increase the row counter
        current_row = current_row + 1

    def build_dict():
        # Clear the list (in order to sync deletions)
        list.clear()
        # Iterate through all tuples
        for tuple in tuples:
            # Get the key and value from the entry fields in the tuple
            key = tuple[0].get()
            value = tuple[1].get()
            # if they are not empty
            if key and value:
                # add an entry to the dict
                list[key] = value

    # Initialise Tk
    root = Tk()

    # If the passed list is not empty
    if len(list) > 0:
        # Add all list items as rows
        for key in list:
            add_row(key, list[key])
    else:
        # Add a single, empty, row
        add_row()

    # Add a button to safe the current rows
    commit_button = Button(root, text="Ausgabe", command=build_dict)
    commit_button.grid(column=0, row=0)

    # Start the Tk loop
    root.mainloop()


if __name__ == "__main__":
    # A small test case
    GUI({"hello": "world"})

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from classAddressBook import AddressBook, Record
from sorter import *


class MainApplication(tk.Tk):
    """
    The Main Application class for managing an address book and displaying various functionalities.

    Attributes:
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        event_time (datetime): The target event time for the countdown timer.
        remaining_time (timedelta): The time remaining until the target event.

    Methods:
        __init__(self): Initializes the MainApplication instance.
        center_window(self): Centers the application window on the screen.
        add_buttons(self): Adds buttons for managing contacts and triggering additional functionalities.
        add_treeview(self): Adds a Treeview widget for displaying contact information.
        search_contacts(self, tree, search_string): Searches and displays contacts based on a search string.
        show_birthday_contacts(self): Displays contacts with upcoming birthdays.
        show_sorting_files_window(self): Displays the Sorting Files window.
        update_timer(self): Updates and displays the countdown timer to the specified event.
    """
    def __init__(self):
        """
        Initializes the MainApplication instance.
        """
        tk.Tk.__init__(self)
        self.title("20th Century Fox Presents")
        self.iconbitmap('icon.ico')
        self.width = 1050
        self.height = 600
        self.geometry(f"{self.width}x{self.height}")
        self.center_window()

        self.address_book = address_book

        # Add labels
        label = tk.Label(self, text="ADDRESS BOOK MANAGEMENT:", font=("Calibri", 13))
        label.grid(row=0, column=0, columnspan=4, pady=10)

        self.add_buttons()
        self.add_treeview()

        event_time = datetime(datetime.now().year + 1, 1, 1, 0, 0, 0)
        
        self.event_time = event_time
        self.remaining_time = event_time - datetime.now()

        self.countdown_label = tk.Label(self, text="", font=("Helvetica", 8))
        self.countdown_label.config(fg='green')
        self.countdown_label.grid(row=3, column=4, padx=5, pady=5, sticky='e')

        self.update_timer()

    def center_window(self):        
        """
        Centers the application window on the screen.
        """
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f'+{x}+{y}')

    def add_buttons(self):
        """
        Adds buttons for managing contacts and triggering additional functionalities.
        """
        PADX = 10
        PADY = 5
        WIDTH = 16
        HEIGHT = 2

        # For "Add". Button 1:
        btn_add_contact = tk.Button(self, text="Add", command=lambda: AddContactWindow(self, address_book), width=WIDTH, height=HEIGHT)
        btn_add_contact.grid(row=1, column=0, sticky="w", padx=PADX, pady=PADY)

        # For "Change". Button 2:
        btn_change_contact = tk.Button(self, text="Change", command=lambda: ChangeContactWindow(self, address_book), width=WIDTH, height=HEIGHT)
        btn_change_contact.grid(row=1, column=1, sticky="w", padx=PADX, pady=PADY)

        # For "Delete". Button 3:
        btn_delete_contact = tk.Button(self, text="Delete", command=lambda: DeleteWindow(self, address_book), width=WIDTH, height=HEIGHT)
        btn_delete_contact.grid(row=1, column=2, sticky="w", padx=PADX, pady=PADY)

        # Add an empty label as a spacer between the two groups of buttons
        spacer_label = tk.Label(self, text="", width=WIDTH, height=HEIGHT)
        spacer_label.grid(row=1, column=3, padx=PADX, pady=PADY)

        # For "Birthday Contacts".  Button 4:
        btn_birthday_contacts = tk.Button(self, text="Birthday Contacts", command=self.show_birthday_contacts, width=WIDTH, height=HEIGHT)
        btn_birthday_contacts.grid(row=1, column=4, sticky="w", padx=PADX, pady=PADY)

        # For Other. "Sorting Files". Button 5:
        btn_sorting_files = tk.Button(self, text="Sorting files", command=self.show_sorting_files_window, width=WIDTH, height=HEIGHT)
        btn_sorting_files.grid(row=1, column=5, sticky="w", padx=PADX, pady=PADY)
        

    def add_treeview(self):
        """
        Adds a Treeview widget for displaying contact information.
        """
        columns_info = {
            "Name": {"text": "Name", "width": 150},
            "Phone": {"text": "Phone", "width": 150},
            "Email": {"text": "Email", "width": 150},
            "Address": {"text": "Address", "width": 150},
            "Birthday": {"text": "Birthday", "width": 150},
            "Notes": {"text": "Notes", "width": 260},
        }

        tree = ttk.Treeview(self, columns=list(columns_info.keys()), show="headings")

        for col, info in columns_info.items():
            tree.heading(col, text=info["text"])
            tree.column(col, width=info["width"])

        tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        tree.config(height=20)

        # Add search entry and button
        label = tk.Label(self, text="Enter search string:")
        label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=search_var, width=40)
        search_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        btn_search = tk.Button(self, text="Search", command=lambda: self.search_contacts(tree, search_var.get()), width=16, height=1)
        btn_search.grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)


    def search_contacts(self, tree, search_string):
        """
        Searches and displays contacts based on a search string.

        Parameters:
            tree (ttk.Treeview): The Treeview widget to display search results.
            search_string (str): The string to search for in contacts.
        """
        # Clear Treeview content before a new search
        tree.delete(*tree.get_children())

        found_contacts = self.address_book.find_data_in_book(search_string)

        # Display found contacts in Treeview
        if found_contacts:
            for record in found_contacts:
                record_data = {
                    "Name": record.name.name,
                    "Phone": ", ".join(phone.value for phone in record.phones),
                    "Email": ", ".join(email.value for email in record.emails),
                    "Address": record.address if record.address else "N/A",
                    "Birthday": str(record.birthday) if record.birthday else "N/A",
                    "Notes": record.notes if record.notes else "N/A",
                }
                tree.insert("", "end", text="ID", values=(record_data["Name"], record_data["Phone"],
                                                            record_data["Email"], record_data["Address"],
                                                            record_data["Birthday"], record_data["Notes"]))
        else:
            print("No results found")

    def show_birthday_contacts(self):
        """
        Displays contacts with upcoming birthdays.
        """
        days = simpledialog.askinteger("Input", "Enter the number of days:")
        if days is not None:
            birthday_contacts = self.address_book.filter_contacts_by_birthday(days)
            if birthday_contacts:
                message = "\n".join(f"{contact.name.name}: {contact.birthday}" for contact in birthday_contacts)
                messagebox.showinfo("Birthday Contacts", message)
            else:
                messagebox.showinfo("Birthday Contacts", "No contacts with birthdays in the specified period")

    # Other - "Sorting files"
    def show_sorting_files_window(self):
        """
        Displays the Sorting Files window.
        """
        sorting_files_window = SortingFilesWindow(self)
        sorting_files_window.center_window()

    def update_timer(self):
        self.remaining_time = self.event_time - datetime.now()
        days = self.remaining_time.days
        hours, remainder = divmod(self.remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        countdown_str = f"Countdown to New Year: {days} days {hours:02d}:{minutes:02d}:{seconds:02d}"
        self.countdown_label.config(text=countdown_str)

        self.after(1000, self.update_timer)


class AddContactWindow(tk.Toplevel):
    """
    A Toplevel window for adding or editing contact information.

    Attributes:
        parent (tk.Tk): The parent Tkinter window.
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.

    Methods:
        __init__(self, parent, address_book): Initializes the AddContactWindow instance.
        center_window(self): Centers the window on the screen.
        add_contact(self): Adds or updates a contact based on the entered information.
    """
    
    def __init__(self, parent, address_book):
        """
        Initializes the AddContactWindow instance.

        Parameters:
            parent (tk.Tk): The parent Tkinter window.
            address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        """
        super().__init__(parent)
        self.title("Add Contact")
        self.iconbitmap('icon.ico')

        # Setting the window position to the center of the screen
        window_width = 350
        window_height = 340
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.address_book = address_book

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        # List of names for the Combobox
        existing_names = [record.name.name for record in self.address_book.data.values()]
        self.name_var = tk.StringVar()
        self.name_combobox = ttk.Combobox(self, textvariable=self.name_var, values=existing_names, width=37)
        self.name_combobox.set("Select or Enter Name")
        self.name_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.phone_label = tk.Label(self, text="Phone:")
        self.phone_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self, textvariable=self.phone_var, width=40)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self, textvariable=self.email_var, width=40)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.address_label = tk.Label(self, text="Address:")
        self.address_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        self.address_var = tk.StringVar()
        self.address_entry = tk.Entry(self, textvariable=self.address_var, width=40)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.birthday_label = tk.Label(self, text="Birthday:")
        self.birthday_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)

        self.birthday_var = tk.StringVar()
        self.birthday_entry = tk.Entry(self, textvariable=self.birthday_var, width=40)
        self.birthday_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering notes
        self.notes_label = tk.Label(self, text="Notes:")
        self.notes_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

        self.notes_text = tk.Text(self, width=30, height=5)
        self.notes_text.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)


        self.notes_label = tk.Label(self, text="Note: You can add tags by prefixing them with the '#'", font=("Helvetica", 7))
        self.notes_label.grid(row=6, column=1, padx=10, pady=5) #, font=("Calibri", 8))


        self.add_button = tk.Button(self, text="Save", command=self.add_contact, width=10, height=1)
        self.add_button.grid(row=7, column=0, padx=30, pady=10, sticky=tk.W)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy, width=10, height=1)
        self.cancel_button.grid(row=7, column=1, padx=30, pady=10, sticky=tk.E)
        # To horizontally align the buttons
        self.add_button.grid(row=7, column=0, padx=30, pady=10, sticky=tk.W, columnspan=2)
    
    def center_window(self):
        """
        Centers the window on the screen.
        """
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f'+{x}+{y}')

    def add_contact(self):
        """
        Adds or updates a contact based on the entered information.
        """
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_var.get()
        birthday = self.birthday_var.get()

        try:
            # Attempt to retrieve an existing record by name
            existing_record = self.address_book.find(name)

            # Get notes from the Text widget
            notes = self.notes_text.get("1.0", tk.END).strip()

            if existing_record:
                # If the name exists, add phone, email, address, and birthday (if provided)
                if phone:
                    existing_record.add_phone(phone)
                if email:
                    existing_record.add_email(email)
                if address:
                    existing_record.address = address
                if birthday:
                    existing_record.add_birthday(birthday)
                if notes:
                    existing_record.notes = notes
            else:
                # If the name does not exist, create a new contact
                new_record = Record(name, birthday)
                if phone:
                    new_record.add_phone(phone)
                if email:
                    new_record.add_email(email)
                if address:
                    new_record.address = address
                if notes:
                    new_record.notes = notes

                self.address_book.add_record(new_record)

            # Save the changes and close the window
            self.address_book.save_to_json("address_book.json")

        except ValueError as e:
            self.grab_set()
            messagebox.showerror("Error", str(e))
            self.grab_release()
        else:
            self.address_book.save_to_json("address_book.json")
            messagebox.showinfo("Contact added", f"Contact name: {name}\nPhone number: {phone}\nEmail: {email}\nAddress: {address}\nBirthday: {birthday}")
            self.destroy()


class ChangeContactWindow(tk.Toplevel):
    """
    A Toplevel window for changing contact information.

    Attributes:
        parent (tk.Tk): The parent Tkinter window.
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.

    Methods:
        __init__(self, parent, address_book): Initializes the ChangeContactWindow instance.
        update_contact_details(self, event=None): Updates the displayed details based on the selected contact.
        save_changes(self): Saves the changes made to the contact and updates the address book.
    """
    
    def __init__(self, parent, address_book):
        """
        Initializes the ChangeContactWindow instance.

        Parameters:
            parent (tk.Tk): The parent Tkinter window.
            address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        """
        super().__init__(parent)
        self.title("Change Contact")
        self.iconbitmap('icon.ico')

        # Setting the window position to the center of the screen
        window_width = 400
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.address_book = address_book

        # Combo for selecting an existing contact
        self.select_contact_label = tk.Label(self, text="Select Contact:")
        self.select_contact_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        existing_contacts = list(self.address_book.data.keys())
        self.selected_contact_var = tk.StringVar()
        self.contact_combobox = ttk.Combobox(self, textvariable=self.selected_contact_var, values=existing_contacts, width=30)
        self.contact_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering the new contact name
        self.new_name_label = tk.Label(self, text="New Name:")
        self.new_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_name_var = tk.StringVar()
        self.new_name_entry = tk.Entry(self, textvariable=self.new_name_var, width=33)
        self.new_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Combo for selecting an existing phone number
        self.select_phone_label = tk.Label(self, text="Select Phone:")
        self.select_phone_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.selected_phone_var = tk.StringVar()
        self.phone_combobox = ttk.Combobox(self, textvariable=self.selected_phone_var, values=[], width=30)
        self.phone_combobox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering the new phone number
        self.new_phone_label = tk.Label(self, text="New Phone:")
        self.new_phone_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_phone_var = tk.StringVar()
        self.new_phone_entry = tk.Entry(self, textvariable=self.new_phone_var, width=33)
        self.new_phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        # Combo for selecting an existing email
        self.select_email_label = tk.Label(self, text="Select Email:")
        self.select_email_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)

        self.selected_email_var = tk.StringVar()
        self.email_combobox = ttk.Combobox(self, textvariable=self.selected_email_var, values=[], width=30)
        self.email_combobox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering the new email
        self.new_email_label = tk.Label(self, text="New Email:")
        self.new_email_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_email_var = tk.StringVar()
        self.new_email_entry = tk.Entry(self, textvariable=self.new_email_var, width=33)
        self.new_email_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering the new address
        self.new_address_label = tk.Label(self, text="New Address:")
        self.new_address_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_address_var = tk.StringVar()
        self.new_address_entry = tk.Entry(self, textvariable=self.new_address_var, width=33)
        self.new_address_entry.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering the new birthday
        self.new_birthday_label = tk.Label(self, text="New Birthday:")
        self.new_birthday_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.E)

        self.new_birthday_var = tk.StringVar()
        self.new_birthday_entry = tk.Entry(self, textvariable=self.new_birthday_var, width=33)
        self.new_birthday_entry.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

        # Text field for entering notes
        self.notes_label = tk.Label(self, text="Notes:")
        self.notes_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.E)

        self.notes_text = tk.Text(self, wrap=tk.WORD, width=25, height=5)
        self.notes_text.grid(row=8, column=1, padx=10, pady=5, sticky=tk.W)

        # Buttons to save changes or cancel
        self.save_button = tk.Button(self, text="Save Changes", command=self.save_changes, width=15, height=1)
        self.save_button.grid(row=9, column=0, padx=10, pady=10, sticky=tk.W)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy, width=15, height=1)
        self.cancel_button.grid(row=9, column=1, padx=10, pady=10, sticky=tk.E)

        # Bind the event to update phone numbers based on the selected contact
        self.contact_combobox.bind("<<ComboboxSelected>>", self.update_contact_details)

        # Initialize details for the first contact in the list (if available)
        if existing_contacts:
            first_contact = existing_contacts[0]
            self.selected_contact_var.set(first_contact)
            self.update_contact_details()

    def update_contact_details(self, event=None):
        """
        Updates the displayed details based on the selected contact.
        """
        selected_contact = self.selected_contact_var.get()
        if selected_contact:
            contact = self.address_book.find(selected_contact)
            if contact:
                # Update phone numbers
                phone_numbers = [str(phone) for phone in contact.phones]
                self.phone_combobox['values'] = phone_numbers
                if phone_numbers:
                    self.selected_phone_var.set(phone_numbers[0])
                else:
                    self.selected_phone_var.set("")

                # Update emails
                emails = [str(email) for email in contact.emails]
                self.email_combobox['values'] = emails
                if emails:
                    self.selected_email_var.set(emails[0])
                else:
                    self.selected_email_var.set("")

                # Update address
                self.new_address_var.set(contact.address if contact.address else "")

                # Update birthday
                self.new_birthday_var.set(str(contact.birthday) if contact.birthday else "")

                # Update notes
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert(tk.END, contact.notes if contact.notes else "")

    def save_changes(self):
        """
        Saves the changes made to the contact and updates the address book.
        """
        selected_contact = self.selected_contact_var.get()
        new_name = self.new_name_var.get()
        selected_phone = self.selected_phone_var.get()
        new_phone = self.new_phone_var.get()
        selected_email = self.selected_email_var.get()
        new_email = self.new_email_var.get()
        new_address = self.new_address_var.get()
        new_birthday = self.new_birthday_var.get()

        contact = self.address_book.find(selected_contact)
        if contact:
            # Remove the old contact from the address book
            self.address_book.delete(selected_contact)

            # Update the contact name if a new name is provided
            if new_name:
                contact.name.name = new_name

            # Update the phone number if a new phone number is provided
            if selected_phone and new_phone:
                contact.edit_phone(selected_phone, new_phone)

            # Update the email if a new email is provided
            if selected_email and new_email:
                contact.edit_email(selected_email, new_email)

            # Update the address if a new address is provided
            contact.address = new_address

            # Update the birthday if a new birthday is provided
            if new_birthday:
                contact.add_birthday(new_birthday)

            # Update notes
            notes = self.notes_text.get("1.0", tk.END).strip()
            contact.notes = notes

            # Add the updated contact back to the address book
            self.address_book.add_record(contact)

            # Save changes to the address book
            self.address_book.save_to_json("address_book.json")

            # Close the window
            self.destroy()
        else:
            messagebox.showerror("Error", "Selected contact not found")


class DeleteWindow(tk.Toplevel):
    """
    A Toplevel window for deleting contact-related information.

    Attributes:
        parent (tk.Tk): The parent Tkinter window.
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.

    Methods:
        __init__(self, parent, address_book): Initializes the DeleteWindow instance.
        delete_contact(self): Opens the DeleteContactWindow to delete a contact.
        delete_phone(self): Opens the DeletePhoneWindow to delete a phone number.
        delete_email(self): Opens the DeleteEmailWindow to delete an email.
    """
    
    def __init__(self, parent, address_book):
        """
        Initializes the DeleteWindow instance.

        Parameters:
            parent (tk.Tk): The parent Tkinter window.
            address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        """
        super().__init__(parent)
        self.title("Delete")
        self.iconbitmap('icon.ico')

        # Setting the window position to the center of the screen
        window_width = 400
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.address_book = address_book

        # Кнопки
        self.delete_contact_button = tk.Button(self, text="Delete Contact", command=self.delete_contact, width=16, height=2)
        self.delete_contact_button.pack(side=tk.LEFT, padx=10)

        self.delete_phone_button = tk.Button(self, text="Delete Phone", command=self.delete_phone, width=16, height=2)
        self.delete_phone_button.pack(side=tk.LEFT, padx=10)

        self.delete_email_button = tk.Button(self, text="Delete Email", command=self.delete_email, width=16, height=2)
        self.delete_email_button.pack(side=tk.LEFT, padx=10)

    def delete_contact(self):
        """
        Opens the DeleteContactWindow to delete a contact.
        """
        DeleteContactWindow(self, address_book)

    def delete_phone(self):
        """
        Opens the DeletePhoneWindow to delete a phone number.
        """
        DeletePhoneWindow(self, address_book)

    def delete_email(self):
        """
        Opens the DeleteEmailWindow to delete an email.
        """
        DeleteEmailWindow(self, address_book)


class DeleteContactWindow(tk.Toplevel):
    """
    A Toplevel window for deleting a contact.

    Attributes:
        parent (tk.Tk): The parent Tkinter window.
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.

    Methods:
        __init__(self, parent, address_book): Initializes the DeleteContactWindow instance.
        delete_contact(self): Deletes the selected contact from the address book.
    """
    
    def __init__(self, parent, address_book):
        """
        Initializes the DeleteContactWindow instance.

        Parameters:
            parent (tk.Tk): The parent Tkinter window.
            address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        """
        super().__init__(parent)
        self.title("Delete Contact")
        self.iconbitmap('icon.ico')

        # Setting the window position to the center of the screen
        window_width = 280
        window_height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.address_book = address_book

        # Combo for selecting an existing contact
        self.select_contact_label = tk.Label(self, text="Select Contact:")
        self.select_contact_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        existing_contacts = list(self.address_book.data.keys())
        self.selected_contact_var = tk.StringVar()
        self.contact_combobox = ttk.Combobox(self, textvariable=self.selected_contact_var, values=existing_contacts, width=20)
        self.contact_combobox.state(['readonly'])
        self.contact_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Button to delete contact or cancel
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_contact, width=10, height=1)
        self.delete_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy, width=10, height=1)
        self.cancel_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

    def delete_contact(self):
        """
        Deletes the selected contact from the address book.
        """
        selected_contact = self.selected_contact_var.get()

        if selected_contact:
            # Check if the contact exists
            existing_contact = self.address_book.find(selected_contact)

            if existing_contact:
                # Delete the selected contact from the address book
                self.address_book.delete(selected_contact)

                messagebox.showinfo("Delete Contact", "Contact deletion successfully completed.")

                # Save changes to the address book
                self.address_book.save_to_json("address_book.json")

                # Close the window
                self.destroy()
            else:
                messagebox.showerror("Error", "Selected contact not found")
        else:
            messagebox.showerror("Error", "Selected contact not specified")


class DeletePhoneWindow(tk.Toplevel):
    """
    A Toplevel window for deleting a phone number associated with a contact.

    Attributes:
        parent (tk.Tk): The parent Tkinter window.
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.

    Methods:
        __init__(self, parent, address_book): Initializes the DeletePhoneWindow instance.
        update_phone_numbers(self, event=None): Updates the available phone numbers based on the selected contact.
        delete_phone(self): Deletes the selected phone number from the associated contact.
    """
    
    def __init__(self, parent, address_book):
        """
        Initializes the DeletePhoneWindow instance.

        Parameters:
            parent (tk.Tk): The parent Tkinter window.
            address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        """
        super().__init__(parent)
        self.title("Delete Phone")
        self.iconbitmap('icon.ico')

        # Setting the window position to the center of the screen
        window_width = 280
        window_height = 140
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.address_book = address_book

        # Combo for selecting an existing contact
        self.select_contact_label = tk.Label(self, text="Select Contact:")
        self.select_contact_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        existing_contacts = list(self.address_book.data.keys())
        self.selected_contact_var = tk.StringVar()
        self.contact_combobox = ttk.Combobox(self, textvariable=self.selected_contact_var, values=existing_contacts, width=20)
        self.contact_combobox.state(['readonly'])
        self.contact_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Combo for selecting an existing phone number
        self.select_phone_label = tk.Label(self, text="Select Phone:")
        self.select_phone_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.selected_phone_var = tk.StringVar()
        self.phone_combobox = ttk.Combobox(self, textvariable=self.selected_phone_var, values=[], width=20)
        self.phone_combobox.state(['readonly'])
        self.phone_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Buttons to delete phone or cancel
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_phone, width=10, height=1)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy, width=10, height=1)
        self.cancel_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)

        # Bind the event to update phone numbers based on the selected contact
        self.contact_combobox.bind("<<ComboboxSelected>>", self.update_phone_numbers)

        # Initialize details for the first contact in the list (if available)
        if existing_contacts:
            first_contact = existing_contacts[0]
            self.selected_contact_var.set(first_contact)
            self.update_phone_numbers()

    def update_phone_numbers(self, event=None):
        """
        Updates the available phone numbers based on the selected contact.

        Parameters:
            event (tk.Event, optional): The event that triggered the update.
        """
        selected_contact = self.selected_contact_var.get()
        if selected_contact:
            contact = self.address_book.find(selected_contact)
            if contact:
                # Update phone numbers
                phone_numbers = [str(phone) for phone in contact.phones]
                self.phone_combobox['values'] = phone_numbers
                if phone_numbers:
                    self.selected_phone_var.set(phone_numbers[0])
                else:
                    self.selected_phone_var.set("")

    def delete_phone(self):
        """
        Deletes the selected phone number from the associated contact.
        """
        selected_contact = self.selected_contact_var.get()
        selected_phone = self.selected_phone_var.get()

        if selected_contact and selected_phone:
            contact = self.address_book.find(selected_contact)
            if contact:
                # Delete the selected phone number from the contact
                contact.remove_phone(selected_phone)

                messagebox.showinfo("Delete Phone", "Phone number deletion successfully completed")

                # Save changes to the address book
                self.address_book.save_to_json("address_book.json")

                # Close the window
                self.destroy()
        else:
            messagebox.showerror("Error", "Selected contact or phone number not found")


class DeleteEmailWindow(tk.Toplevel):
    """
    A Toplevel window for deleting an email address associated with a contact.

    Attributes:
        parent (tk.Tk): The parent Tkinter window.
        address_book (AddressBook): An instance of the AddressBook class for managing contacts.

    Methods:
        __init__(self, parent, address_book): Initializes the DeleteEmailWindow instance.
        update_email_addresses(self, event=None): Updates the available email addresses based on the selected contact.
        delete_email(self): Deletes the selected email address from the associated contact.
    """

    def __init__(self, parent, address_book):
        """
        Initializes the DeleteEmailWindow instance.

        Parameters:
            parent (tk.Tk): The parent Tkinter window.
            address_book (AddressBook): An instance of the AddressBook class for managing contacts.
        """
        super().__init__(parent)
        self.title("Delete Email")
        self.iconbitmap('icon.ico')

        # Setting the window position to the center of the screen
        window_width = 280
        window_height = 140
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.address_book = address_book

        # Combo for selecting an existing contact
        self.select_contact_label = tk.Label(self, text="Select Contact:")
        self.select_contact_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        existing_contacts = list(self.address_book.data.keys())
        self.selected_contact_var = tk.StringVar()
        self.contact_combobox = ttk.Combobox(self, textvariable=self.selected_contact_var, values=existing_contacts, width=20)
        self.contact_combobox.state(['readonly'])
        self.contact_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Combo for selecting an existing email
        self.select_email_label = tk.Label(self, text="Select Email:")
        self.select_email_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.selected_email_var = tk.StringVar()
        self.email_combobox = ttk.Combobox(self, textvariable=self.selected_email_var, values=[], width=20)
        self.email_combobox.state(['readonly'])
        self.email_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Buttons to delete email or cancel
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_email, width=10, height=1)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy, width=10, height=1)
        self.cancel_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)

        # Bind the event to update emails based on the selected contact
        self.contact_combobox.bind("<<ComboboxSelected>>", self.update_email_addresses)

        # Initialize details for the first contact in the list (if available)
        if existing_contacts:
            first_contact = existing_contacts[0]
            self.selected_contact_var.set(first_contact)
            self.update_email_addresses()

    def update_email_addresses(self, event=None):
        """
        Updates the available email addresses based on the selected contact.

        Parameters:
            event (tk.Event, optional): The event that triggered the update.
        """
        selected_contact = self.selected_contact_var.get()
        if selected_contact:
            contact = self.address_book.find(selected_contact)
            if contact:
                # Update email addresses
                email_addresses = [str(email) for email in contact.emails]
                self.email_combobox['values'] = email_addresses
                if email_addresses:
                    self.selected_email_var.set(email_addresses[0])
                else:
                    self.selected_email_var.set("")

    def delete_email(self):
        """
        Deletes the selected email address from the associated contact.
        """
        selected_contact = self.selected_contact_var.get()
        selected_email = self.selected_email_var.get()

        if selected_contact and selected_email:
            contact = self.address_book.find(selected_contact)
            if contact:
                contact.remove_email(selected_email)

                messagebox.showinfo("Delete Email", "Email address deletion successfully completed.")

                # Save changes to the address book
                self.address_book.save_to_json("address_book.json")

                self.destroy()
        else:
            messagebox.showerror("Error", "Selected contact or email address not found")


class SortingFilesWindow(tk.Toplevel):
    """
    A Toplevel window for configuring and initiating the sorting of files in a specified directory.

    Attributes:
        main_app: The main application instance.
        path_var (tk.StringVar): A Tkinter variable to store the path for sorting.

    Methods:
        __init__(self, main_app): Initializes the SortingFilesWindow instance.
        center_window(self): Centers the window on the screen.
        sorting_files(self): Initiates the sorting of files based on the specified path.
    """

    def __init__(self, main_app):
        """
        Initializes the SortingFilesWindow instance.

        Parameters:
            main_app: The main application instance.
        """
        tk.Toplevel.__init__(self, main_app)

        self.title("Sorting Files")
        self.iconbitmap('icon.ico')

        self.path_var = tk.StringVar()

        # Text input fields
        path_label = tk.Label(self, text="Path for Sorting:")
        path_entry = tk.Entry(self, width=30, textvariable=self.path_var)

        # Placing widgets on a window
        path_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        path_entry.grid(row=0, column=1, padx=10, pady=5)

        # Buttons "Save" and "Cancel"
        save_button = tk.Button(self, text="Save", command=self.sorting_files, width=10, height=1)
        cancel_button = tk.Button(self, text="Cancel", command=self.destroy, width=10, height=1)

        save_button.grid(row=1, column=0, sticky="e", padx=30, pady=10)
        cancel_button.grid(row=1, column=1, sticky="e", padx=30, pady=10)

    def center_window(self):
        """
        Centers the window on the screen.
        """
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f'+{x}+{y}')

    def sorting_files(self):
        """
        Initiates the sorting of files based on the specified path.
        """
        path_s = self.path_var.get()
        
        # <--  Here, the logic for "Sorting Files"
        main(f'sort {path_s}')

        messagebox.showinfo("Information", f"Sorting files in a directory: {path_s}")
        self.destroy()


address_book = AddressBook()

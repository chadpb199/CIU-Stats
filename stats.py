import tkinter as tk
import ttkbootstrap as ttk
import os
from datetime import datetime
import sqlite3 as sql

# get location of the .py file
__location__ = os.path.realpath(os.path.dirname(__file__))

class App(ttk.Window):
    """
    ttk.Window based class that generates and runs a data entry window.
    """
    
    def __init__(self):
        super().__init__(
        title="JCSO CIU Stats",
        iconphoto=None
        )
        
        # sqlite3 connection and cursor
        self.con = sql.connect(os.path.join(__location__, "ciu_stats.db"))
        self.cur = self.con.cursor()
        
        # Configure grid layout of the window.
        self.rowconfigure((0,1,2,3,5), weight=0)  # Rows won't grow
        self.rowconfigure(4, weight=1)      # Row will grow
        self.columnconfigure(0, weight=0)   # Col won't grow
        self.columnconfigure(1, weight=1)   # Col will grow
        
        # Get icon image from same dir as .py file and set the default icon.
        jcso_det_badge = tk.PhotoImage(
            file=os.path.join(__location__, "JCSO Detective Badge.png")
            )
        self.iconphoto(True, jcso_det_badge)
        
        # Generate the Data Entry Widgets and place in the window.
        self.data = DataEntryWidgets(self)
        self.data.grid(row=0, column=0, sticky="new")
        self.data.set_tab_order()
        
        # Generate the Data Management Buttons and place in the window.
        self.data_btns = DataBtns(self)
        self.data_btns.grid(row=1, column=0, sticky="new")
        
        # Generate the Data Table widget and place in the window.
        self.data_tbl = DataTable(self)
        self.data_tbl.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=10,
            pady=10
            )
            
        # Initialize Data Table with data from database
        self.data_tbl.update_table()
        
        self.mainloop()


class LabelEntry(ttk.Frame):
    """
    Custom widget - ttk.Frame containing a ttk.Label next to a ttk.Entry
    
    Args:   parent:str - parent for the frame
            label_text:str - text displayed on the label
            style:str - bootstyle of the widgets
            width:int - width of the entry widget
    """
    
    def __init__(self,
        parent,
        label_text:str,
        style:str="default",
        width:int=None,
        ):
        super().__init__(parent)
        # Generate the Label and Entry widgets.
        self.lbl = ttk.Label(self, text=label_text, bootstyle=style)
        self.entry = ttk.Entry(self, bootstyle=style, width=width)
        
        # Pack the generated widgets into the frame.
        self.lbl.pack(side="left", padx=2)
        self.entry.pack(side="left", padx=2)


class LabelDate(ttk.Frame):
    """
    Custom widget - ttk.Frame containing a ttk.Label next to a ttk.DateEntry.
    
    Args:   parent:str - parent for the frame
            label_text:str - text displayed on the label
            style:str - bootstyle of the widgets
    """

    def __init__(
        self,
        parent,
        label_text:str,
        style:str="default"
        ):
        
        super().__init__(parent)
        # Generate the Label and DateEntry widgets.
        self.lbl = ttk.Label(self, text=label_text, bootstyle=style)
        self.date = ttk.DateEntry(self, bootstyle=style)
        self.date.entry.delete(0, ttk.END)
        self.date.button.configure(takefocus=0)
        
        # Pack the generated widgets into the frame.
        self.lbl.pack(side="left", padx=2)
        self.date.pack(side="left", padx=2)


class LabelSpin(ttk.Frame):
    """
    Custom widget - ttk.Frame containing a ttk.Label next to a ttk.Spinbox.
    
    Args:   parent:str - parent for the frame
            label_text:str - text displayed on the label
            style:str - bootstyle of the widgets
    """
    
    def __init__(
        self,
        parent,
        label_text:str,
        style:str="default",
        ):
            
        super().__init__(parent)
        # Generate the Label and Spinbox widgets.
        self.lbl = ttk.Label(self, text=label_text, bootstyle=style)
        self.spin = ttk.Spinbox(
            self,
            bootstyle=style,
            from_=0, to=100,
            width=8)
        
        # Pack the generated widgets into the frame.
        self.lbl.pack(side="left", padx=2)
        self.spin.pack(side="left", padx=2)


class DataEntryWidgets(ttk.Frame):
    """
    Generate a ttk.Frame containing several custom widgets for data entry.
    
    Args:   parent:any - parent for the frame
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure the grid layout for the frame.
        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2), weight=1)
        
        # Initialize in-custody checkbutton var
        self.custody_var = ttk.StringVar()
        
        # Generate and place the data entry widgets
        self.generate_data_entry_widgets()
        self.place_data_entry_widgets()
        
        
    def generate_data_entry_widgets(self):
        """
        Generate data entry field widgets for the DataEntryWidgets class.
        """
        
        self.crn_field = LabelEntry(
            parent=self,
            label_text="CRN",
            width=15,
            )
        self.report_date_field = LabelDate(
            parent=self,
            label_text="REPORT DATE"
            )
        self.incident_code_field = LabelEntry(
            parent=self,
            label_text="INCIDENT DESCRIPTION",
            width=40,
            )
        self.filed_date_field = LabelDate(
            parent=self,
            label_text="DATE FILED"
            )
        self.charges_field = LabelSpin(
            parent=self,
            label_text="CHARGES"
            )
        self.warrants_field = LabelSpin(
            parent=self,
            label_text="SEARCH WARRANTS"
            )
        self.custody_btn = ttk.Checkbutton(
            self,
            text="IN CUSTODY",
            bootstyle="warning-outline-toolbutton",
            variable=self.custody_var,
            takefocus=0,
            onvalue="X",
            offvalue="",
            )
        self.detective_field = LabelEntry(
            parent=self,
            label_text="DETECTIVE",
            width = 25,
            )
        
    def place_data_entry_widgets(self):
        """
        Place the data entry field widgets into the DataEntryWidgets frame.
        """
        self.crn_field.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
            )
        self.report_date_field.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
            )
        self.filed_date_field.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=5,
            pady=5
            )
        self.incident_code_field.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5,
            columnspan=2
            )
        self.custody_btn.grid(
            row=1,
            column=2,
            sticky="nsew",
            padx=5,
            pady=5
            )
        self.charges_field.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
            )
        self.warrants_field.grid(
            row=2,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
            )
        self.detective_field.grid(
            row=2,
            column=2,
            sticky="nsew",
            padx=5,
            pady=5
            )
    
    def set_tab_order(self):
        """
        Set proper tab order for widgets inside the DataEntryWidgets class.
        """
        widgets = [self.crn_field, self.report_date_field,
            self.filed_date_field, self.incident_code_field, self.custody_btn,
            self.charges_field, self.warrants_field, self.detective_field]
            
        for w in widgets:
            w.lift()

class DataBtns(ttk.Frame):
    """
    Generate a ttk.Frame containing buttons to manage data in the table.
    
    Args:   parent:any - parent for the frame
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent
        
        # Generate the button widgets.
        self.add_btn = ttk.Button(
            self,
            text="ADD",
            width = 20,
            bootstyle="success",
            command=self.add_data
            )
        self.delete_btn = ttk.Button(
            self,
            text="DELETE",
            width = 20,
            bootstyle="danger"
            )
        self.export_btn = ttk.Button(
            self,
            text="EXPORT",
            width = 20,
            bootstyle="info"
            )
        self.print_btn = ttk.Button(
            self,
            text="PRINT",
            width = 20,
            bootstyle="info"
            )
        
        # Place the button widgets in the frame
        self.add_btn.grid(row=0, column=0, padx=10)
        self.delete_btn.grid(row=0, column=1, padx=10)
        self.export_btn.grid(row=0, column=2, padx=10)
        self.print_btn.grid(row=0, column=3, padx=10)
        
    def add_data(self):
        """
        Adds the data from DataEntryWidgets to the database, then clears the
        DataEntryWidgets fields except for detective_field.
        """

        # Create a list and add the data from the entry fields
        self.data_lst = []
        self.data_lst.append(
            self.root.data.crn_field.entry.get()
            )
        self.data_lst.append(
            self.root.data.report_date_field.date.entry.get()
            )
        self.data_lst.append(
            self.root.data.filed_date_field.date.entry.get()
            )
        self.data_lst.append(
            self.root.data.incident_code_field.entry.get()
            )
        self.data_lst.append(
            self.root.data.custody_var.get()
            )
        self.data_lst.append(
            self.root.data.charges_field.spin.get()
            )
        self.data_lst.append(
            self.root.data.warrants_field.spin.get()
            )
        self.data_lst.append(
            self.root.data.detective_field.entry.get()
            )
        
        # Add data from list into database and commit
        self.root.cur.execute("""
            INSERT INTO stats VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
            """, data_lst
            )
        self.root.con.commit()
        
        # Update data table to display new information
        self.root.data_tbl.update_table()
        
        self.clear_data()
        
    def clear_data(self):
        """
        Clear data entry fields for next entry EXCEPT DETECTIVE.
        Used by add_data().
        """
        self.root.data.crn_field.entry.delete(0, ttk.END)
        self.root.data.report_date_field.date.entry.delete(0, ttk.END)
        self.root.data.filed_date_field.date.entry.delete(0, ttk.END)
        self.root.data.incident_code_field.entry.delete(0, ttk.END)
        self.root.data.custody_var.set(0)
        self.root.data.charges_field.spin.delete(0, ttk.END)
        self.root.data.warrants_field.spin.delete(0, ttk.END)

class DataTable(ttk.Treeview):
    """
    Custom ttk.Treeview for a multicolumn data table
    
    Args:   parent:any - parent for the frame
    """
    
    def __init__(self, parent):
        # Get column headers from database
        self.root = parent
        data = self.root.cur.execute("SELECT * FROM stats")
        self.headers = [c[0] for c in data.description]
        
        super().__init__(
            parent,
            columns=self.headers,
            show="headings",
            bootstyle="primary"
            )
        
        # Display column headers
        for col in self.headers:
            self.heading(col, text=col, anchor=ttk.W)
            
        # Set column widths
        self.column(0, width=75, stretch=False)
        self.column(1, width=100, stretch=False)
        self.column(2, width=100, stretch=False)
        self.column(3, width=400, stretch=False)
        self.column(4, width=85, stretch=False)
        self.column(5, width=75, stretch=False)
        self.column(6, width=125, stretch=False)
        
    def update_table(self, order_by:str="CRN"):
        """
        Clears the data table and repopulates it with the information from the
        database.
        """
        # Clear the data table
        self.delete(*self.get_children())
        
        # Get the data from the database and turn it into a list of tuples
        sql_data = self.root.cur.execute(
            f"SELECT * FROM stats ORDER BY {order_by}"
            )
        data_lst = [row for row in sql_data]
        
        # display the data on the table
        for row in data_lst:
            self.insert("", "end", iid=row[0], values=row)

if __name__ == "__main__":
    App()
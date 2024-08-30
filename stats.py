import tkinter as tk
import ttkbootstrap as ttk
import os
from datetime import datetime
import sqlite3 as sql

# Get location of the .py file
__location__ = os.path.realpath(os.path.dirname(__file__))

class App(ttk.Window):
    """
    ttk.Window based class that generates and runs a data entry window.
    """
    
    def __init__(self):
        super().__init__(
        title="JCSO CIU Stats",
        iconphoto=None,
        minsize=(662, 372)
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
            
        # TESTING ONLY
        self.init_test_data()
            
        # Initialize Data Table with data from database
        self.data_tbl.update_table()
        
        self.update()
        print(self.winfo_width(), self.winfo_height(), sep=", ")
        
        self.mainloop()
        
    def init_test_data(self):
        self.cur.execute("DELETE FROM stats")
        # Test data for database
        test_data = [
            ('24-00001', '08/20/2024', '08/21/2024', 'desc 1',
            'X', 1, 0, 'det 1'),
            ('24-00002', '08/22/2024', '08/23/2024', 'desc 2',
            '', 3, 2, 'det 2'),
            ('24-00003', '08/24/2024', '08/25/2024', 'desc 3',
            'X', 5, 4, 'det 1'),
            ('24-00004', '08/26/2024', '08/26/2024', 'desc 4',
            'X', 7, 6, 'det 1'),
            ('24-00005', '08/28/2024', '08/29/2024', 'desc 5',
            '', 9, 8, 'det 2'),
            ]
            
        self.cur.executemany("""INSERT INTO stats
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", test_data)
        self.con.commit()
        self.data_tbl.update_table()


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
    
    Args:   parent:Any - parent for the frame
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
    
    Args:   parent:Any - parent for the frame
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
            bootstyle="danger",
            command=self.delete_data
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
        
        Args:   data_lst:list - list of tuples with data for the database.
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
        
        self.clear_fields()
        
    def clear_fields(self):
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
        
    def delete_data(self):
        """
        Delete selected data rows from the databse and update the Treeview.
        """
        
        # Get selected data
        sel = [(row,) for row in self.root.data_tbl.selection()]
        
        # Delete selected data from database
        self.root.cur.executemany("""DELETE FROM stats
            WHERE "CRN" = ?""", sel)
        
        self.root.con.commit()
        self.root.data_tbl.update_table()


class DataTable(ttk.Frame):
    """
    Custom ttk.Frame widget with a ttk.Treeview for a multicolumn data table
    and scrollbars.
    
    Args:   parent:Any - parent for the frame
    """

    def __init__(self, parent):
        self.root = parent
        super().__init__(self.root)
        
        # Configure grid geometry
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        
        # Generate widgets for the frame
        self.gen_data_treeview()
        self.gen_scrollbars()
        
    def gen_data_treeview(self):
        """
        Generate ttk.Treeview to display data from database.
        """
        
        # Get data and headings from database
        data = self.root.cur.execute("SELECT * FROM stats")
        headers = [c[0] for c in data.description]
        
        # Generate tree
        self.tree = ttk.Treeview(
            self,
            columns=headers,
            show="headings",
            bootstyle="primary"
            )
        
        # Set column headings and widths
        widths = [75, 100, 100, 400, 85, 75, 125]
        for col in headers:
            self.tree.heading(col, text=col, anchor=ttk.W)
            
        for i in range(7):
            self.tree.column(
                i,
                width=widths[i],
                stretch=False
                )
        
        # Grid tree into parent frame
        self.tree.grid(row=0, column=0, sticky="nsew")
        
    def gen_scrollbars(self):
        """
        Generate two ttk.Scrollbar widgets to scroll the ttk.Treeview.
        """
        
        # Generate scrollbars
        self.vscroll = ttk.Scrollbar(
            self,
            orient=ttk.VERTICAL,
            command=self.tree.yview
            )
            
        self.hscroll = ttk.Scrollbar(
            self,
            orient=ttk.HORIZONTAL,
            command=self.tree.xview
            )
            
        # Tie scrollbar position and size to the tree
        self.tree.configure(
            yscrollcommand=self.vscroll.set,
            xscrollcommand=self.hscroll.set
            )
        
        # Grid scrollbars into the parent frame
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll.grid(row=1, column=0, sticky="ew")
        
    def update_table(self, order_by:str="CRN"):
        """
        Clears the data table and repopulates it with the information from the
        database.
        """
        # Clear the data table
        self.tree.delete(*self.tree.get_children())
        
        # Get the data from the database and turn it into a list of tuples
        sql_data = self.root.cur.execute(
            f"SELECT * FROM stats ORDER BY {order_by}"
            )
        data_lst = [row for row in sql_data]
        
        # display the data on the table
        for row in data_lst:
            self.tree.insert("", "end", iid=row[0], values=row)
        
if __name__ == "__main__":
    root = App()

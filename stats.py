import tkinter as tk
import ttkbootstrap as ttk
import os
from datetime import datetime

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
        self.custody_var = ttk.IntVar()
        
        # Generate and place the data entry widgets
        self.generate_data_entry_widgets()
        self.place_data_entry_widgets()
        
        
    def generate_data_entry_widgets(self):
        # Generate all of the widgets for the frame.
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
            variable=self.custody_var
            )
        self.detective_field = LabelEntry(
            parent=self,
            label_text="DETECTIVE",
            width = 25,
            )
        
    def place_data_entry_widgets(self):    
        # Place all of the generated widgets into the frame.
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


class DataBtns(ttk.Frame):
    """
    Generate a ttk.Frame containing buttons to manage data in the table.
    
    Args:   parent:any - parent for the frame
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
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
            bootstyle="primary"
            )
        self.print_btn = ttk.Button(
            self,
            text="PRINT",
            width = 20,
            bootstyle="primary"
            )
        
        # Place the button widgets in the frame
        self.add_btn.grid(row=0, column=0, padx=10)
        self.delete_btn.grid(row=0, column=1, padx=10)
        self.export_btn.grid(row=0, column=2, padx=10)
        self.print_btn.grid(row=0, column=3, padx=10)
        
    def custody_display(self):
        if self.parent.data.custody_var.get() == 0:
            self.in_custody = ""
        else:
            self.in_custody = "X"
        
        return self.in_custody
        
    def add_data(self):
        
        # create a list and add the data from the entry fields
        data_lst = []
        data_lst.append(self.parent.data.crn_field.entry.get())
        data_lst.append(self.parent.data.report_date_field.date.entry.get())
        data_lst.append(self.parent.data.filed_date_field.date.entry.get())
        data_lst.append(self.parent.data.incident_code_field.entry.get())
        data_lst.append(self.custody_display())
        data_lst.append(self.parent.data.charges_field.spin.get())
        data_lst.append(self.parent.data.warrants_field.spin.get())
        data_lst.append(self.parent.data.detective_field.entry.get())
        print(data_lst)
        
        # clear data entry fields for next entry
        self.parent.data.crn_field.entry.delete(0, ttk.END)
        self.parent.data.report_date_field.date.entry.delete(0, ttk.END)
        self.parent.data.filed_date_field.date.entry.delete(0, ttk.END)
        self.parent.data.incident_code_field.entry.delete(0, ttk.END)
        self.parent.data.custody_var.set(0)
        self.parent.data.charges_field.spin.delete(0, ttk.END)
        self.parent.data.warrants_field.spin.delete(0, ttk.END)
        self.parent.data.detective_field.entry.delete(0, ttk.END)


class DataTable(ttk.Treeview):
    """
    Custom ttk.Treeview for a multicolumn data table
    
    Args:   parent:any - parent for the frame
    """
    
    def __init__(self, parent):
        # List of column headers
        self.headers = ["CRN", "REPORT DATE", "INCIDENT DESCRIPTION", "DATE FILED",
        "CHARGES", "SEARCH WARRANTS", "IN-CUSTODY", "DETECTIVE"]
        
        super().__init__(parent, columns=self.headers, show="headings", bootstyle="primary")
        
        # display column headers
        for col in self.headers:
            self.heading(col, text=col)        


if __name__ == "__main__":
    App()
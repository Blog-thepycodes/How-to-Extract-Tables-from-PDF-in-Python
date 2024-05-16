import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import tabula
 
 
def extract_tables():
   # Open file dialog to select PDF file
   file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
   if file_path:
       try:
           # Read tables from the selected PDF
           tables = tabula.read_pdf(file_path, pages="all", output_format="json", stream=True)
 
 
           # Clear previous content from the text widget
           text_widget.delete(1.0, tk.END)
 
 
           # Function to write table data to text widget with aligned columns
           def write_table_to_text_widget(table_data):
               # Calculate maximum width for each column
               max_widths = [max(len(str(cell.get("text", ""))) for cell in column) for column in zip(*table_data)]
               # Format and insert rows with aligned columns
               for row in table_data:
                   row_str = "\t".join(str(cell.get("text", "")).center(width) for cell, width in zip(row, max_widths))
                   text_widget.insert(tk.END, row_str + "\n")
               text_widget.insert(tk.END, "\n")
 
 
           # Write tables to text widget
           for i, table in enumerate(tables):
               text_widget.insert(tk.END, f"Table {i + 1}:\n")
               if "data" in table:
                   write_table_to_text_widget(table["data"])
               else:
                   text_widget.insert(tk.END, "No table data found.\n\n")
 
 
           messagebox.showinfo("Success", "Tables extracted successfully!")
 
 
       except Exception as e:
           messagebox.showerror("Error", f"An error occurred: {str(e)}")
 
 
# Create main Tkinter window
root = tk.Tk()
root.title("PDF Table Extractor - The Pycodes")
 
 
# Create text widget to display tables
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_widget.pack(padx=10, pady=10)
 
 
# Create button to trigger table extraction
extract_button = tk.Button(root, text="Extract Tables", command=extract_tables)
extract_button.pack(pady=10)
 
 
# Run the Tkinter event loop
root.mainloop()

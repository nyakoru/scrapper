from essential import fetch_csv
from essential import info
from essential import data_detail
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import logging
from card_essential import card_functions
from datetime import datetime

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y %H-%M-%S")

misc.mkdir('EditorLogs')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all messages

# Create file handlers for different log levels
info_handler = logging.FileHandler(f'./EditorLogs/info.log')
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(f'./EditorLogs/error.log')
error_handler.setLevel(logging.ERROR)

warning_handler = logging.FileHandler(f'./EditorLogs/warning.log')
warning_handler.setLevel(logging.WARNING)

# Create formatters and set them for the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
warning_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(warning_handler)

class Editor:
    def __init__(self, data):
        self.data = data
    
    def search(self, key, value):
        results = []
        data_index = data_detail(self.data)
        for item in self.data:
            if key not in item: return NameError
            if value == item[key]:
                index = data_index.get_index(item)
                results.append((index, item))
        return results
            
    def update_key_value(self, index, key, value):
        dict_data = self.data[index]
        information = info(dict_data)
        if isinstance(value, list):
            updated_dict = information.listvalue_add(key = key, add_value = value)
        else:
            updated_dict = information.change_value(key = key, update_value = value)
        data = data_detail(self.data)
        self.data = data.replace_item(index, updated_dict)

    def beautify_dict(self, dictionary):
        import json
        return json.dumps(dictionary, indent=4)
    
    def load_from_file(self, directory, file_name):
        file_path = f'{directory}/{file_name}'
        if os.path.exists(file_path):
            file = fetch_csv(directory=directory, file_name=file_name)
            self.data = file.read()
            return True
        else:
            return False
        
    def overwrite_file(self, directory, file_name):
        try:
            file = fetch_csv(directory=directory, file_name=file_name)
            file.dump(self.data)
            print('Data overwritten')
            return True
        except Exception as e:
            print(f'Fail to overwrite data {e}')
            return False
    
    
class EditorGUI:
    def __init__(self, root, editor):
        self.editor = editor
        self.root = root
        self.root.title("Data Editor")
        self.logger = logger

        #file Frame
        self.file_admin = tk.Frame(root)
        self.file_admin.pack(padx=10, pady=10)

        tk.Label(self.file_admin, text="File Name:").grid(row=0, column=0, padx=5, pady=5)
        self.file_name_entry = tk.Entry(self.file_admin)
        self.file_name_entry.insert(0,'YGO')
        self.file_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.file_admin, text="Directory:").grid(row=1, column=0, padx=5, pady=5)
        self.directory_entry = tk.Entry(self.file_admin)
        self.directory_entry.insert(0,'./')
        self.directory_entry.grid(row=1, column=1, padx=5, pady=5)

        self.load_button = tk.Button(self.file_admin, text="Load File", command=self.load_file)
        self.load_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # Search Frame
        self.search_frame = tk.Frame(root)
        self.search_frame.pack(padx=10, pady=10)

        tk.Label(self.search_frame, text="Search Key:").grid(row=0, column=0, padx=5, pady=5)
        self.search_key_entry = tk.Entry(self.search_frame)
        self.search_key_entry.insert(0,'name')
        self.search_key_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.search_frame, text="Search Value:").grid(row=1, column=0, padx=5, pady=5)
        self.search_value_entry = tk.Entry(self.search_frame)
        self.search_value_entry.insert(0,'Photon Alexandra Queen')
        self.search_value_entry.grid(row=1, column=1, padx=5, pady=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # Update Frame
        self.update_frame = tk.Frame(root)
        self.update_frame.pack(padx=10, pady=10)

        tk.Label(self.update_frame, text="Key:").grid(row=0, column=0, padx=5, pady=5)
        self.update_key_entry = tk.Entry(self.update_frame)
        self.update_key_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.update_frame, text="Value:").grid(row=1, column=0, padx=5, pady=5)
        self.update_value_entry = tk.Entry(self.update_frame)
        self.update_value_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.update_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5)
        self.update_type_entry = tk.Entry(self.update_frame)
        self.update_type_entry.grid(row=2, column=1, padx=5, pady=5)

        self.update_button = tk.Button(self.update_frame, text="Update Key-Value", command=self.update_key_value)
        self.update_button.grid(row=3, columnspan=2, padx=5, pady=5)
        
        # Display Frame
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(padx=10, pady=10)

        self.result_text = tk.Text(self.display_frame, height=50, width=100, wrap=tk.WORD)
        self.result_text.pack()

        self.save_button = tk.Button(self.display_frame, text="Save changes", command=self.save_changes)
        self.save_button.pack(pady=5)

        self.selected_index = None
        self.selected_data = None

    def perform_search(self):
        key = self.search_key_entry.get()
        value = self.search_value_entry.get()
        value = value.split(',') if ',' in value else value #pending removal
        results = self.editor.search(key, value)
        result_str = '\n'.join(self.editor.beautify_dict(result) for item, result in results)
        if len(results) == 1:
            self.selected_index = results[0][0]
            self.selected_data = results[0][1] #first data
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_str if result_str else "No results found.")

    def update_key_value(self):
        if self.selected_index is not None:
            key = self.update_key_entry.get()
            value = self.update_value_entry.get()
            value = value.split(',') if ',' in value else value
            ctype = self.update_type_entry.get()
            value = eval(f"{ctype}('{value}')")

            try:
                self.editor.update_key_value(self.selected_index, key, value)
                self.perform_search()
                current_datetime = datetime.now()
                formatted_datetime = current_datetime.strftime("%d-%m-%Y %H-%M-%S")
                self.logger.info(f"update {self.selected_index} {key} {value} {formatted_datetime}")
                messagebox.showinfo("Success", "Key-Value pair updated.")
            except IndexError:
                messagebox.showerror("Error", "Index out of range.")
        else:
            messagebox.showerror("Error", "No dictionary selected from the search results.")

    def load_file(self):
        file_name = str(self.file_name_entry.get())
        if '.json' not in file_name:
            file_name = f'{file_name}.json'

        directory = str(self.directory_entry.get())
        if directory == ('' or None):
            directory = './'

        if self.editor.load_from_file(directory, file_name):
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%d-%m-%Y %H-%M-%S")
            self.logger.info(f"load {file_name} {formatted_datetime}")
            messagebox.showinfo("Success", "File loaded successfully.")
        else:
            messagebox.showerror("Error", "Invalid file. File does not exist or cannot be read.")

    def save_changes(self):
        directory = self.directory_entry.get()
        file_name = self.file_name_entry.get()
        
        if self.editor.overwrite_file(directory=directory, file_name=file_name):
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%d-%m-%Y %H-%M-%S")
            self.logger.info(f"saved {file_name} {formatted_datetime}")
            messagebox.showinfo("File saved")
        else:
            messagebox.showerror("Fail to save.")

if __name__ == "__main__":

    data = []
    root = tk.Tk()
    editor = Editor(data)
    gui = EditorGUI(root, editor)
    root.mainloop()
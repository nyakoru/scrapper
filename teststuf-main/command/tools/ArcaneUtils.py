import sys
import os

import json
import csv

from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional

@dataclass
class fetch_json:
    directory: str = "./"
    file_name: str = "New File"
    print_switch: bool = True
    repeat_check: bool = True

    def json_file_correction(self, file_path: str) -> str:
        """Ensure the file path ends with '.json' and starts with './'."""
        if not file_path.endswith('.json'):
            file_path += '.json'
        if not file_path.startswith('./'):
            file_path = './' + file_path.lstrip('./')
        return file_path

    def list_checker(self, input_list: list, target) -> bool:
        """Check if a target exists in the provided list."""
        return target in input_list

    def read(self) -> list:
        from command.tools.logrecord import logger
        """Read and return the contents of the JSON file."""
        try:
            location = self.json_file_correction(os.path.join(self.directory, self.file_name))
            with open(location, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"TLS-AU-FETCHJ-READ: File not found at {location}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"TLS-AU-FETCHJ-READ: JSON decode error in {location} - {e}")
            return []
        except Exception as e:
            logger.error(f"TLS-AU-FETCHJ-READ: {location} - {e}")
            return []

    def json_add(self, old_data: list, new_data: dict):
        """Add new data to the existing JSON file."""
        try:
            old_data.append(new_data)
            location = self.json_file_correction(os.path.join(self.directory, self.file_name))
            with open(location, 'w', encoding='utf-8') as file:
                json.dump(old_data, file, ensure_ascii=False, indent=4)
            if self.print_switch: print(f"Data added successfully to {self.file_name}")
        except Exception as e:
            if self.print_switch: print(f"JSON Add Error: {e}")

    def add(self, new_data: dict):
        """Add new data to the JSON file if not already present."""
        try:
            location = self.json_file_correction(os.path.join(self.directory, self.file_name))
            with open(location, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        if self.repeat_check and self.list_checker(data, new_data):
            if self.print_switch: print(f"Data already exists: {new_data}")
        else:
            self.json_add(data, new_data)

    def dump(self, data: list) -> bool:
        """Overwrite the JSON file with the provided data."""
        try:
            location = self.json_file_correction(os.path.join(self.directory, self.file_name))
            with open(location, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            if self.print_switch: print(f"Data dumped successfully to {self.file_name}")
            return True
        except Exception as e:
            from command.tools.logrecord import logger
            logger.error(f"TLS-AU-FETCHJ-DUMP-{self.directory}, {self.file_name} - {e}")
            return False
        
@dataclass
class Download:
    directory: str = './'
    print_switch: bool = True

    def image_extension_check(self, file_name):
        extensions = [".png", ".jpg"]
        if not any(file_name.endswith(ext) for ext in extensions):
            file_name += ".png"
        return file_name

    def image(self, url: str, file_name: str) -> bool:
        """"""
        from command.tools.logrecord import logger
        from io import BytesIO
        from PIL import Image
        import requests
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = self.image_extension_check(file_name)
                file_location = os.path.join(self.directory, file_name)
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image.save(f'{file_location}', quality=100)
                if self.print_switch: print(f'{url} Downloaded Successfully')
                return True
            else:
                logger.error(f'TLS-AU-DOWNL-IMAGE-{response.status_code}')
                return False
        except Exception as e:
            logger.error(f"TLS-AU-DOWNL-IMAGE-{url} {self.directory}/{file_name}.png {e}")
            return False

    def blank(self, file_name: str) -> bool:
        from command.tools.logrecord import logger
        from PIL import Image
        width, height = 100, 100
        image = Image.new("RGB", (width, height), "white")
        try:
            file_name = self.image_extension_check(file_name)
            file_location = os.path.join(self.directory, file_name)
            image.save(f'{file_location}')
            if self.print_switch:
                logger.warning(f'{file_name} Blank Saved')
            return True
        except Exception as e:
            logger.error(f'Download Blank Error {e}')
            return False

@dataclass
class fetch_csv:
    directory:str = "./"
    file_name:str = "New File"
    print_switch:bool = False

    def read(self, remove_header: bool = False) -> List[List[str]]:
        """
        Reads the CSV file and returns its contents as a list of rows.
        If remove_header is True, skips the first row.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        data = []
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            if remove_header:
                next(reader, None)
            data.extend(row for row in reader)
        return data

    def json_format(self, remove_header: bool = False) -> List[Dict[str, str]]:
        """
        Reads the CSV file and returns its contents as a list of dictionaries.\n
        Each row is represented as a dictionary with keys from the header.\n
        Example:\n
        
        name,age,city\          \n                  
        Alice,30,New York       \n               
        Bob,25,Los Angeles      \n      
               to                          
       [{                           \n
            "name": "Alice",        \n
            "age": "30",            \n
            "city": "New York"      \n
            },                      \n
            {                       \n
            "name": "Bob",          \n
            "age": "25",            \n
            "city": "Los Angeles"   \n
            }]                      \n                            
                                            
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if remove_header:
                next(reader, None)
            return list(reader)

    def overwrite(self, data_list: List[Union[List[str], Dict[str, str]]], there_is_header: bool = False) -> None:
        """
        Overwrites the CSV file with the provided data.
        - data_list can either be a list of lists or a list of dictionaries.
        - If there_is_header is True, the first dictionary's keys will be used as the header row.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            if isinstance(data_list[0], dict):
                writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
                if there_is_header:
                    writer.writeheader()
                writer.writerows(data_list)
            else:
                writer = csv.writer(file)
                writer.writerows(data_list)

    def append(self, data: Union[List[str], Dict[str, str]]) -> None:
        """
        Appends a single row to the CSV file.
        - If data is a dictionary, it appends it as a row using the existing header.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            if isinstance(data, dict):
                writer = csv.DictWriter(file, fieldnames=data.keys())
                writer.writerow(data)
            else:
                writer = csv.writer(file)
                writer.writerow(data)

    def filter_rows(self, column_name: str, value: str) -> List[Dict[str, str]]:
        """
        Filters rows based on a column value and returns matching rows as a list of dictionaries.
        Only works if the file has a header.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        filtered_data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[column_name] == value:
                    filtered_data.append(row)
        return filtered_data

    def delete_rows(self, column_name: str, value: str) -> None:
        """
        Deletes rows where the specified column matches the given value.
        Writes back the modified data to the file.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        rows_to_keep = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows_to_keep = [row for row in reader if row[column_name] != value]

        self.overwrite(rows_to_keep, there_is_header=True)

    def get_columns(self) -> List[str]:
        """
        Returns the column names (header) of the CSV file.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return next(reader, [])

    def get_row_count(self, exclude_header: bool = False) -> int:
        """
        Returns the number of rows in the CSV file. Excludes the header if exclude_header is True.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
        return len(rows) - (1 if exclude_header else 0)

    def add_column(self, column_name: str, default_value: Optional[str] = None) -> None:
        """
        Adds a new column to the CSV file with an optional default value for all rows.
        If the CSV file does not exist, it creates a new one with the specified column.
        """
        updated_data = []
        file_path = f"{self.directory}/{self.file_name}"
        if misc.path_check(file_path):
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames + [column_name] if reader.fieldnames else [column_name]
                for row in reader:
                    row[column_name] = default_value
                    updated_data.append(row)
        else:
            fieldnames = [column_name]

        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            if updated_data:
                writer.writerows(updated_data)
            else:
                writer.writerow({column: default_value for column in fieldnames})

    def column_values(self, column_name: str) -> List[str]:
        """
        Returns all values in the specified column.
        """
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        values = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                values.append(row[column_name])
        return values

    def add_row_list(self, row_data:List[list]):
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(row_data)

    def add_row_dict(self, row_data:List[dict]):
        file_path = f"{self.directory}/{self.file_name}"
        try:
            misc.verify_path(self.directory, file_path)
            with open(file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
            with open(file_path, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerows(row_data)
        except FileNotFoundError:
            with open(file_path, mode="w", newline="") as file:
                fieldnames = row_data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(row_data)

class misc:
    
    @staticmethod
    def mkdir(folder_path: str) -> None:
        """
        Creates a directory if it doesn't exist.
        
        Args:
            folder_path (str): Path of the directory to create.
        
        Returns:
            None
        """
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except Exception as e:
                from command.tools.logrecord import logger
                logger.error(f"TLS-AU-MISC-MKDIR-Err {folder_path}: {e}")
                sys.exit(1)

    @staticmethod
    def path_check(folder_path: str) -> bool:
        """
        Checks if a folder exists.
        
        Args:
            folder_path (str): Path of the folder to check.
        
        Returns:
            bool: True if the folder exists, False otherwise.
        """
        return os.path.exists(folder_path)
    
    @staticmethod
    def get_folders(parent_path: str) -> List[str]:
        """
        Retrieves a list of folder names in the specified directory.
        
        Args:
            path (str): Path to the directory.
        
        Returns:
            List[str]: A list of folder names within the directory.
        """
        if not os.path.exists(parent_path) or not os.path.isdir(parent_path):
            return []
        return [name for name in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path, name))]
    
    @staticmethod
    def verify_path(directory:str, file_path:str) -> bool:
        if directory not in ['./','']:
            if not misc.path_check(directory): raise FileNotFoundError("Directory not found")
        if not misc.path_check(file_path): raise FileNotFoundError("File not found")
        return True

@dataclass
class data_detail:
    data:list

    def get_index(self, element) -> int:
        """Returns the index of the element"""
        try:
            index = self.data.index(element)
            return index
        except ValueError: 
            raise ValueError
    
    def replace_item(self, index, element) -> list:
        """Replaces the element to the new element at the input index"""
        try:
            self.data[index] = element
            return self.data
        except Exception: 
            raise Exception

@dataclass
class fetch_file:
    directory: str = "./"
    file_name: str = "New File"
    print_switch: bool = False
    """file name needs to specify extension"""

    def read(self):
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
        
    def write(self, data):
        file_path = f"{self.directory}/{self.file_name}"
        with open(file_path, 'w', encoding = 'utf-8') as file:
            file.write(data)
            if self.print_switch: print(f"Data saved to file {file_path}.")
        
    def add(self, lineData):
        file_path = f"{self.directory}/{self.file_name}"
        misc.verify_path(self.directory, file_path)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.writelines(lineData+'\n')
            if self.print_switch: print(f"Data added to file {file_path}.")

class Wrapper:
    @staticmethod
    def log_function_call(func):
        from functools import wraps
        from command.tools.logrecord import logger
        @wraps(func)
        def wrapper(*args, **kwargs): 
            logger.info(f"func {func.__name__}, input: {args}, {kwargs}")
            return func(*args, **kwargs)
        return wrapper
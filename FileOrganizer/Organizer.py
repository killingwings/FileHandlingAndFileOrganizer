from pathlib import Path
import shutil
import logging
from FileHandeling import FileHandlingOperations as m
import json

# -------------------------------------------------------------------------
# Ensure logs folder exists (Fix for missing log directory)
# -------------------------------------------------------------------------
# Get the absolute path to the project root (PYTHONPROJECTS folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_PATH = LOG_DIR / "fileOrganizer.log"

# Clear any existing handlers to avoid conflicts
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging
logging.basicConfig(
    filename=str(LOG_PATH),  # Convert Path to string
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    force=True  # Force reconfiguration
)

# Add console handler to see logs in terminal too (optional)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger('').addHandler(console)

logging.info("="*50)
logging.info("FileOrganizer logger initialized successfully")
logging.info(f"Log file location: {LOG_PATH}")
logging.info("="*50)


class FileOrganizer:
    extensionToCategoryData = {}
    def __init__(self, base_path):
        """Initialize object with base path + FileHandling instance."""
        self.base_path = base_path
        self.fileHandelingObj = m.FileHandling(self.base_path)
        
        logging.info(f"FileOrganizer initialized at path: {self.base_path}")


    # -------------------------------------------------------------------------
    # STATIC METHOD: Validate folder name
    # -------------------------------------------------------------------------
    @staticmethod
    def validateFolderName(name):
        name = name.strip()

        if not name:
            logging.warning("Attempted to create folder with empty name")
            return [False, "Folder name cannot be empty"]

        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for ch in invalid_chars:
            if ch in name:
                logging.warning(f"Invalid character '{ch}' in folder name: {name}")
                return [False, f"Folder name {name} contains invalid character: {ch}"]

        if name in [".", ".."]:
            logging.warning("User entered reserved folder name")
            return [False, "Invalid folder name"]

        if len(name) > 255:
            logging.warning(f"Folder name too long: {name}")
            return [False, f"Folder name '{name}' is too long"]

        return [True, "Valid folder name", name]

    # -------------------------------------------------------------------------
    # Safe Input
    # -------------------------------------------------------------------------
    @staticmethod
    def getInput(message, inputType):
        try:
            user_input = input(message)

            if inputType == int:
                return [True, int(user_input)]

            elif inputType == float:
                return [True, float(user_input)]

            elif inputType == str:
                return [True, user_input.strip()]
            
            logging.warning(f"Unsupported input type: {inputType}")
            return [False, "Unsupported input type"]

        except ValueError:
            logging.error(f"Invalid input type. Expected {inputType.__name__}")
            return [False, f"Invalid {inputType.__name__} value"]

        except Exception as err:
            logging.error(f"Error in input: {err}")
            return [False, str(err)]

    # -------------------------------------------------------------------------
    # Load JSON Data
    # -------------------------------------------------------------------------
    def loadJSON(self,file_name):
        try:
            p = self.fileHandelingObj.getPath(file_name)

            with open(p, "r") as fs:
                data = json.load(fs)

            return [True, data]

        except FileNotFoundError:
            return [False, f"JSON file '{file_name}' not found"]

        except json.JSONDecodeError as err:
            return [False, f"Invalid JSON format: {err}"]

        except Exception as err:
            return [False, str(err)]  
    # -------------------------------------------------------------------------
    # File Extensions to Category Mapping
    # -------------------------------------------------------------------------
    @staticmethod
    def extensionToCategory(myDict):
        try:
            if not isinstance(myDict, dict):
                logging.error(f"Invalid input type: expected dict, got {type(myDict).__name__}")
                return [False, f"Invalid input: expected dictionary, got {type(myDict).__name__}"]

            result = {}

            # Iterate categories and their extension lists
            for category, extList in myDict.items():

                # Validate category
                if not isinstance(category, str):
                    msg = f"Invalid category '{category}' (type {type(category).__name__}). Expected string."
                    logging.error(msg)
                    return [False, msg]

                # Validate extension list type
                if not isinstance(extList, list):
                    msg = f"Extensions for category '{category}' must be a list. Found {type(extList).__name__}."
                    logging.error(msg)
                    return [False, msg]

                # Process extensions
                for extension in extList:

                    # Validate extension type
                    if not isinstance(extension, str):
                        msg = f"Extension '{extension}' in category '{category}' must be a string."
                        logging.error(msg)
                        return [False, msg]

                    # Validate extension format
                    if not extension.startswith("."):
                        msg = f"Extension '{extension}' in category '{category}' must start with '.'."
                        logging.error(msg)
                        return [False, msg]

                    ext_lower = extension.lower()

                    # Duplicate extension check
                    if ext_lower in result:
                        logging.warning(
                            f"Duplicate extension '{extension}'. Already mapped to '{result[ext_lower]}'. "
                            f"Ignoring duplicate under '{category}'."
                        )
                    else:
                        result[ext_lower] = category.lower()

            logging.info("Extension-to-category mapping created successfully.")
            return [True, result]

        except Exception as err:
            logging.error(f"Unexpected error in extensionToCategory: {err}")
            return [False, str(err)]

    # -------------------------------------------------------------------------
    # Create Folder
    # -------------------------------------------------------------------------
    def createFolder(self, name):
        try:
            validName = FileOrganizer.validateFolderName(name)
            if not validName[0]:
                logging.warning(f"Create folder failed: {validName[1]}")
                return validName

            folder_name = validName[2]
            p = self.fileHandelingObj.getPath(folder_name)

            if p.exists():
                logging.warning(f"Folder already exists: {name}")
                return [False, f"Folder '{name}' already exists"]

            p.mkdir()
            logging.info(f"Folder created: {name}")
            return [True, f"Folder '{name}' created successfully"]

        except Exception as err:
            logging.error(f"Create folder error: {err}")
            return [False, str(err)]

    # -------------------------------------------------------------------------
    # Read Folder
    # -------------------------------------------------------------------------
    def readFolderContent(self, name: str) -> list:
        try:
            validName = FileOrganizer.validateFolderName(name)
            if not validName[0]:
                logging.warning(f"Read folder failed: {validName[1]}")
                return validName

            p = self.fileHandelingObj.getPath(validName[2])

            if not p.exists():
                logging.warning(f"Folder does not exist: {name}")
                return [False, f"Folder '{name}' does not exist"]

            logging.info(f"Reading folder: {name}")
            return self.fileHandelingObj.getAllFilesAndFolder(p) # type: ignore

        except Exception as err:
            logging.error(f"Read folder error: {err}")
            return [False, str(err)]

    # -------------------------------------------------------------------------
    # Rename Folder
    # -------------------------------------------------------------------------
    def renameFolder(self, name: str, newName: str) -> list:
        try:
            valid = FileOrganizer.validateFolderName(newName)
            if not valid[0]:
                logging.warning(f"Rename failed: {valid[1]}")
                return valid

            old_path = self.fileHandelingObj.getPath(name)
            if not old_path.exists():
                logging.warning(f"Folder does not exist: {name}")
                return [False, f"Folder '{name}' does not exist"]

            new_path = self.fileHandelingObj.getPath(newName)
            if new_path.exists():
                logging.warning(f"New folder name already exists: {newName}")
                return [False, f"Folder '{newName}' already exists"]

            old_path.rename(new_path)
            logging.info(f"Folder renamed: {name} → {newName}")
            return [True, "Folder renamed successfully"]

        except Exception as err:
            logging.error(f"Rename folder error: {err}")
            return [False, str(err)]

    # -------------------------------------------------------------------------
    # Delete Folder
    # -------------------------------------------------------------------------
    def deleteFolder(self, name: str) -> list:
        try:
            p = self.fileHandelingObj.getPath(name)

            if not p.exists():
                logging.warning(f"Delete failed: folder does not exist: {name}")
                return [False, f"Folder '{name}' does not exist"]

            result = self.fileHandelingObj.getAllFilesAndFolder(p) # type: ignore

            if result[1]:  
                mode = FileOrganizer.getInput(
                    f"Folder '{name}' is not empty.\n"
                    "Press 1 to delete everything OR 2 to cancel: ",
                    int
                )

                if not mode[0]:
                    logging.warning(f"User cancelled deletion of non-empty folder: {name}")
                    return mode

                if mode[1] == 1:
                    shutil.rmtree(p)
                    logging.info(f"Folder deleted with contents: {name}")
                    return [True, f"Folder '{name}' deleted successfully"]

                logging.info(f"User cancelled folder deletion: {name}")
                return [False, f"Folder '{name}' not deleted"]

            p.rmdir()
            logging.info(f"Folder deleted: {name}")
            return [True, f"Folder '{name}' deleted successfully"]

        except Exception as err:
            logging.error(f"Delete folder error: {err}")
            return [False, str(err)]
    
    # -------------------------------------------------------------------------
    # File Operations
    # -------------------------------------------------------------------------
    def fileOperations(self, folderName):
        try:
            # Resolve path
            p = self.fileHandelingObj.getPath(folderName)

            # Check folder exists
            if not p.exists():
                logging.warning(f"Folder does not exist: {folderName}")
                return [False, f"Folder '{folderName}' does not exist"]

            # Log start
            logging.info(f"Reading folder: {folderName}")

            # Get files & folders
            items = self.fileHandelingObj.getAllFilesAndFolder(p) #type: ignore
            logging.info(f"Found {len(items)} items in folder '{folderName}'")

            # File operations (your run() has no return)
            logging.info(f"Performing file handling operations on folder: {folderName}")
            m.FileHandling(p).run() #type: ignore

            # Log success
            logging.info(f"File handling completed for folder: {folderName}")

            return [True, "Operation completed"]

        except Exception as err:
            logging.error(f"Error while processing folder '{folderName}': {err}")
            return [False, str(err)]
    # -------------------------------------------------------------------------
    # Folder Organizer Category Helper Function
    # -------------------------------------------------------------------------
    def getCategoryForFile(self,item):
        ext = item.suffix.lower()
        if ext == "":
            logging.info(f"File '{item.name}' has no extension -> 'others'")
            return "others"
        # Determine category
        if ext in FileOrganizer.extensionToCategoryData:
            category = FileOrganizer.extensionToCategoryData[ext]
        else:
            logging.info(f"Unknown extension '{ext}' -> assigning to 'others'")
            category = "others"
        return category
    # -------------------------------------------------------------------------
    # Folder Organizer
    # -------------------------------------------------------------------------

    def organizeMyFolder(self, folderName, extensionFileName):
        try:
            # Resolve path
            p = self.fileHandelingObj.getPath(folderName)

            # Check folder exists
            if not p.exists():
                logging.warning(f"Folder does not exist: {folderName}")
                return [False, f"Folder '{folderName}' does not exist"]

            logging.info(f"Organizing folder: {folderName}")

            # ----------------------------------------------------
            # Load JSON Mapping (only once)
            # ----------------------------------------------------
            if not FileOrganizer.extensionToCategoryData:

                data = self.loadJSON(extensionFileName)
                if not data[0]:
                    logging.error(data[1])
                    return data

                result = FileOrganizer.extensionToCategory(data[1])
                if not result[0]:
                    logging.error(result[1])
                    return result

                FileOrganizer.extensionToCategoryData = result[1]
                logging.info("Extension mapping loaded successfully.")

            # ----------------------------------------------------
            # Read folder contents
            # ----------------------------------------------------
            items = self.fileHandelingObj.getAllFilesAndFolder(p)  # type: ignore
            if not items[0]:
                return items

            all_items = items[1]
            logging.info(f"Found {len(all_items)} items in folder '{folderName}'")

            # ----------------------------------------------------
            # Organize each file
            # ----------------------------------------------------
            for item in all_items:

                
                # Skip folders
                if item.is_dir():
                    continue
                category = self.getCategoryForFile(item)
                # Skip categories you don't want to organize
                if category in ["code", "others"]:
                    continue

                # Build category folder
                category_folder = p / category
                category_folder.mkdir(exist_ok=True)

                # Final destination path
                destination = category_folder / item.name
                
                conflict = 1
                # Check If File with same name already exists in the destination folder
                while destination.exists():
                    # Rename File
                    ext = item.suffix 
                    fileName = item.stem
                    newName = f"{fileName}({conflict}){ext}"
                    logging.info(f"Conflict detected → trying new name: {newName}")
                    conflict += 1
                    destination = category_folder / newName
                    # logging.info(f"File {item.name} Renamed as {newName}")
                    
                logging.info(f"Moving '{item.name}' → '{category_folder}'")

                # Move file
                shutil.move(str(item), str(destination))

            return [True, f"Folder '{folderName}' organized successfully"]

        except Exception as err:
            logging.error(f"Error while organizing folder '{folderName}': {err}")
            return [False, str(err)]
    # -------------------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------------------
    def run(self):
        try:
            logging.info("FileOrganizer program started")

            while True:
                # Display current base directory contents
                items = self.fileHandelingObj.getAllFilesAndFolder()
                if items[0]:
                    print("\n========== Current Directory ==========")
                    for i, item in enumerate(items[1], start=1):
                        print(f"{i}. {item.name}")
                    print("=======================================\n")

                # Menu
                print("1. Create Folder")
                print("2. Read Folder")
                print("3. Rename Folder")
                print("4. Delete Folder")
                print("5. File Operations (open folder in FileHandling)")
                print("6. Organize Folder")
                print("7. Exit\n")

                # Get user choice
                choice = FileOrganizer.getInput("Selection: ", int)
                if not choice[0]:
                    print(choice[1])
                    continue

                choice = choice[1]

                match choice:
                    case 1:
                        name = input("Enter folder name to create: ").strip()
                        result = self.createFolder(name)
                        print(result[1])

                    case 2:
                        name = input("Enter folder name to read: ").strip()
                        result = self.readFolderContent(name)
                        if result[0]:
                            print("\n--- Folder Contents ---")
                            if result[1]:
                                for i, item in enumerate(result[1], start=1):
                                    print(f"{i}. {item.name}")
                            else:
                                print(f"Folder '{name}' is empty")
                            print("------------------------\n")
                        else:
                            print(result[1])

                    case 3:
                        name = input("Enter folder name to rename: ").strip()
                        newName = input("Enter new folder name: ").strip()
                        result = self.renameFolder(name, newName)
                        print(result[1])

                    case 4:
                        name = input("Enter folder name to delete: ").strip()
                        result = self.deleteFolder(name)
                        print(result[1])

                    case 5:
                        name = input("Enter folder name for file operations: ").strip()
                        result = self.fileOperations(name)
                        print(result[1])

                    case 6:
                        name = input("Enter the folder name you want to organize: ").strip()
                        result = self.organizeMyFolder(name, "fileExtensions.json")
                        print(result[1])

                    case 7:
                        logging.info("Program exited by user")
                        print("Exiting...")
                        break

                    case _:
                        print("Invalid choice. Please try again.")

        except Exception as err:
            logging.error(f"Unexpected error in run(): {err}")
            print("Unexpected Error:", err)






# import shutil
# from pathlib import Path
# import os
# from FileHandeling import main as m

# class FileOrganizer:
#     def __init__(self,base_path):
#         self.base_path = base_path
#         self.fileHandelingObj = m.FileHandling(self.base_path)
#     @staticmethod
#     def validateFolderName(name):
        
#         # Trim spaces
#         name = name.strip()
#         # 1. Empty name check
#         if not name:
#             return [False, "Folder name cannot be empty"]

#         # 2. Illegal characters
#         invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
#         for ch in invalid_chars:
#             if ch in name:
#                 return [False, f"Folder name {name} contains invalid character: {ch}"]

#         # 3. Reserved names
#         if name in [".", ".."]:
#             return [False, "Invalid folder name"]

#         # 4. Length check (optional but recommended)
#         if len(name) > 255:
#             return [False, f"Folder: {name} name too long"]

#         return [True, "Valid folder name",name]

#     @staticmethod
    
#     def getInput(message, inputType):
#         try:
#             user_input = input(message)

#             # Convert input to desired type
#             if inputType == int:
#                 return [True, int(user_input)]
#             elif inputType == float:
#                 return [True, float(user_input)]
#             elif inputType == str:
#                 return [True, user_input.strip()]
#             else:
#                 return [False, "Unsupported input type"]

#         except ValueError:
#             return [False, f"Invalid {inputType.__name__} value"]
#         except Exception as err:
#             return [False, str(err)]




#     def createFolder(self,name):
#         try:
            
#             validName = FileOrganizer.validateFolderName(name)
#             if not validName[0]:
#                 return validName
#             p = self.fileHandelingObj.getPath(validName[2])
#             if p.exists():
#                 return [False,f"Folder: {name} Exist"]
#             p.mkdir()
#             return [True,"Folder Created"]
#         except Exception as err:
#             return [False,str(err)]
        
#     def readFolderContent(self,name:str) -> list:
#         try:
#             validName = FileOrganizer.validateFolderName(name)
#             if not validName[0]:
#                 return validName
#             p = self.fileHandelingObj.getPath(validName[2])
#             if not p.exists():
#                 return [False,f"Folder: {name} Doesn't Exist"]
#             result = self.fileHandelingObj.getAllFilesAndFolder(p) # type: ignore
#             return result
            
#         except Exception as err:
#             return [False,str(err)]
    
#     def renameFolder(self,name:str,newName:str) -> list:
#         try:
#             validName = FileOrganizer.validateFolderName(newName)
#             if not validName[0]:
#                 return validName
#             p = self.fileHandelingObj.getPath(name)
#             if not p.exists():
#                 return [False,f"Folder: {name} Doesn't Exist"]
#             newP = self.fileHandelingObj.getPath(newName)
#             if newP.exists():
#                 return [False,f"Folder with name: {newName} already exist"]
            
#             p.rename(newP)
#             return [True,"Folder Successfully Renamed"]

            
#         except Exception as err:
#             return [False,str(err)]
        

#     def deleteFolder(self, name: str) -> list:
#         try:
#             p = self.fileHandelingObj.getPath(name)

#             if not p.exists():
#                 return [False, f"Folder: {name} Doesn't Exist"]

#             # Check content
#             result = self.fileHandelingObj.getAllFilesAndFolder(p) # type: ignore

#             # Folder NOT empty
#             if result[0] and result[1]:

#                 mode = FileOrganizer.getInput(
#                     f"Folder {name} contains files.\n"
#                     "Press 1 to delete everything OR 2 to cancel: ",
#                     int
#                 )

#                 if not mode[0]:
#                     return mode

#                 if mode[1] == 1:
#                     shutil.rmtree(p)
#                     return [True, f"Folder {name} deleted successfully"]

#                 return [False, f"Folder {name} not deleted"]

#             # Folder EMPTY → safe to delete
#             p.rmdir()
#             return [True, f"Folder {name} deleted successfully"]

#         except Exception as err:
#             return [False, str(err)]




#     def run(self):

#         while True:
#             result = self.fileHandelingObj.getAllFilesAndFolder()

#             if result[0] and result[1]:
#                 for i, item in enumerate(result[1]):
#                     print(f"{i+1} : {item}")

#             print("\n1 Create Folder\n2 Read Folder\n3 Rename Folder\n4 Delete Folder\n5 Exit")
#             choice = int(input("Selection: "))

#             match choice:
#                 case 1:
#                     name = input("Enter Folder Name to create: ")
#                     print(self.createFolder(name)[1])

#                 case 2:
#                     name = input("Enter Folder Name to read: ")
#                     result = self.readFolderContent(name)

#                     if result[0] and result[1]:
#                         for i, item in enumerate(result[1]):
#                             print(f"{i+1} : {item}")
#                     elif result[0]:
#                         print(f"Folder {name} is empty")
#                     else:
#                         print(result[1])

#                 case 3:
#                     name = input("Enter Folder Name you wish to rename: ")
#                     newName = input("Enter new name: ")
#                     print(self.renameFolder(name, newName)[1])

#                 case 4:
#                     name = input("Enter Folder Name you wish to delete: ")
#                     print(self.deleteFolder(name)[1])

#                 case 5:
#                     break

#                 case _:
#                     print("Invalid Choice")

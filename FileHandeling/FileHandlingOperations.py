import logging
from pathlib import Path


# -------------------------------------------------------------------------
# Ensure logs folder exists (Fix for missing log directory)
# -------------------------------------------------------------------------
# Get the absolute path to the project root (PYTHONPROJECTS folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_PATH = LOG_DIR / "fileHandeling.log"

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
logging.info("FileHandeling logger initialized successfully")
logging.info(f"Log file location: {LOG_PATH}")
logging.info("="*50)

class FileHandling:

    def __init__(self, base_path="./FileHandeling"):
        self.base_path = Path(base_path)
        Path(self.base_path).mkdir(exist_ok=True)
        logging.info(f"Base directory set to: {self.base_path}")

    def getPath(self, name=""):
        p = self.base_path / name #type: ignore
        logging.debug(f"getPath({name}) -> {p}")
        return p

    def getAllFilesAndFolder(self, myPath=""):
        """
        Returns list of files/folders.
        myPath can be:
        - "" -> base directory
        - Path object -> custom directory
        """
        try:
            if isinstance(myPath, str) and not myPath.strip():
                target = self.base_path
            elif isinstance(myPath, Path):
                target = myPath
            else:
                logging.warning("Invalid path type passed to getAllFilesAndFolder")
                return [False, "Invalid path type"]

            items = list(target.glob("*"))
            logging.info(f"Contents of {target}: {items}")
            return [True, items]

        except Exception as err:
            logging.error(f"Error in getAllFilesAndFolder: {err}")
            return [False, str(err)]

    def createNewFile(self, name, content=""):
        try:
            p = self.getPath(name)

            if p.exists():
                logging.warning(f"File already exists: {p}")
                return [False, "File already exists"]

            with open(p, "w") as fs:
                fs.write(content)

            logging.info(f"File created: {p}")
            return [True, "File created"]

        except Exception as err:
            logging.error(f"Error creating file {name}: {err}")
            return [False, str(err)]

    def readFile(self, name):
        try:
            p = self.getPath(name)

            if not p.exists():
                logging.warning(f"Tried reading nonexistent file: {name}")
                return [False, "File not found"]

            with open(p, "r") as fs:
                data = fs.read()

            logging.info(f"File read successfully: {name}")
            return [True, "Read success", data]

        except Exception as err:
            logging.error(f"Error reading file {name}: {err}")
            return [False, str(err)]

    def updateFile(self, name, mode, oldContent, newContent):
        try:
            p = self.getPath(name)

            if not p.exists():
                logging.warning(f"Update attempted on nonexistent file: {name}")
                return [False, "File not found"]

            with open(p, "r") as fs:
                data = fs.read()

            if mode == 1:
                if oldContent not in data:
                    logging.warning(f"Old content '{oldContent}' not found in {name}")
                    return [False, "Old text not found"]
                newData = data.replace(oldContent, newContent)
                with open(p, "w") as fs:
                    fs.write(newData)

            elif mode == 2:
                with open(p, "a") as fs:
                    fs.write(" " + newContent)

            elif mode == 3:
                with open(p, "w") as fs:
                    fs.write(newContent)

            elif mode == 4:
                with open(p, "w") as fs:
                    fs.write("")

            logging.info(f"File updated: {name}, mode: {mode}")
            return [True, "Update success"]

        except Exception as err:
            logging.error(f"Error updating file {name}: {err}")
            return [False, str(err)]

    def deleteTheFile(self, name):
        try:
            p = self.getPath(name)

            if not p.exists():
                logging.warning(f"Delete attempted on nonexistent file: {name}")
                return [False, "File not found"]

            p.unlink()
            logging.info(f"File deleted: {name}")
            return [True, "File deleted"]

        except Exception as err:
            logging.error(f"Error deleting file {name}: {err}")
            return [False, str(err)]

    def renameFile(self, name, newName):
        try:
            p = self.getPath(name)

            if not p.exists():
                logging.warning(f"Rename attempted on nonexistent file: {name}")
                return [False, "File not found"]

            newPath = self.getPath(newName)

            if newPath.exists():
                logging.warning(f"Rename failed; new name exists: {newName}")
                return [False, "New file already exists"]

            p.rename(newPath)

            logging.info(f"File renamed from {name} to {newName}")
            return [True, "Rename success"]

        except Exception as err:
            logging.error(f"Error renaming file {name}: {err}")
            return [False, str(err)]

    def createNewFolder(self, name):
        try:
            p = self.getPath(name)

            if p.exists():
                logging.warning(f"Folder already exists: {name}")
                return [False, "Folder already exists"]

            p.mkdir()
            logging.info(f"Folder created: {name}")

            return [True, "Folder created"]

        except Exception as err:
            logging.error(f"Error creating folder {name}: {err}")
            return [False, str(err)]

    # -------------------------------------------------------
    # RUN METHOD WITH LOGGING
    # -------------------------------------------------------
    def run(self):
        logging.info("Program started")

        while True:
            try:
                print("1 Create\n2 Read\n3 Update\n4 Delete\n5 Rename\n6 Exit")
                choice = int(input("Selection: "))
                logging.info(f"User selected: {choice}")

            except ValueError:
                print("Invalid input! Please enter a number.")
                logging.warning("Invalid non-numeric menu choice")
                continue

            except Exception as err:
                print(f"Unexpected error: {err}")
                logging.error(f"Unexpected error at menu selection: {err}")
                continue

            try:
                match choice:
                    case 1:
                        name = input("Enter filename: ")
                        content = input("Enter content: ")
                        logging.info(f"Create operation for: {name}")

                        result = self.createNewFile(name, content)
                        logging.info(f"Create result: {result}")

                        print(result[1])

                    case 2:
                        name = input("Enter filename: ")
                        logging.info(f"Read operation for: {name}")

                        result = self.readFile(name)
                        logging.info(f"Read result: {result}")

                        print(result[1] if not result[0] else result[2])

                    case 3:
                        name = input("File to update: ")
                        mode = int(input("Select Mode\n1 replace\n2 append\n3 overwrite\n4 clear\n"))
                        logging.info(f"Update requested: {name}, mode: {mode}")

                        oldVal = input("Old: ") if mode == 1 else None
                        newVal = input("New: ")

                        result = self.updateFile(name, mode, oldVal, newVal)
                        logging.info(f"Update result: {result}")

                        print(result[1])

                    case 4:
                        name = input("File to delete: ")
                        logging.info(f"Delete requested for: {name}")

                        result = self.deleteTheFile(name)
                        logging.info(f"Delete result: {result}")

                        print(result[1])

                    case 5:
                        name = input("Old name: ")
                        newName = input("New name: ")
                        logging.info(f"Rename requested: {name} → {newName}")

                        result = self.renameFile(name, newName)
                        logging.info(f"Rename result: {result}")

                        print(result[1])

                    case 6:
                        print("Exiting…")
                        logging.info("Program exited by user")
                        break

                    case _:
                        print("Invalid choice")
                        logging.warning(f"Invalid menu option selected: {choice}")

            except ValueError:
                print("Invalid data provided")
                logging.warning("ValueError in run operation")

            except Exception as err:
                print(f"Unexpected error occurred: {err}")
                logging.error(f"Unexpected error in operation: {err}")



# from pathlib import Path
# import os
# class FileHandling:

#     def __init__(self, base_path="./FileHandeling"):
#         self.base_path = base_path
#         Path(self.base_path).mkdir(exist_ok=True)

#     def getPath(self, name=""):
#         return Path(os.path.join(self.base_path, name))

#     def getAllFilesAndFolder(self,myPath = ""):
#         """
#         Returns list of files/folders.
#         myPath can be:
#         - "" -> base directory
#         - Path object -> custom directory
#         """

#         try:
#             # Case 1: Default → return items of base folder
#             if isinstance(myPath, str) and not myPath.strip():
#                 target = self.getPath()

#             # Case 2: User passes a Path object
#             elif isinstance(myPath, Path):
#                 target = myPath

#             else:
#                 return [False, "Invalid path type"]

#             items = list(target.glob("*"))
#             return [True, items]

#         except Exception as err:
#             return [False, str(err)]

#     def createNewFile(self, name, content=""):
#         try:
#             p = self.getPath(name)

#             if p.exists():
#                 return [False, "File already exists"]

#             with open(p, "w") as fs:
#                 fs.write(content)

#             return [True, "File created"]

#         except Exception as err:
#             return [False, str(err)]

#     def readFile(self, name):
#         try:
#             p = self.getPath(name)

#             if not p.exists():
#                 return [False, "File not found"]

#             with open(p, "r") as fs:
#                 data = fs.read()

#             return [True, "Read success", data]

#         except Exception as err:
#             return [False, str(err)]

#     def updateFile(self, name, mode, oldContent, newContent):
#         try:
#             p = self.getPath(name)

#             if not p.exists():
#                 return [False, "File not found"]

#             # Read old data
#             with open(p, "r") as fs:
#                 data = fs.read()

#             # Mode 1: replace
#             if mode == 1:
#                 if oldContent not in data:
#                     return [False, "Old text not found"]

#                 newData = data.replace(oldContent, newContent)

#                 with open(p, "w") as fs:
#                     fs.write(newData)

#             # Mode 2: append
#             elif mode == 2:
#                 with open(p, "a") as fs:
#                     fs.write(" " + newContent)

#             # Mode 3: overwrite
#             elif mode == 3:
#                 with open(p, "w") as fs:
#                     fs.write(newContent)

#             # Mode 4: clear
#             elif mode == 4:
#                 with open(p, "w") as fs:
#                     fs.write("")

#             return [True, "Update success"]

#         except Exception as err:
#             return [False, str(err)]

#     def deleteTheFile(self, name):
#         try:
#             p = self.getPath(name)

#             if not p.exists():
#                 return [False, "File not found"]

#             p.unlink()

#             return [True, "File deleted"]

#         except Exception as err:
#             return [False, str(err)]

#     def renameFile(self, name, newName):
#         try:
#             p = self.getPath(name)

#             if not p.exists():
#                 return [False, "File not found"]

#             newPath = self.getPath(newName)

#             if newPath.exists():
#                 return [False, "New file already exists"]

#             p.rename(newPath)

#             return [True, "Rename success"]

#         except Exception as err:
#             return [False, str(err)]

#     def createNewFolder(self, name):
#         try:
#             p = self.getPath(name)

#             if p.exists():
#                 return [False, "Folder already exists"]

#             p.mkdir()
#             return [True, "Folder created"]

#         except Exception as err:
#             return [False, str(err)]
#     def run(self):
#         while True:
#             try:
#                 print("1 Create\n2 Read\n3 Update\n4 Delete\n5 Rename\n6 Exit")
#                 choice = int(input("Selection: "))
#             except ValueError:
#                 print("Invalid input! Please enter a number.")
#                 continue
#             except Exception as err:
#                 print(f"Unexpected error: {err}")
#                 continue

#             try:
#                 match choice:
#                     case 1:
#                         name = input("Enter filename: ")
#                         content = input("Enter content: ")

#                         result = self.createNewFile(name, content)
#                         print(result[1])

#                     case 2:
#                         name = input("Enter filename: ")
#                         result = self.readFile(name)
#                         print(result[1] if not result[0] else result[2])

#                     case 3:
#                         name = input("File to update: ")
#                         mode = int(input("Enter Mode\n1 replace\n2 append\n3 overwrite\n4 clear\n"))
#                         oldVal = input("Old: ") if mode == 1 else None
#                         newVal = input("New: ")

#                         result = self.updateFile(name, mode, oldVal, newVal)
#                         print(result[1])

#                     case 4:
#                         name = input("File to delete: ")
#                         result = self.deleteTheFile(name)
#                         print(result[1])

#                     case 5:
#                         name = input("Old name: ")
#                         newName = input("New name: ")
#                         result = self.renameFile(name, newName)
#                         print(result[1])

#                     case 6:
#                         print("Exiting…")
#                         break

#                     case _:
#                         print("Invalid choice")

#             except ValueError:
#                 print("Invalid data provided")
#             except Exception as err:
#                 print(f"Unexpected error occurred: {err}")


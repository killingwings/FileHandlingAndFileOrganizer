# 📁 Python File Organizer & File Handling Utility

A simple and powerful **file organizer + file handling system** built in Python.

It provides a robust, log-enabled set of utilities for managing file systems, built around two core, interactive modules:
1.  **FileOrganizer:** For automated file sorting and folder management.
2.  **FileHandling:** For precise file-level CRUD operations.

## 🌟 Key Capabilities

| Feature | Description |
| :--- | :--- |
| **🧹 Auto-Organize** | Sorts files into category-wise folders (e.g., Images, Videos, Docs) based on a configurable JSON map. |
| **📝 File CRUD** | Create, Read, Update (Replace, Append, Overwrite, Clear), Rename, and Delete files. |
| **🗄 Folder Management** | Create, Read, Rename, and Safely Delete folders with content checks and validation. |
| **🪵 Logging** | Tracks all operations, errors, and warnings in dedicated log files (`fileHandeling.log`, `fileOrganizer.log`). |
| **🛡 Validation** | Strong input validation for folder names to prevent illegal characters and errors. |

---

## 🏷 Badges

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Repo Stars](https://img.shields.io/github/stars/killingwings/FileHandlingAndFileOrganizer?style=social)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/killingwings/FileHandlingAndFileOrganizer.git
```
### 2. Run the Interactive Utilities
| Utility            | Command                        | Description                                    |
| ------------------ | ------------------------------ | ---------------------------------------------- |
| **File Organizer** | `python FileOrganizer/main.py` | Run folder management & file organization menu |
| **File Handling**  | `python FileHandeling/main.py` | Run file-level CRUD operations menu            |

📂 Project Structure (Correct & Clean)
```
FileHandlingAndFileOrganizer/
│
├── FileHandeling/
│   ├── main.py                 # File handling engine (CRUD)
│   └── __init__.py
│
├── FileOrganizer/
│   ├── Organizer.py            # Folder organizer logic
│   ├── main.py                 # CLI entry for organizer
│   ├── __init__.py
│   └── fileExtensions.json     # Extension-category mapping
│
├── logs/
│   ├── fileHandeling.log
│   └── fileOrganizer.log
│
└── README.md
```
### 💡 Code Examples (API Usage)

#### ✔️ 1. Organizing a Folder


```bash
from FileOrganizer.Organizer import FileOrganizer

org = FileOrganizer("./FileOrganizer")
org.organizeMyFolder("", "fileExtensions.json")
```

#### ✔ 2. Creating a New File

```bash
from FileHandeling.main import FileHandling

fh = FileHandling("./FileHandeling")
success, message = fh.createNewFile("hello.txt", "Hi there!")

print(message)
```

### 📘 API Documentation

#### ▶ FileOrganizer (Organizer.py)

| Method                                            | Purpose                                                          |
| ------------------------------------------------- | ---------------------------------------------------------------- |
| `organizeMyFolder(folderName, extensionFileName)` | Organizes files into category folders based on the JSON mapping. |
| `getCategoryForFile(item)`                        | Returns extension-based category for a file.                     |
| `createFolder(name)`                              | Validates and creates a folder.                                  |
| `readFolderContent(name)`                         | Lists items in a folder.                                         |
| `deleteFolder(name)`                              | Deletes folder (safe for non-empty folders).                     |
| `renameFolder(name, newName)`                     | Renames a folder safely.                                         |

### ▶ FileHandling (main.py)

| Method                                           | Purpose                                                                |
| ------------------------------------------------ | ---------------------------------------------------------------------- |
| `createNewFile(name, content)`                   | Creates a file with content.                                           |
| `readFile(name)`                                 | Reads and returns file content.                                        |
| `updateFile(name, mode, oldContent, newContent)` | Updates file using: Replace (1), Append (2), Overwrite (3), Clear (4). |
| `renameFile(name, newName)`                      | Renames a file.                                                        |
| `deleteTheFile(name)`                            | Deletes a file.                                                        |

### 🤝 Contribution Guidelines

```
1. Fork this repository
2. Create a new branch: git checkout -b feature-name
3. Make your changes
4. Commit: git commit -m "Added new feature"
5. Push: git push origin feature-name
6. Open a Pull Request
```

### 📜 License

Licensed under the MIT License.

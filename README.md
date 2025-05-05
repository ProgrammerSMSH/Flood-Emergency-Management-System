# 🌊 Flood Emergency Management System

A command-line simulation for managing emergency resources and navigation during a flood crisis.  
Built in Python with dynamic suburb loading via JSON.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features
- Dynamic suburb loading and management
- Role-based access (admin/guest)
- Evacuation center details and navigation
- Command-line inventory management
- Take and drop resources (admin-only)
- Easy-to-follow interface for flood emergency management

## 📝 Prerequisites
- Python 3.6+
- pip package manager
- `suburbs.json` file with suburb data (see below for structure)

## 🛠️ Installation

### Option A: Clone using Git (if Git is installed)

1. Clone the repository:
    ```bash
    git clone https://github.com/ProgrammerSMSH/Flood-Emergency-Management-System.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Flood-Emergency-Management-System
    ```

### Option B: Manual Download (ZIP)

1. Download ZIP from GitHub:  
   [https://github.com/ProgrammerSMSH/Flood-Emergency-Management-System/archive/refs/heads/main.zip](https://github.com/ProgrammerSMSH/Flood-Emergency-Management-System/archive/refs/heads/main.zip)

2. Extract the ZIP file.

3. Open the extracted folder in terminal or command prompt.

## 🏁 Usage

1. Run the system:
    ```bash
    python main.py
    ```

2. Login credentials:
   - **Username:** admin  
   - **Password:** flood2024

3. After login, you will access commands based on your role.

## 💻 Commands

### 1. Take Resources
Take resources from the available stock:
```bash
take <resource_name> <quantity>
```
Example:
```bash
take sandbags 5
```

### 2. Move Direction
Navigate between locations:
```bash
go <direction>
```
Example:
```bash
go north
```

### 3. Check Inventory
See your current inventory:
```bash
inventory
```

### 4. Drop Resources
Drop some resources:
```bash
drop <resource_name> <quantity>
```
Example:
```bash
drop sandbags 3
```

### 5. Return to Headquarters
Shortcut to return:
```bash
go south
```

### 6. Exit
Exit the application:
```bash
exit
```

## 📧 Contact

- **Shakib Hossain**  
- 🌐 [www.shakib.me](https://www.shakib.me)  
- 📧 Email: contact@smshmail.com

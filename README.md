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
1. Clone the repository:
    ```bash
    git clone https://github.com/ProgrammerSMSH/Flood-Emergency-Management-System.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Flood-Emergency-Management-System
    ```

## 🏁 Usage
1. Run the system with:
    ```bash
    python main.py
    ```
2. On startup, you will be prompted for a login.  
   Enter the following credentials:
   - **Username:** admin  
   - **Password:** flood2024

3. After a successful login, you'll be granted access based on your role (admin or guest).

## 💻 Commands

### 1. Take Resources
Take resources from the available stock.
```bash
take <resource_name> <quantity>
```
Example:
```bash
take sandbags 5
```

### 2. Move Direction
Navigate between locations (north, south, east, west).
```bash
go <direction>
```
Example:
```bash
go north
```

### 3. Check Inventory
View the resources you have.
```bash
inventory
```

### 4. Drop Resources
Drop a specified quantity of resources.
```bash
drop <resource_name> <quantity>
```
Example:
```bash
drop sandbags 3
```

### 5. Return to Headquarters
Quickly return to the headquarters location.
```bash
go south
```

### 6. Exit
Exit the system.
```bash
exit
```

## 📧 Contact
- Shakib Hossain  
- 🌐 www.shakib.me  
- 📧 Email: contact@smshmail.com

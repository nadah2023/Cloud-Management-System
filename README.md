# Cloud-Management-System

## Overview
The **Cloud Management System** is a Python-based application that allows users to manage Virtual Machines (VMs) and Docker containers using a graphical user interface (GUI) built with `CustomTkinter`. It supports creating VMs using QEMU, managing Docker images, and performing various cloud-related operations efficiently.

## Prerequisites
Before running the application, ensure you have the following installed:

- **Python**: Installed and configured on your system.
- **Required Python Libraries**:
  ```sh
  pip install customtkinter CTkMessagebox
  ```
- **QEMU**: Ensure QEMU is installed and available in the system's PATH.
- **Docker**: Install Docker and ensure it is running.
- **Ubuntu ISO File**: Download `ubuntu-22.04.3-desktop-amd64.iso` from [Ubuntu's official website](https://ubuntu.com/download/desktop) and place it in the same directory as the project files.

## Installation
1. Clone the repository from GitHub:
   ```sh
   git clone https://github.com/your-username/cloud-management-system.git
   ```
2. Navigate to the project directory:
   ```sh
   cd cloud-management-system
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Ensure that **QEMU** and **Docker** are installed and running on your system.

## Usage
### Running the Application
To start the application, run:
```sh
python MainPage.py
```
This will open the **Cloud Management System** main interface.

### Features
1. **Create a Virtual Machine (VM)**
   - Click **Create a VM** on the main page.
   - Specify VM configurations (disk size, memory size, VM name) or upload a batch configuration file.
   - Click **Create VM** to set up the VM.
   - Success messages confirm VM creation.
  
     
  ![image](https://github.com/user-attachments/assets/b403db27-765f-4c35-b51e-61c8ec3d08a0)

  ![image](https://github.com/user-attachments/assets/9f46b563-cc7b-4da8-a626-b0c7cae367ea)
  
  ![image](https://github.com/user-attachments/assets/1c862fd4-20c5-4d56-b6d6-15b055eb4206)

2. **Manage Docker Containers**
   - Click **Docker Operations** to manage Docker images and containers.
   - Features include:
    
   ![image](https://github.com/user-attachments/assets/62a483bd-2a8c-44e2-9e71-a73a56be0c45)


## Installing Ubuntu from ISO
To install Ubuntu using the ISO file:
1. Download the `ubuntu-22.04.3-desktop-amd64.iso` from [Ubuntu's official site](https://ubuntu.com/download/desktop).
2. Use QEMU to create and boot a virtual machine with the ISO:
   ```sh
   qemu-system-x86_64 -boot d -cdrom ubuntu-22.04.3-desktop-amd64.iso -m 2048 -enable-kvm
   ```
3. Follow the on-screen instructions to install Ubuntu.




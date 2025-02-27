#VM page containing options for creating and running the VM

import subprocess, sys, re
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os

#function to go back to the Main page
def Back_Main():
    root.destroy()
    subprocess.call(["python", "MainPage.py"])

#function to go back to the VM menu page
def Back():
    root.destroy()
    subprocess.call(["python", "VM.py"])

#function to create the VM by taking user input
def VM_Manual():
    main_frame.pack_forget() #removing past frame

    manual_frame = ctk.CTkFrame(master=root) #creating new frame
    manual_frame.pack(pady=20, padx=20, fill="both", expand=True)

    #taking the image disk size
    disk_label = ctk.CTkLabel(manual_frame, text='\nEnter the disk image size', font=("Century", 20))
    disk_label.pack(padx=20, pady=10)
    disk_entry = ctk.CTkEntry(master=manual_frame, placeholder_text='10G, 5M, etc..', font=("Century", 15))
    disk_entry.pack(padx=10, pady=10)

    #taking the memory size of the VM
    memory_label = ctk.CTkLabel(manual_frame, text='Enter the memory size', font=("Century", 20))
    memory_label.pack(padx=10, pady=10)
    memory_size = ctk.CTkEntry(master=manual_frame, placeholder_text='2G, 2M, etc..', font=("Century", 16))
    memory_size.pack(padx=10, pady=10)

    #taking the VM name
    vm_name_label = ctk.CTkLabel(manual_frame, text='Enter the VM name', font=("Century", 20))
    vm_name_label.pack(padx=10, pady=10)
    vm_name_entry = ctk.CTkEntry(master=manual_frame, placeholder_text='my_vm, etc..', font=("Century", 15))
    vm_name_entry.pack(padx=10, pady=10)

    #function to run the QEMU commands to create a VM and run Ubuntu on it
    def Create_VM(DS, MS, VMN):
        disk_size = DS.get()
        memory_size = MS.get()
        vm_name = VMN.get()

        #Make sure no field is empty
        if not disk_size or memory_size or vm_name:
            CTkMessagebox(title="Error", message="Please make sure all required fields are filled.")
            return

        # Validate disk size format
        if not re.match(r'^\d+[M|G]$', disk_size):
            CTkMessagebox(title="Error", message="Invalid disk size format. Please use a valid format, e.g., '10G', '5M', etc.")
            return

        # Validate memory size format
        if not re.match(r'^\d+[M|G]$', memory_size):
            CTkMessagebox(title="Error", message="Invalid memory size format. Please use a valid format, e.g., '2G', '2M', etc.")
            return

        # Validate VM name
        if not re.match(r'^[a-zA-Z0-9_\-]+$', vm_name):
            CTkMessagebox(title="Error", message="Invalid VM name. Please use only alphanumeric characters, underscores, and hyphens.")
            return
        try:
            image_command = subprocess.Popen(["powershell.exe", f"qemu-img create -f qcow2 Image.img {disk_size}"], 
                stdout=sys.stdout)
            image_command.communicate()

            vm_command = subprocess.Popen(["powershell.exe", 
                f"qemu-system-x86_64 -name {vm_name} -accel whpx,kernel-irqchip=off -cdrom ubuntu-22.04.3-desktop-amd64.iso -boot menu=on -drive file=Image.img -m {memory_size}"], 
                stdout=sys.stdout)
            vm_command.communicate()
            CTkMessagebox(title="Success", message="Virtual Machine created successfully.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    #creating buttons to call the create VM function and back to VM menu function respectively
    enter_button = ctk.CTkButton(master=manual_frame, text="Create VM", font=("Century", 20), command=lambda: Create_VM(disk_entry,memory_size,vm_name_entry))
    enter_button.pack(pady=25, padx=10, ipadx=30,ipady=10)
    back_button = ctk.CTkButton(master=manual_frame, text="Back", font=("Century", 15), command=Back)
    back_button.pack(pady=10, padx=5, side='left')

#function to create a VM using a batch file
def VM_Config():
    main_frame.pack_forget()

    config_frame = ctk.CTkFrame(master=root)
    config_frame.pack(pady=20, padx=20, fill="both", expand=True)

    #getting batch file path from user
    file_path_label = ctk.CTkLabel(master=config_frame, text="\n\n\n\n\n\nPlease enter the name of the batch configuration file with it's path\nNote: The disk image size limit is 20G.",
                font=("Century", 20))
    file_path_label.pack(padx=10, pady=15)
    file_path_entry = ctk.CTkEntry(master=config_frame, placeholder_text='Desktop/configFolder/myvm_config.bat, etc..', font=("Century", 10))
    file_path_entry.pack(padx=10, pady=10, ipadx=110,ipady=5)

    #function to read batch file and run it
    def Read_Config():
        Path = file_path_entry.get()
        file_name = os.path.basename(Path)

        # Check if the file name has an extension
        if not '.' in file_name:
            CTkMessagebox(title="Error", message="Invalid file path. Please provide a path with a valid file name and extension.")
            return

        #Check if the specified path exists
        if not os.path.exists(os.path.dirname(Path)):
            CTkMessagebox(title="Error", message="The specified path does not exist.")
            return
        
        # Check if the file has the correct extension (e.g., .bat)
        if not Path.lower().endswith('.bat'):
            CTkMessagebox(title="Error", message="Invalid file format. Please select a valid batch (.bat) file.")
            return
        
        # Check if the specified path is a file
        if not os.path.isfile(Path):
            CTkMessagebox(title="Error", message="The specified path does not point to a valid file.")
            return
        try:
            vm_command = subprocess.Popen(["powershell.exe", f"Start-Process -FilePath {Path} -NoNewWindow -Wait"], stdout=sys.stdout)
            vm_command.communicate()
            CTkMessagebox(title="Success", message="Virtual Machine created successfully.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    #creating buttons for calling the read config function and back to VM menu page function
    create_button = ctk.CTkButton(config_frame,text="Create VM", font=("Century", 15), command=Read_Config)
    create_button.pack(pady=20, padx=10)
    back_button = ctk.CTkButton(master=config_frame, text="Back", font=("Century", 15), command=Back)
    back_button.pack(pady=10, padx=5, side='left')

#########################################################################################################################

#setting the color and theme of the window
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("dark-blue")  

#creating root object and assigning title, icon, and size
root = ctk.CTk()
root.wm_title('Cloud System')
root.wm_iconbitmap("cloud.ico")
root.geometry("700x500")
root.resizable(True, True)

#creating main frame of the window
main_frame = ctk.CTkFrame(master=root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

#creating title and choose label
title_label = ctk.CTkLabel(master=main_frame, text="Creating a Virtual Machine", font=("Century", 40))
title_label.pack(pady=55, padx=10)
choose_label = ctk.CTkLabel(master=main_frame, text="Please choose one of the following", font=("Century", 25))
choose_label.pack(pady=12, padx=10)

#creating buttons that call each predefined functions above
vm_manual_button = ctk.CTkButton(master=main_frame, text="Enter VM Specifications Manually", font=("Century", 20), command=VM_Manual)
vm_manual_button.pack(pady=20, padx=5, ipadx=23,ipady=15)
vm_config_button = ctk.CTkButton(master=main_frame, text="Upload VM Configuration File", font=("Century", 20), command=VM_Config)
vm_config_button.pack(pady=20, padx=5,ipadx=57,ipady=15)

back_main_button = ctk.CTkButton(main_frame, text='Back to Main', font=("Century", 15), command=Back_Main)
back_main_button.pack(pady=10, padx=5, side='left')

#start executing the application
root.mainloop()
#Main page for our cloud system application

import customtkinter as ctk
import subprocess

#function to open the VM page
def VMPage():
    root.destroy()
    subprocess.call(["python", "VM.py"])

#function to open the Docker operations page
def DockerPage():
    root.destroy()
    subprocess.call(["python", "DockerOper.py"])

#setting the color and theme of the window
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("dark-blue")  

#creating root object and assigning title, icon, and size
root = ctk.CTk()
root.wm_title('Cloud System')
root.wm_iconbitmap('cloud.ico')
root.geometry("700x500")
root.resizable(True, True)

#creating main frame of the window
main_frame = ctk.CTkFrame(master=root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

#creating title and choose label
title_ = ctk.CTkLabel(master=main_frame, text="Cloud Management System", font=("Century", 40))
title_.pack(pady=55, padx=10)
choose_label = ctk.CTkLabel(master=main_frame, text="Please choose one of the following options", font=("Century", 25))
choose_label.pack(pady=22, padx=10)

#creating buttons that call each predefined functions above
vm_button = ctk.CTkButton(master=main_frame, text="Create a VM", font=("Century", 20), command=VMPage)
vm_button.pack(pady=10, padx=10, ipadx=50,ipady=25)
docker_button = ctk.CTkButton(master=main_frame, text="Docker Operations", font=("Century", 20), command=DockerPage)
docker_button.pack(pady=10, padx=10,ipadx=10,ipady=25)

#start executing the application
root.mainloop()
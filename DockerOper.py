import customtkinter as ctk
from tkinter import scrolledtext, Listbox
from CTkMessagebox import CTkMessagebox
import docker
import os
import subprocess
import requests


# Create a Docker client
client = docker.from_env()

def Back_Main():
    root.destroy()
    subprocess.call(["python", "MainPage.py"])

def Back():
     root.destroy()
     subprocess.call(["python", "DockerOper.py"])

# Create the Dockerfile creation window
def Create_Dockerfile():
    main_frame.pack_forget()

    dockerfile_frame = ctk.CTkFrame(master=root)
    dockerfile_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Ask the user for the path to save the Dockerfile and the contents of the Dockerfile
    path_label = ctk.CTkLabel(dockerfile_frame, text="\nEnter the path to save the Dockerfile", font=("Century", 15))
    path_label.pack(pady=5)

    path_entry = ctk.CTkEntry(dockerfile_frame)
    path_entry.pack(ipadx=110)

    contents_label = ctk.CTkLabel(dockerfile_frame, text="Enter the contents of the Dockerfile",font=("Century", 15))
    contents_label.pack()

    contents_entry = ctk.CTkTextbox(dockerfile_frame)
    contents_entry.pack(ipady=70, ipadx=120)

    # Write the contents to the Dockerfile at the specified path
    def Write_Dockerfile():
        path = path_entry.get()
        contents = contents_entry.get("0.0","end")

        if not os.path.exists(os.path.dirname(path)):
            CTkMessagebox(title="Error", message="The specified path does not exist.")
            return
        
        if contents_entry.get("1.0", "end")=="\n":
            CTkMessagebox(title="Error", message="The Dockerfile content cannot be empty.")
            return
        
        if not path.endswith('\\Dockerfile'):
            CTkMessagebox(title="Error", message="Please append \\Dockerfile to the path.")
            return

        try:
            with open(path, 'w') as file:
                file.write(contents)
            CTkMessagebox(title="Success", message="Dockerfile created successfully.")
        except Exception as e:
            CTkMessagebox(title="Error", message="There was an error creating the Dockerfile: " + str(e))

    write_button = ctk.CTkButton(dockerfile_frame, text="Write Dockerfile", command=Write_Dockerfile, font=("Century", 15))
    write_button.pack(pady=5)

    back_button = ctk.CTkButton(dockerfile_frame, text="Back", command=Back, font=("Century", 15))
    back_button.pack(side='left', padx=5)

# Create the Docker image building window
def Build_Docker_Image():
    main_frame.pack_forget()

    image_frame = ctk.CTkFrame(master=root)
    image_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Ask the user for the Dockerfile to use and the image name/tag
    dockerfile_label = ctk.CTkLabel(image_frame, text="\n\n\n\n\nEnter the path to the Dockerfile", font=("Century", 20))
    dockerfile_label.pack(pady=15)

    dockerfile_entry = ctk.CTkEntry(image_frame)
    dockerfile_entry.pack(ipadx=110)

    image_label = ctk.CTkLabel(image_frame, text="Enter the image name/tag", font=("Century", 20))
    image_label.pack(pady=15)

    image_entry = ctk.CTkEntry(image_frame)
    image_entry.pack()

    # Build the Docker image
    def Build_Image():
        dockerfile_path = dockerfile_entry.get()
        image_name = image_entry.get()
        
        if not os.path.exists(os.path.dirname(dockerfile_path)):
            CTkMessagebox(title="Error", message="The specified path does not exist.")
            return

        try:
            image, build_logs = client.images.build(path=dockerfile_path, tag=image_name)
            CTkMessagebox(title="Success", message="Docker image built successfully.")
            for log in build_logs:
                print(log)
        except docker.errors.DockerException as e:
            CTkMessagebox(title="Error", message="There was an error building the Docker image: " + str(e))
        except docker.errors.BuildError as e:
            CTkMessagebox(title="Error", message="There was an error building the Docker image: " + str(e))

    build_button = ctk.CTkButton(image_frame, text="Build Image", command=Build_Image, font=("Century", 15))
    build_button.pack(pady=15)

    back_button = ctk.CTkButton(image_frame, text="Back", command=Back, font=("Century", 15))
    back_button.pack(pady=5, padx=5, side='left')

# Function to check if Docker is installed and running
def check_docker_installation():
    try:
        subprocess.check_output(["docker", "--version"])
    except subprocess.SubprocessError:
        CTkMessagebox("Error", "Docker is not installed or not accessible. Please check your Docker installation.")
        return False
    try:
        subprocess.check_output(["docker", "info"])
    except subprocess.SubprocessError:
        CTkMessagebox("Error", "Docker daemon is not running. Please start Docker.")
        return False
    return True

# Function to list docker images
def List_Docker_Images():
    if not check_docker_installation():
        return
    try:
        result = subprocess.check_output(["docker", "images"])
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return "Failed to list Docker images: " + e.output.decode('utf-8')

# Function to list running containers
def List_Running_Containers():
    if not check_docker_installation():
        return
    try:
        result = subprocess.check_output(["docker", "ps"])
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return "Failed to list running containers: " + e.output.decode('utf-8')


# Function to update the output in the text area
def Update_Output(command):
    if command == 'images':
        output = List_Docker_Images()
    elif command == 'containers':
        output = List_Running_Containers()

    # Frame for text area
    text_frame = ctk.CTkToplevel(root)
    text_frame.title('Cloud System')
    text_frame.geometry("750x300") # Set the window size
    text_frame.resizable(True, True) # Prevent the window from being resized

    # Add a text area to display output
    text_area = scrolledtext.ScrolledText(text_frame, wrap='word', width=100, height=20, font=("Consolas", 15))
    text_area.configure(state='disabled')  # Text area styling
    text_area.pack(padx=10, pady=10, fill='both', expand=True)

    text_area.configure(state='normal')
    text_area.delete('1.0', ctk.END)
    text_area.insert(ctk.INSERT, output)
    text_area.configure(state='disabled')

def Stop_Container():
    main_frame.pack_forget()

    stop_container_frame = ctk.CTkFrame(master=root)
    stop_container_frame.pack(pady=20, padx=20, fill="both", expand=True)

    container_label = ctk.CTkLabel(stop_container_frame, text="\n\n\n\n\n\nEnter Container name", font=("Century", 20))
    container_label.pack(pady=10)

    container_entry = ctk.CTkEntry(stop_container_frame)
    container_entry.pack()

    def Stop(container_name):
        #connect python with Docker
        Docker = docker.from_env()
        #list all containers
        all_containers = Docker.containers.list(all=True)
        
        container_found = False
        
        #loop over all the containers to find the specified container
        for container in all_containers:
            if container.name == container_name:
                container_found = True    #change the flag to true as the container is found
                if container.status == 'running':
                    
                    container.stop()  #stop the container
                    CTkMessagebox(title='success', message= f"Container '{container_name}' has been stopped.\n\n")
                    break
                else:  # the container is already not running
                    CTkMessagebox(title='inform', message=f"Container '{container_name}' is already not running.\n\n")
                    break
        
        if not container_found:
            # container is not found
            CTkMessagebox(title='Error', message= f"Container '{container_name}' not found.\n\n")

    #function to check that the user enters valid input
    def Validate_Input(): 
        container_name = container_entry.get()
        if ' ' in container_name:
            CTkMessagebox(title="Error", message="Invalid input. Container name cannot contain spaces.")
            
        elif container_name.isdigit():
            CTkMessagebox(title="Error", message= "Invalid input. Container name should not be numbers only.")
            
        elif  container_name[0].isdigit():
            CTkMessagebox(title="Error", message="Invalid input. Container name should start with a letter.")
        
        else:
            Stop(container_name)

    stop_container_button = ctk.CTkButton(stop_container_frame, text="Stop Container", command=Validate_Input, font=("Century", 15))
    stop_container_button.pack(pady=15)

    back_button = ctk.CTkButton(stop_container_frame, text="Back", command=Back, font=("Century", 15))
    back_button.pack(pady=15, padx=5, side='left')
def Search_Docker_Images():
    main_frame.pack_forget()

    search_image_frame = ctk.CTkFrame(master=root)
    search_image_frame.pack(pady=20, padx=20, fill="both", expand=True)  

    search_label = ctk.CTkLabel(search_image_frame, text="\n\n\n\n\n\nEnter Docker image name", font=("Century", 20))
    search_label.pack(pady=10)

    search_entry = ctk.CTkEntry(search_image_frame)
    search_entry.pack()

    def Search_Images(image_name):
        #connect python with docker
        Docker = docker.from_env()
        all_images = Docker.images.list(all=True)  #list all the images
        
        image_found = False
        
        for img in all_images:  #loop over all images
            for tag in img.tags:
                if tag == image_name:
                    image_found = True
                    CTkMessagebox(title='Success', message=f"Found matching images for '{image_name}':\nImage ID: {img.id}, Tags: {', '.join(img.tags)}")
                    break  # Exit the inner loop if a match is found
            if image_found:
                break  # Exit the outer loop if a match is found
        
        if not image_found: #if the image is not found
            CTkMessagebox(title='Error', message=f"No matching images found for '{image_name}'\n\n")

    #check that the user enters a valid inputs
    def Validate_Input():
        image_name = search_entry.get()
        if ' ' in image_name:
            CTkMessagebox(title="Error", message="Invalid input. Docker image name cannot contain spaces.")
        
        elif image_name.isdigit():
            CTkMessagebox(title="Error", message= "Invalid input. Docker image name should not be numbers only.")
        
        elif  image_name[0].isdigit():
            CTkMessagebox(title="Error", message="Invalid input. Docker image name should start with a letter.")
            
        else:
            Search_Images(image_name)

    search_button = ctk.CTkButton(search_image_frame, text="Search", command=Validate_Input, font=("Century", 15))
    search_button.pack(pady=15)

    back_button = ctk.CTkButton(search_image_frame, text="Back", command=Back, font=("Century", 15))
    back_button.pack(pady=5, padx=5, side='left')

def DockerHub():
    DOCKER_HUB_SEARCH_API = "https://hub.docker.com/v2/search/repositories/"

    main_frame.pack_forget()
    dockerhub_frame = ctk.CTkFrame(master=root)
    dockerhub_frame.pack(pady=20, padx=20, fill="both", expand=True)

    dockerhub_label = ctk.CTkLabel(dockerhub_frame, text="\nSearch and Pull Docker Image", font=("Century", 20))
    dockerhub_label.pack(pady=10)

    dockerhub_search_entry = ctk.CTkEntry(dockerhub_frame, width=40)
    dockerhub_search_entry.pack(pady=5,ipadx=100)

    def Search_DockerHub_Images():
        search_term = dockerhub_search_entry.get().strip()
        if not search_term:
            CTkMessagebox(title="Search Result", message="Please enter a search term.")
            return

        search_results = Search_On_DockerHub(search_term)
        if search_results:
            Show_Nearest_Images(search_results)
        else:
            CTkMessagebox(title="Search Result", message="No results found.")

    def Search_On_DockerHub(search_term):
        try:
            response = requests.get(DOCKER_HUB_SEARCH_API, params={"query": search_term})
            response.raise_for_status()
            data = response.json()
            if "results" in data and data["results"]:
                return [result for result in data["results"]]
        except requests.RequestException as e:
            print(f"Error during Docker Hub search: {e}")
        return None

    def Show_Nearest_Images(results):
        dockerhub_nearest_images_listbox.delete(0, ctk.END)
        for result in results:
            image_name = result.get("name") or result.get("repo_name", "")
            dockerhub_nearest_images_listbox.insert(ctk.END, image_name)

    def Pull_Selected_Image():
        selected_index = dockerhub_nearest_images_listbox.curselection()
        if not selected_index:
            CTkMessagebox(title="Pull Image", message="Please select an image to pull.")
            return

        # Convert selected_index to int
        selected_index = int(selected_index[0])

        selected_image = dockerhub_nearest_images_listbox.get(selected_index)
        
        input_dialog = ctk.CTkInputDialog(title="Image Tag", text=f"Enter tag for image {selected_image}", font=("Century", 15))
        image_tag = input_dialog.get_input()

        if not image_tag:
            CTkMessagebox(title="Pull Image", message="Please enter a tag for the image.")
            return

        full_image_name = f"{selected_image}:{image_tag}"

        try:
            client = docker.from_env()
            client.images.pull(full_image_name)
            print(f"Image {full_image_name} pulled successfully.")

            CTkMessagebox(title="Success", message=f"Image {full_image_name} pulled successfully.")
        except docker.errors.APIError as e:
            CTkMessagebox(title="Error", message=f"Failed to pull image: {e}")
            print(f"Failed to pull image: {e}")


    dockerhub_search_button = ctk.CTkButton(dockerhub_frame, text="Search Image", command=Search_DockerHub_Images, font=("Century", 15))
    dockerhub_search_button.pack(pady=5)

    dockerhub_nearest_images_listbox = Listbox(dockerhub_frame, selectmode=ctk.SINGLE, height=10, width=50,font=("Century", 20))
    dockerhub_nearest_images_listbox.pack()

    pull_button = ctk.CTkButton(dockerhub_frame, text="Pull Selected Image", command=Pull_Selected_Image, font=("Century", 15))
    pull_button.pack(pady=10)

    back_button = ctk.CTkButton(dockerhub_frame, text="Back", command=Back,font=("Century", 10))
    back_button.pack(pady=5, padx=5, side='left')

###########################################################################################################################################################

ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("dark-blue") 

# Create the main application window
root = ctk.CTk()
root.wm_title('Cloud System')
root.wm_iconbitmap('cloud.ico')
root.geometry("700x500") # Set the window size
root.resizable(True, True) # Prevent the window from being resized

# Frame for buttons
main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

choose_label = ctk.CTkLabel(master=main_frame, text="Please Choose One of the Following Options", font=("Century", 25))
choose_label.pack(pady=30, padx=60)

# Create buttons to open the Dockerfile creation and image building windows
create_dockerfile_button = ctk.CTkButton(main_frame, text="Create Dockerfile", command=Create_Dockerfile,font=("Century", 20))
create_dockerfile_button.pack(padx=10, pady=5, ipadx=57, ipady=5)

build_docker_image_button = ctk.CTkButton(main_frame, text="Build Docker Image", command=Build_Docker_Image,font=("Century", 20))
build_docker_image_button.pack(padx=10, pady=5, ipadx=39, ipady=5)

# Add buttons
list_images_button = ctk.CTkButton(main_frame, text="List Docker Images", command=lambda: Update_Output('images'),font=("Century", 20))
list_images_button.pack(padx=10, pady=5, ipadx=43, ipady=5)

list_containers_button = ctk.CTkButton(main_frame, text="List Running Containers", command=lambda: Update_Output('containers'),font=("Century", 20))
list_containers_button.pack(padx=10, pady=5, ipady=5)

stop_container_button = ctk.CTkButton(main_frame, text="Stop Docker Container", command=Stop_Container,font=("Century", 20))
stop_container_button.pack(padx=10, pady=5, ipady=5,ipadx=15)

search_image_button = ctk.CTkButton(main_frame, text="Search Docker Image", command=Search_Docker_Images,font=("Century", 20))
search_image_button.pack(padx=10, pady=5, ipady=5, ipadx=27)

dockerhub_button = ctk.CTkButton(main_frame, text="DockerHub Operations", command=DockerHub,font=("Century", 20))
dockerhub_button.pack(padx=10, pady=5, ipady=5, ipadx=16)

back_main_button = ctk.CTkButton(main_frame, text='Back to Main', font=("Century", 15), command=Back_Main)
back_main_button.pack(pady=5, padx=5, side='left')

# Start the GUI event loop
root.mainloop()
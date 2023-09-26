# 
# Author: Jose Lo Huang
# Creation Date: 20/12/2020
# Updates:
# 21/12/2020 - Add function calls and add comments
# 03/01/2021 - Add more functions for tkinter management
# 
# This code is to maintain all the management menus in the same place.
# From this code, the specific Docker tasks are triggered.
# 

import Docker
import Error
import tkinter as tk
from tkinter import *

# Instantiate the Error class
error = Error.Error()

# Instantiate the Docker class
docker = Docker.Docker()

# Instatiate the tkinter class for root menu
root = tk.Tk()
v = tk.IntVar()

# Global variable to choose container for docker actions
image_name = ""

# Global variable to choose container for docker actions
container_name = ""

# Global variable to choose the python script to execute on a container
python_script = ""

# Global variable to choose the python script version to execute on a container
python_version = ""

def task_finished ():
    #
    # This method prints a message after the completion of each task
    # 
    print("******************************************************************")
    print("Task completed. Please, choose your next task in the window.      ")
    print("******************************************************************")


def get_version ():
    # 
    # Get version menu:
    # This function request the script version to run on the container.
    #
    try:

        # Show the python script
        versions = ["Python 2.7","Python 3.8"]
        options = []
        for i in range(len(versions)):
            options.append((versions[i],i+1))

        # Create the new window
        version_list = Toplevel()
        version_option = StringVar()

        # Set the window title
        version_list.title("***** VERSION TO USE *****")

        # Set the window label
        tk.Label(version_list, text="""Please insert the script version to use and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Wrap all the containers and values in tuples and show them
        for option, val in options:
            tk.Radiobutton(version_list, 
                       text=option,
                       padx = 20, 
                       variable=version_option,
                       value=val).pack(anchor=tk.W)

        def version_clicked ():
            # 
            # This function will store the version chosen on the global variable
            # and destroy the top level window.
            #
            global python_version
            
            python_version = versions[int(version_option.get())-1]
            print(python_version)
            version_list.destroy()
            version_list.quit()
            version_list.update()

        # Show the Execute button
        btn = tk.Button(version_list, text="EXECUTE", fg='green', command=version_clicked).pack()
        
        # Wait for user input
        version_list.mainloop()
        
    except:
        error.general_error("creating the version menu")  


def get_script ():
    # 
    # Get script menu:
    # This function request the script name to run on the container.
    #
    try:
        
        name_list = Toplevel()
        name_option = StringVar()

        # Set the window title
        name_list.title("***** SCRIPT TO USE *****")

        # Set the window label
        tk.Label(name_list, text="""Please insert the script name to use and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Create the entry box
        entry = tk.Entry(name_list)        
        entry.pack()

        def name_clicked ():
            # 
            # This function will store the image chosen on the global variable
            # and destroy the top level window.
            #
            global python_script
            python_script = str(entry.get())
            name_list.destroy()
            name_list.quit()
            name_list.update()

        # Create the Execute button
        btn = tk.Button(name_list, text="EXECUTE", fg='green', command=name_clicked).pack()
        
        # Wait for user input
        name_list.mainloop()
        
    except:
        error.general_error("creating the get script menu")  


def get_image ():
    # 
    # Get image menu:
    # This function request the user image to run the container.
    #
    try:
        
        image_list = Toplevel()
        image_option = StringVar()

        # Set the window title
        image_list.title("***** IMAGE TO USE *****")

        # Set the window label
        tk.Label(image_list, text="""Please insert the image name to use and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Create the entry box
        entry = tk.Entry(image_list)        
        entry.pack()

        def image_clicked ():
            # 
            # This function will store the image chosen on the global variable
            # and destroy the top level window.
            #
            global image_name
            image_name = str(entry.get())
            print(image_name)
            image_list.destroy()
            image_list.quit()
            image_list.update()

        # Create the Execute button
        btn = tk.Button(image_list, text="EXECUTE", fg='green', command=image_clicked).pack()
        
        # Wait for user input
        image_list.mainloop()
        
    except:
        error.general_error("creating the get image menu")  



def get_container ():
    # 
    # Get container menu:
    # This function shows the containers and request the user option.
    #
    try:

        global docker

        # Get the container list
        containers = docker.list_containers()
        options = []
        for i in range(len(containers)):
            options.append((containers[i],i+1))

        # If there are no containers.
        if len(options) == 0:
            print("******************************************************************")
            print(" THERE ARE NO CONTAINERS! CREATE ONE FIRST. >>>>>>>>>>>>>>>>>>>>> ")
            print("******************************************************************")
            return

        container_list = Toplevel()
        container_option = IntVar()

        # Set the window title
        container_list.title("***** ALL CONTAINERS *****")

        # Set the window label
        tk.Label(container_list, text="""Please select the container and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Wrap all the containers and values in tuples and show them
        for option, val in options:
            tk.Radiobutton(container_list, 
                       text=option,
                       padx = 20, 
                       variable=container_option,
                       value=val).pack(anchor=tk.W)

        def container_clicked ():
            # 
            # This function will store the pod name chosen on the global variable
            # and destroy the top level window.
            #
            global container_name
            
            container_name = containers[int(container_option.get())-1]
            print(container_name)
            container_list.destroy()
            container_list.quit()
            container_list.update()

        # Show the Execute button
        btn = tk.Button(container_list, text="EXECUTE", fg='green', command=container_clicked).pack()
        
        # Wait for user input
        container_list.mainloop()
        
    except:
        error.general_error("creating the container menu")  


def router ():
    # 
    # Router menu:
    # This procedure is in charge of route the user to the different docker functions
    # depending on the chosen options.
    #
    global docker
    global image_name
    global container_name
    global python_script
    global python_version
    
    option = str(v.get())
    print()
    # List all containers
    if (option == "1"):
        print("******************************************************************")
        print(" ALL CONTAINERS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        docker.list_containers()
        task_finished()
    # Run a container
    elif (option == "2"):
        print("******************************************************************")
        print(" RUN CONTAINER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        get_image()
        docker.run_container(image_name)
        task_finished()
    # Stop a container
    elif (option == "3"):
        print("******************************************************************")
        print(" STOP CONTAINER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        get_container()
        if container_name == "":
            pass
        else:
            docker.stop_container(container_name)
        task_finished()
    # Remove all stopped/exited containers
    elif (option == "4"):
        print("******************************************************************")
        print(" REMOVE CONTAINER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        docker.remove_stopped_containers()
        task_finished()
    # Run a python script on a container
    elif (option == "5"):
        print("******************************************************************")
        print(" RUN PYTHON SCRIPT ON A CONTAINER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        # Get the script name
        files = docker.list_files()
        get_script()
        if python_script not in files:
            error.not_valid_value(python_script)
            task_finished()
            return
        # Get the python version ["Python 2.7","Python 3.8"]
        get_version()
        if python_version == "Python 2.7":
            docker.python_container(python_script, "2")
        elif python_version == "Python 3.8":
            docker.python_container(python_script, "3")
        task_finished()
    # Run a docker compose example
    elif (option == "6"):
        print("******************************************************************")
        print(" RUN DOCKER COMPOSE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        docker.docker_compose()
        task_finished()
    # Exit program
    elif (option == "7"):
        del docker
        root.destroy()
        print("******************************************************************")
        print("Program completed. Close all the windows to finish.               ")
        print("******************************************************************")
    else:
        print(option)
        error.not_valid_value(option)
    return


def menu ():
    # 
    # Main Menu:
    # This function shows the main menu and request the user option.
    #
    try:

        # Set main window titkle
        root.title("***** DOCKER MENU *****")

        # Set main window label
        tk.Label(root, text="""DOCKER MANAGER V2.0. Author: Jose Lo Huang.\nPlease select the action to execute and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        options = [("1. List all containers", 1),
                   ("2. Run a container", 2),
                   ("3. Stop a container", 3),
                   ("4. Remove all stopped/exited containers", 4),
                   ("5. Run a python script on a container", 5),
                   ("6. Use docker compose", 6),
                   ("7. Exit", 7)]

        # Create radio buttons for each option in the main menu
        for option, val in options:
            tk.Radiobutton(root, 
                       text=option,
                       padx = 20, 
                       variable=v,
                       value=val).pack(anchor=tk.W)

        # Show the main menu
        btn = tk.Button(root, text="EXECUTE", fg='green', command=router).pack()

        # Wait for user input
        root.mainloop()
        
    except:
        error.general_error("creating the menu")








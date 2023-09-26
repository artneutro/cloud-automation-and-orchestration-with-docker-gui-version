# 
# Author: Jose Lo Huang
# Creation Date: 21/12/2020
# Updates:
# 03/01/2021 - Minor fixes
# 
# This code is to define the Docker class
#


import os
import time
import docker
import Error


class Docker:
    # 
    # The Docker class will manage the docker tasks
    # 

    def __init__ ( self ):
        #
        # It will instantiates a client of the docker class
        # Also, a instantiation of Error class for error messages
        # 
        self.client = docker.from_env()
        self.error = Error.Error()


    def list_containers ( self ):
        #
        # This function will list all the containers including the exited and stopped ones.
        # Returns a list with all the containers in running state.
        # 
        try:
            print ('{0:^67s} {1:<24s} {2:>10s}'.format("CONTAINER ID", "NAME", "STATUS"))

            containers = []
            for container in self.client.containers.list("all"):
                if container.status == 'running':
                    containers.append(container.id)
                print ('{0:<67s} {1:<24s} {2:>10s}'.format(container.id, container.name, container.status))
            return containers
        except:
            self.error.general_error("listing the containers")


    def run_container ( self , image ):
        # 
        # This function receives an image as input and creates a container with it.
        # Input: The docker image ID
        # 
        try:
            container = self.client.containers.run(image, detach=True, tty=True)
            print("**************************** RUNNING *******************************")
            time.sleep(10)
            print("****** OUTPUT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(container.logs())
        except docker.errors.ContainerError:
            self.error.error_containers("running") 
        except docker.errors.ImageNotFound:
            print ("The image specified doesn't exists.")
        except docker.errors.APIError:
            self.error.error_containers("running")
        except:
            self.error.general_error("running the containers")


    def stop_container ( self , container_id ):
        #
        # This function request a container ID and stop the container.
        # Input: Container ID
        # 
        try:
            container = self.client.containers.get(container_id)
            print("**************************** STOPPING ******************************")
            container.stop()
        except docker.errors.APIError:
            self.error.error_containers("stopping")
            print("Check if the container ID exists.")
        except:
            self.error.general_error("stopping the containers")


    def remove_stopped_containers ( self ):
        #
        # This functions removes all the stopped/exited containers.
        # 
        try:
            print("**************************** REMOVING ******************************")
            containers = self.client.containers.prune()
            for container in containers['ContainersDeleted']:
                print (container)
        except docker.errors.APIError:
            self.error.error_containers("removing")
        except:
            self.error.general_error("removing the containers")


    def list_files ( self ):
        #
        # This function lists all the *.py files on the current directory.
        # 
        try:
            py_files = []
            print("******************************************************************")
            print("Listing *.py files: ")
            print("******************************************************************")
            os.system('ls -l *.py | awk \'{print $9}\'')
            for i in os.popen('ls -l *.py | awk \'{print $9}\'').read().split('\n'):
                py_files.append(i)
            return py_files[:-1]
        except:
            print("Error while listing the files on local directory.")

        
    def create_dockerfile ( self , file_name , python_version):
        #
        # This function creates a dockerfile to build an image that runs a specified python script.
        # Input:
        # * file_name: The python code
        # * python_version: The version of python engine to use
        # 
        try: 
            print("******************************************************************")
            print("********************* CREATING DOCKER FILE ***********************")
            print("******************************************************************")
            dockerfile = open('Dockerfile', 'w')
            if python_version == "2":
                line1 = "FROM python:2"
                line6 = "ENTRYPOINT [\"python\"]"
            else:
                line1 = "FROM python:3.8"
                line6 = "ENTRYPOINT [\"python3.8\"]"
            line2 = "WORKDIR /usr/src/app"
            line3 = "COPY . ."
            line4 = "CMD [\""+ str(file_name) +"\"]"
            dockerfile.write("%s \n%s \n%s \n" % (line1, line2, line3))
            dockerfile.write("%s \n%s \n" % (line4, line6))
            dockerfile.close()
            os.system('cat Dockerfile')
            print("******************************************************************")
        except:
            print ("There was an error while writing the Dockerfile file")


    def build_image ( self ):
        #
        # This function build a docker image from a dockerfile in the current directory.
        # 
        try:
            (image_object, image_generator) = self.client.images.build(path='./')
            os.system('docker images | head -2')
        except docker.errors.BuildError:
            self.error.error_images("building")
        except docker.errors.APIError:
            self.error.error_images("building")
        except :
            self.error.general_error("building the image")
        print("******************************************************************")
        print("***************************** IMAGE ID ***************************")
        print(image_object.id)
        return image_object.id
    

    def python_container ( self , file_name, python_version ):
        #
        # This function creates a container that runs a python script provided by the user.
        # Input:
        # * file_name: The python code
        # * python_version: The version of python engine to use
        # 
        try:
            # Create the dockerfile
            self.create_dockerfile(file_name, python_version)
            # Build image
            image_object_id = self.build_image()
            # Run container
            self.run_container(image_object_id)
        except:
            self.error.general_error("executing the python file on the container")


    def docker_compose ( self ):
        #
        # This function shows how the docker compose component works
        # 
        try:
            # Show running containers before execution
            print("******************************************************************")
            print("**************** CONTAINER LIST BEFORE EXECUTION *****************") 
            os.system('docker container ls')
            # Docker compose up
            print("******************************************************************")
            print("********************** DOCKER COMPOSE UP *************************") 
            os.system('cd composetest; nohup docker-compose up &')
            time.sleep(60)
            # Show running containers during execution
            print("******************************************************************")
            print("**************** CONTAINER LIST DURING EXECUTION *****************") 
            os.system('docker container ls')
            # Show link between Web and DB
            print("******************************************************************")
            print("*********** DEMONSTRATION OF LINK BETWEEN WEB AND DB *************") 
            for i in range(5):
                time.sleep(5)
                print("******************************************************************")
                print("************** CALLING WEBPAGE USING CURL COMMAND ****************") 
                os.system('curl http://localhost:5000')
                print("******************************************************************")
                print("******* LOGS FROM DOCKER COMPOSER SHOWN HTTP GET REQUEST *********") 
                os.system('tail -10 composetest/nohup.out')
            # Docker compose down
            print("******************************************************************")
            print("********************** DOCKER COMPOSE DOWN ***********************") 
            os.system('cd composetest; docker-compose down')
            # Show running containers after execution
            print("******************************************************************")
            print("**************** CONTAINER LIST AFTER EXECUTION ******************") 
            os.system('docker container ls')
        except:
            self.error.general_error("executing docker compose")





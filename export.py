import jq
import os
import stdiomask
import subprocess

print("******* This script will get the Image Stream values from all project in Openshift, You need permission as cluster_reader *********")
host = input("URL:  ")
username = input("Username: ")
password = stdiomask.getpass(prompt = 'Password: ')
command = os

#oc_project_list = os.system("oc get is -A")
#print(oc_project_list)

def login(username, password, host):
    oc_login_cmd = "oc login -u %s -p %s %s" % (username, password, host)
    process = subprocess.Popen(oc_login_cmd, shell=True, stdout=subprocess.PIPE)
    try:
        output, error = process.communicate()
        return True
    except:   
        print("Error OC LOGIN CMD: " + oc_login_cmd)
        return False

def logout():
    try:
        oc_logout_cmd = "oc logout"
        subprocess.popen(oc_logout_cmd)
    except:
        print('Error oc logout')
        
def list_all_is():
#    print("Logando...")
    if login(username, password, host):
        print("Auth is ok")
        print("Searching the projects")
        projects = subprocess.Popen("oc get projects -o jsonpath='{range .items[*]}{\":\"}{.metadata.name}'",shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for project  in projects.stdout:
            project_list = project.decode("utf-8").split(":")       
            for proj_obj in project_list:
#                print("Searching the pods")
                cmd_pods = "oc get pods -n {} -o custom-columns=NAME:.metadata.name  --field-selector status.phase=Running".format(proj_obj)
                pods = subprocess.Popen(cmd_pods,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                for pod in pods.stdout:
                    pod_name = pod.decode("utf-8")
#                    print("Searching image")
                    filter_json="-o jsonpath='{.spec.containers[0].image}'"
                    image_cmd = "oc get -n %s pod %s %s"% (proj_obj,pod_name.strip(), filter_json)

                    print(image_cmd)
                    images = subprocess.Popen(image_cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    for img in images.stdout:
                        img_name = img.decode("utf-8")
                        print("Image found: \n {} \n Project {} \n Pod {}".format(img_name, proj_obj, pod_name))

list_all_is()


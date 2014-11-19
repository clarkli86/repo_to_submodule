#!/usr/bin/python

import os
import sys
import xml.etree.ElementTree as ET
from termcolor import colored

def repo_to_submodule(superproject):
    # FIXME remove this line
    os.system("rm " + superproject + " -rf")
    os.mkdir(superproject)

    MANIFEST_XML = "manifest.xml"

    # 1. Create a manifest from repo
    if os.system("repo manifest -r -o " + superproject + "/" + MANIFEST_XML) != 0:
        print "Failed to create a repo manifest. Are you sure we are in a repo project folder?"
        sys.exit(-1)

    # 2. Initialise the git superproject
    os.chdir(superproject)
    os.system("git init")

    # 3. Add git submodules according to the hash in manifest.xml
    tree = ET.parse(MANIFEST_XML)
    root = tree.getroot()

    # Read fetch
    remote = root.find("remote")
    fetch = remote.get("fetch")

    # Iterate through all project
    for project in root.findall("project"):
        os.system("git submodule add " + fetch + project.get("name") + " " + project.get("path"))
        # Save current working directory
        pwd = os.getcwd()
        os.chdir(project.get("path"))
        os.system("git reset --hard " + project.get("revision"))
        # Get back to the root of superproject
        os.chdir(pwd)

    # Remove manifest.xml
    os.remove(MANIFEST_XML)

    print colored("Success!\nPlease go to " + superproject + " and commit your superproject", "green")

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print "Usage: repo_to_submodule.py GIT_SUPERPROJECT_NAME"
        sys.exit(-1)

    repo_to_submodule(sys.argv[1])

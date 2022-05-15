# chatroom

This is a chatroom program made for the spring 2022 semester Advanced Python Programming class at Mission College. It was made by Kyle Smith and Adeeb Syed.

# Dependencies

This project depends on multiple other projects to function:
1. Python 3: [Python](https://www.python.org/downloads/)
2. MariaDB for Python
3. git: [git](https://git-scm.com/downloads)
4. git-crypt: [git-crypt](https://github.com/AGWA/git-crypt)




# Installation:

First, you need to install Python. Once python is installed, you can install the mariadb module by doing the following in the command line: ```pip install mariadb```. 

Now you need git, which can be downloaded and installed from their website. Once git is installed, you can download the latest release from git-crypt. I recommend renaming the exe file to something easier like ```git-crypt.exe```. Now we need to clone this repository with git. To do this, you can click on the green code icon at the top and copy the repo link seen there: ```https://github.com/BrakeZap/chatroom.git```. Once copied, do the following in the command line: ```git clone https://github.com/BrakeZap/chatroom.git```. You can also specify where you want the files to go using: ```git clone https://github.com/BrakeZap/chatroom.git <dir>```. 

Now that we have all the files, we still aren't able to run the program because the info.json file is encrypted. In order to decrypt it, drag the git-crypt.exe into the same directory. Now you also need the secret file that I will give to trusted people. This for extra protection for the database and servers that will be running the chatrooms. There are security precausions taken to prevent even further damage even if you have the key but just to be safe, the info.json file is encrypted. Drag the secret file into the directory. Now type the following into the command line: ```git-crypt.exe unlock secretkey.key```. You know that this works if you can see inside the info.json file. 

Once you are able to see inside the info.json file, you can change the 3 ips listed in there to the ips for the running servers.


# Usage

Now you can finally run the LoginGUI.py by double-clicking it or by running the following in the command line: ```py LoginGUI.py```. Create an account, login, and then choose one of the online servers to chat!

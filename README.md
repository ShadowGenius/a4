# ICS 32 Assignment 4 Direct Messaging App

## Features

### Direct Messaging
You can send messages directly to other people connected to the ICS 32 DSU system.

### Contacts
You can add multiple contacts and easily switch between them to send messages and view your message history.

### DSU Profiles
You can create a .dsu file to save your Profile in. This allows you to save your message history locally and easily 'log in' for future uses of the app.

## How to Use

### Set Up

1) Run the a4.py file to start the application. A GUI should automatically appear.

2) Go to 'Settings' and click on 'Configure Server' to enter in the server IP, your username, and your password.

3) (Optional, but recommended): Go to 'File' and click on 'New' and choose a directory. This will create a .dsu file that holds your DSU Profile, enabling you to store your information and message history locally.

### Messaging Someone

1) Click on 'Add Contact' on the bottom left to enter the username of someone you want to send a message to.

2) The name you entered will appear in the tree on the left. Click on the name to select them.

3) Type in your message into the box on the bottom right and press 'Send' to send it.

4) The message will appear in the large box in the top right. Messages from the recipient will automatically appear in the same box shortly after they are sent. Your messages will be in red and on the right while the recipient's messages will be in blue on the left.

### Files

Under 'Files,' there are three options: 'New,' 'Open...,' and 'Close.'

The 'New' option allows you to create a new .dsu file containing a Profile based on current data.

The 'Open...' option allows you to open a previously created .dsu file and load its information, closing any currently loaded file.

The 'Close' option allows you to clear all current information such as username, password, and loaded file.

### Settings

Under 'Settings,' there are two options: 'Configure DS Server' and 'Remove Contact.' 

The 'Configure DS Server' option allows you to enter a server IP, username, and password to log into the DSU network.

The 'Remove Contact' option allows you to remove one of the contacts you have added. If you have a .dsu file loaded, message history with this contact is saved.
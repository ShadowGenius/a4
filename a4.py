'''Module for GUI for Assignment 4'''

import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import ds_messenger
import Profile

class Body(tk.Frame):
    '''Body of the GUI'''
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts: list[str] = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        '''Calls the function when a contact is selected.'''
        if event and len(self.posts_tree.selection()) > 0:
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
        '''Inserts a contact in to the contact tree.'''
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, contact_id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        else:
            entry = contact
        contact_id = self.posts_tree.insert('', contact_id, contact_id, text=entry)

    def remove_contact(self, contact: str):
        '''Removes a contact from the contact tree.'''
        if contact in self._contacts:
            contact_id = self._contacts.index(contact)
            self._remove_contact_tree(contact_id)

    def _remove_contact_tree(self, contact_id):
        self.posts_tree.delete(contact_id)

    def get_contacts(self):
        '''Returns the currently added contacts.'''
        return self._contacts

    def clear_contacts(self):
        '''Removes all contacts.'''
        for contact in self._contacts:
            self.remove_contact(contact)
        self._contacts: list[str] = []

    def insert_user_message(self, message:str):
        '''Inserts messages into the body on the user side, which is the right.'''
        self.entry_editor.insert(tk.END, message + '\n', ['entry-right', 'red'])

    def insert_contact_message(self, message:str):
        '''Inserts messages into the body on the contact side, which is the left.'''
        self.entry_editor.insert(tk.END, message + '\n', ['entry-left', 'blue'])

    def clear_messages(self):
        '''Clears all messages in the entry editor.'''
        self.entry_editor.delete(1.0, tk.END)

    def get_text_entry(self) -> str:
        '''Returns the text in the message editor.'''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        '''Replaces current text in the messager editor with text argument.'''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.tag_configure('blue', foreground="blue")
        self.entry_editor.tag_configure('red', foreground="red")
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''Footer of the GUI'''
    def __init__(self, root, send_callback=None, add_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._draw()

    def send_click(self):
        '''Calls the function associated with the "Send" button.'''
        if self._send_callback is not None:
            self._send_callback()

    def add_click(self):
        '''Calls the function associated with the "Add Contact" button.'''
        if self._add_callback is not None:
            self._add_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

        add_button = tk.Button(master=self, text="Add Contact", width=15, command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=35, pady=5)


class NewContactDialog(tk.simpledialog.Dialog):
    '''Dialog for a user to add a new contact.'''
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, master):
        self.server_label = tk.Label(master, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        self.server_entry.insert(tk.END, self.server if self.server is not None else '')
        self.server_entry.pack()

        self.username_label = tk.Label(master, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user if self.user is not None else '')
        self.username_entry.pack()

        self.password_label = tk.Label(master, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, width=30)
        self.password_entry.insert(tk.END, self.pwd if self.pwd is not None else '')
        self.password_entry['show'] = '*'
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    '''Main functionality of the application.'''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.direct_messenger = ds_messenger.DirectMessenger()
        self.profile = None
        self.file = None

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        #self.body.insert_contact("studentexw23") # adding one example student.

    def send_message(self):
        '''Sends a message or gives an error if message couldn't be sent.'''
        message = self.body.get_text_entry()
        if self.direct_messenger.send(message, self.recipient):
            self.publish(message)
        else:
            tk.messagebox.showerror("Error", "Message not sent.")

    def add_contact(self):
        '''Asks for a contact to add to the tree and Profile (if any).'''
        contact_name = tk.simpledialog.askstring("Add contact.", "Contact name")
        if contact_name:
            self.body.insert_contact(contact_name)
            if self.profile and self.file:
                self.profile.friends_list.append(contact_name)
                self.profile.save_profile(self.file)

    def recipient_selected(self, recipient):
        '''Sets the current recipient to the one just selected and displays messages.'''
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        self.check_new()

    def configure_server(self):
        '''Allows the user to set their server IP, username, 
        and password to configure the DirectMessenger.'''
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = ds_messenger.DirectMessenger(self.server,
                                                             self.username,
                                                             self.password)

    def publish(self, message:str):
        '''Publishes sent messages to the body.'''
        self.body.insert_user_message(message)
        self.body.set_text_entry('')
        if self.profile and self.file:
            for dm in self.direct_messenger.dms_out:
                if dm not in self.profile.direct_messages:
                    self.profile.direct_messages.append(dm)
            self.profile.save_profile(self.file)

    def check_new(self):
        '''Retrieves all messages to update the body with.'''
        if self.profile:
            list_of_dms = self.profile.direct_messages
            list_of_dms += self.direct_messenger.retrieve_new()
        else:
            list_of_dms = self.direct_messenger.retrieve_all()
            list_of_dms += self.direct_messenger.dms_out
            list_of_dms = Profile.recursive_sort(list_of_dms)
        if len(list_of_dms) > 0:
            self.update_new(list_of_dms)
        # elif self.profile and not self.direct_messenger.token:
        #     for msg in self.profile.direct_messages:
        #         self.insert_message(msg)
        self.check_new_loop()

    def insert_message(self, msg):
        '''Inserts a message into the message body based on the sender and recipient.'''
        if msg.sender == self.recipient:
            self.body.insert_contact_message(msg.message)
        elif msg.sender == self.username and msg.recipient == self.recipient:
            self.body.insert_user_message(msg.message)

    def update_new(self, list_of_dms):
        '''Given a list of DMs, adds them to the currently 
        loaded Profile (if any) and inserts them into the body.'''
        for msg in list_of_dms:
            if self.profile and self.file and msg not in self.profile.direct_messages:
                self.profile.direct_messages.append(msg)
                self.profile.save_profile(self.file)
            self.insert_message(msg)

    def check_new_loop(self):
        '''Looping function to check for new messages and calls update_new if there are any.'''
        list_of_new = self.direct_messenger.retrieve_new()
        if len(list_of_new) > 0:
            self.update_new(list_of_new)
        self.root.after(2000, self.check_new_loop)

    def open_file(self):
        '''Opens a .dsu file and loads its relevant information.'''
        file = filedialog.askopenfilename()
        if file:
            self.close_file()
            self.file = file
            profile = Profile.Profile()
            profile.load_profile(file)
            self.profile = profile
            self.username = profile.username
            self.password = profile.password
            self.server = profile.dsuserver
            for friend in profile.friends_list:
                self.body.insert_contact(friend)
            self.direct_messenger = ds_messenger.DirectMessenger(self.server,
                                                                 self.username,
                                                                 self.password)

    def new_file(self):
        '''Creates a new .dsu file based on currently entered 
        username, password, server ip, messages, and contacts.'''
        directory = filedialog.askdirectory()
        if directory:
            p = Path(directory) / (self.username + ".dsu")
            self.file = p
            f = p.open("w+")
            f.close()
            user_profile = Profile.Profile(self.server, self.username, self.password)
            user_profile.friends_list = self.body.get_contacts()
            user_profile.direct_messages = self.direct_messenger.retrieve_all()
            user_profile.save_profile(p)
            self.profile = user_profile

    def close_file(self):
        '''Clears all loaded user information if a file is loaded.'''
        if self.profile is not None:
            self.body.clear_contacts()
            self.username = ''
            self.password = ''
            self.server = ''
            self.recipient = None
            self.direct_messenger = ds_messenger.DirectMessenger()
            self.profile = None
            self.file = None
            self.body.clear_messages()

    def remove_contact(self):
        '''Asks for a contact to remove from the tree and Profile (if any).'''
        contact_name = tk.simpledialog.askstring("Remove Contact.", "Contact name")
        if contact_name:
            self.body.remove_contact(contact_name)
            if self.profile and self.file and contact_name in self.profile.friends_list:
                self.profile.friends_list.remove(contact_name)
                self.profile.save_profile(self.file)

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_file)
        menu_file.add_command(label='Open...', command=self.open_file)
        menu_file.add_command(label='Close', command=self.close_file)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        settings_file.add_command(label='Remove Contact',
                                  command=self.remove_contact)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message,
                             add_callback=self.add_contact)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    after_id = main.after(2000, app.check_new)
    print(after_id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox

FILE_TYPES = [("Text Documents", "*.txt"), ("All Files", "*.*")]

class Notepad:
    def __init__(self):
        self.root = tk.Tk() # create main window for notepad
        self.root.title("Notepad")
        self.root.geometry("600x600")

        self.current_file = None  # keep track of the current file being edited

        # display notepad stuff 
        self.root.option_add('*tearoff', False) # disable tear-off menus (NEEDED)
        self.create_menu()
        self.create_text() 
        self.bind_shortcuts() 

        self.root.protocol("WM_DELETE_WINDOW", self.exit) 

    def create_text(self): # create the text area for the notepad
        self.text = tk.Text(self.root, wrap='word', font=('Consolas', 11), undo=True)
        self.text.pack(expand=True, fill='both')

    def create_menu(self): # create the menu bar for the notepad
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Rename", command=self.rename_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)

        menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu)

    def new_file(self):
        if not self.warn_unsaved_changes():  # check for unsaved changes before creating a new file
            return
        
        self.root.title("Notepad - New File")
        self.current_file = None
        self.text.delete(1.0, tk.END) 
        self.text.edit_modified(False)  
        self.text.edit_reset() 

    def rename_file(self):
        if self.current_file is None:
            messagebox.showinfo("Rename File", "No file is currently open to rename.")
            return

        new_name = asksaveasfilename(defaultextension=".txt", 
                                     filetypes=FILE_TYPES, 
                                     initialfile=self.current_file)
        
        if new_name:
            try:
                with open(self.current_file, "r", encoding="utf-8") as file:
                    content = file.read()
                with open(new_name, "w", encoding="utf-8") as new_file:
                    new_file.write(content)
                self.current_file = new_name
                self.root.title(f"Notepad - {new_name}")
            except OSError as e:
                messagebox.showerror("Error", f"Could not rename file: {e}")


    def open_file(self):
        if not self.warn_unsaved_changes(): 
            return
        
        path = askopenfilename(defaultextension=".txt", filetypes=FILE_TYPES)
        
        if path:
            try: 
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
            except (OSError, UnicodeDecodeError) as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
                return

            self.current_file = path
            self.root.title(f"Notepad - {path}")
            self.text.delete(1.0, tk.END) 
            self.text.insert(1.0, content) 
            self.text.edit_modified(False)  
            self.text.edit_reset() 

    def save_file(self):
        path = self.current_file

        if path is None:
            path = asksaveasfilename(defaultextension=".txt", filetypes=FILE_TYPES)

        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(self.text.get("1.0", "end-1c")) 
            except OSError as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
                return

            self.current_file = path
            self.root.title(f"Notepad - {path}") 
            self.text.edit_modified(False)  
            self.text.edit_reset() 

    def bind_shortcuts(self): # keyword shortcuts for the notepad
        self.root.bind("<Control-n>", self._shortcut_handler(self.new_file))
        self.root.bind("<Control-o>", self._shortcut_handler(self.open_file))
        self.root.bind("<Control-s>", self._shortcut_handler(self.save_file))
        self.root.bind("<Control-q>", self._shortcut_handler(self.exit))
        self.root.bind("<Control-r>", self._shortcut_handler(self.rename_file))

    def _shortcut_handler(self, func): # handler for keyboard shortcuts
        def handler(event):
            func()
            return "break"  
        return handler

    def warn_unsaved_changes(self): # warn about unsaved changes before new, open, or exit
        if not self.text.edit_modified():  
            return True  # no unsaved changes, proceed with the action
        
        response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")

        if response is None:  # user clicked cancel, do not proceed 
            return False
        if response: # user clicked yes, save the file
            self.save_file()
            return not self.text.edit_modified()  # return true if save was good, false otherwise
        return True  # user clicked no, proceed without saving

    def run(self): # run the notepad application
        self.root.mainloop()

    def exit(self): # exit the application
        if self.warn_unsaved_changes(): 
            self.root.destroy()


if __name__ == "__main__":
    notepad = Notepad()
    notepad.run()


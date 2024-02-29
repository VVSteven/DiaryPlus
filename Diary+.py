import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import Text
import os

#Diary+ App by Elvis Canastuj

#variable to store the selected directory
selectDirectory = ""

#creates a function to save a diary entry
def saveEntry():
    #gets the diary entry text from the text box
    entry = text.get("1.0", "end-1c")
    #get the current date and time in 12-hour format
    currentDateTime = datetime.now().strftime("%Y-%m-%d_%I-%M-%S %p")
    #creates a filename with the current date and time
    filename = f"Diary_Entry_{currentDateTime}.txt"
    
    #the user find a path to store the file
    filePath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile=filename)
    
    #if a file path is selected
    if filePath:
        #opens the file for writing
        with open(filePath, "w") as file:
            #writes the users entry to the file
            file.write(entry)
        messagebox.showinfo("Note Saved")
#function to select a directory and to show the diary entries in the selected directory 
def selectDirectory():
    #calls the selectDirectory variable 
    global selectDirectory
    #opens new window to select a directory
    selectDirectory = filedialog.askdirectory()
    #clears the entry to insert the address of the diary folder
    directoryEntry.delete(0, tk.END)
    directoryEntry.insert(tk.END, selectDirectory)
    
    try:
        #lists and looks for all the txt files in the selected directory
        fileList = [f for f in os.listdir(selectDirectory) if f.endswith('.txt')]
        #clears any previous lists
        entryListBox.delete(0, tk.END)  # Clear the listbox
        
        #inserts all the txt files in the file box
        for file in fileList:
            entryListBox.insert(tk.END, file)
    #shows error message if the directory is not found
    except FileNotFoundError:
        messagebox.showerror("Error", "Directory not selected.")

#function to open the selected txt file 
def openSelectedFile():
    #gets the file from the selected file in the list box
    selectedFile = entryListBox.get(tk.ACTIVE)
    #concatenates the selected directory with the selected file to make a full path 
    filePath = os.path.join(selectDirectory, selectedFile)

    try:
        #opens the file to read the entry
        with open(filePath, 'r') as file:
            file_contents = file.read()
            #clears previous entry to insert the new one that was selected 
            text.delete(1.0, tk.END)
            text.insert(tk.END, file_contents)
    #shows error message if the file is not found
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
 
#function to clear text from the text box
def clearText():
    # Deletes all text from the text widget
    text.delete(1.0, tk.END)

#creates the main app window
root = tk.Tk()

#sets the app title
root.title("Diary+")

#sets the size of the window
root.geometry("550x655")

#creates a frame for the text box and save and clear buttons
mainFrame = tk.Frame(root)
#creates 1 column 
mainFrame.columnconfigure(0, weight=1)

#creates a text box for diary entries 
text = tk.Text(mainFrame, height=15, wrap=tk.WORD, font=('Arial', 14)) 
#adds the box to the frame
text.grid(row=0, column=0)

#creates a button to save diary entries
saveButton = tk.Button(mainFrame, height=2, text="Save Entry", font=('Arial', 10), command=saveEntry)
#adds the button in the frame
saveButton.grid(row=1, column=0, sticky=tk.W+tk.E)

#creates a button to clear text from the text box
clearButton = tk.Button(mainFrame, height=2, text="Clear Text", font=('Arial', 10), command=clearText)
#adds the button in the frame
clearButton.grid(row=2, column=0, sticky=tk.W + tk.E)

#organizes the frame widget
mainFrame.pack(fill='x')

#creates a frame for the ent box and save and clear buttons
directoryFrame = tk.Frame(root)
#creates 3 columns
directoryFrame.columnconfigure(0, weight=10)
directoryFrame.columnconfigure(1, weight=1)
directoryFrame.columnconfigure(2, weight=5)

#creates a box that shows the address of the selected directory
directoryEntry = tk.Entry(directoryFrame)
#adds the box to the frame
directoryEntry.grid(row=0, column=0, sticky=tk.W+tk.E)

#creates a box and shows the list of availible diary entries
entryListBox = Listbox(directoryFrame, font=('Arial', 11))
#adds the box to the frame
entryListBox.grid(row=1, column=0, sticky=tk.W+tk.E)

#adds a scroll bar to the entry list box 
entryListScrollBar = Scrollbar(directoryFrame, orient="vertical" ,command=entryListBox.yview)
#adds the scroll bar to the frame
entryListScrollBar.grid(row=1, column=1, sticky=tk.N+tk.S)
#links the scroll bar to the entry list box
entryListBox.config(yscrollcommand=entryListScrollBar.set)

#button that when clicked activates the selectDirectory function
directorySelectButton = tk.Button(directoryFrame, text="Select Directory", command=selectDirectory)
#adds the button in the frame
directorySelectButton.grid(row=0, column=2, sticky=tk.W+tk.E)

#button that when clicked activates the openSelectedFile function
openEntryButton = tk.Button(directoryFrame, text="Open Entry", font=('Arial', 10), command=openSelectedFile)
#adds the button in the frame
openEntryButton.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

#organizes the frame widget
directoryFrame.pack(fill='both')

#start the main GUI event loop
root.mainloop()

import tkinter as tk
 
 
def selected():
    print(listbox.get(listbox.curselection()[0]))
 
root = tk.Tk()
listbox = tk.Listbox(root)
listbox.pack()
for i in range(10):
    listbox.insert(0,i)
listbox.bind("<<ListboxSelect>>", lambda x: selected())
root.mainloop()
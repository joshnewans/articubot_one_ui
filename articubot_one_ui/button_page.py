from tkinter import *

class ButtonPage():

    def __init__(self, root):
        self.tk = Frame(root)
        self.tk.pack(expand=True, fill="both")

        self.tk.configure(bg="white")
        self.tk.rowconfigure(tuple(range(3)), weight=1)
        self.tk.columnconfigure(tuple(range(3)), weight=1)

        self.col_a = "orange"
        self.col_b = "red"
        
        self.b1 = Button(self.tk, text="Button1", bg=self.col_a, font=("Arial", 30))
        self.b2 = Button(self.tk, text="Button2", bg=self.col_a, font=("Arial", 30))
        self.b3 = Button(self.tk, text="Button3", bg=self.col_a, font=("Arial", 30))
        self.b4 = Button(self.tk, text="Button4", bg=self.col_a, font=("Arial", 30))

        self.b1.grid(row = 0, column = 1, sticky = 'news', pady = 2)
        self.b2.grid(row = 1, column = 0, sticky = 'news', pady = 2)
        self.b3.grid(row = 1, column = 2, sticky = 'news', pady = 2)
        self.b4.grid(row = 2, column = 1, sticky = 'news', pady = 2)

        self.buttons = {}


    def assign_button(self, ui_button_handle, joy_button_id, button_text, command):
        ui_button_handle["text"] = button_text
        ui_button_handle["command"] = command
        self.buttons[joy_button_id] = { "val": False, "ui": ui_button_handle, "zzz": command}


    def update_image(self):
        self.tk.update()


    def button_down(self, widget):
        widget.config(relief = "sunken")
        widget["bg"] = self.col_b


    def button_up(self, widget):
        widget.config(relief = "raised")
        widget["bg"] = self.col_a
        widget.invoke()


    def handle_button(self, button_id, button_val):
        if button_id in self.buttons:
            prev_val = self.buttons[button_id]["val"]
            if (button_val and not prev_val):
                self.button_down(self.buttons[button_id]["ui"])
            elif (not button_val and prev_val):
                self.button_up(self.buttons[button_id]["ui"])
            self.buttons[button_id]["val"] = button_val


    def process_joy(self, joy_vals):
        for i,b in enumerate(joy_vals.buttons):
            self.handle_button(i,b)
        return


    def destroy(self):
        self.tk.destroy()

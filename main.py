import tkinter as tk
from tkinter import ttk, filedialog

from bitmapedit import BitmapEdit
from monovlsb import MonoVlsb


class BitmapEditApp:
    def __init__(self, root):
        self.index = 0
        self.popup = None
        self.root = root
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="NWES")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.font_data = bytearray(8)
        self.bitmap = MonoVlsb(memoryview(self.font_data), 8, 8)
        self.bme = BitmapEdit(mainframe, self.bitmap, 20)
        self.bme.grid(row=1, column=1)
        self.filename = None

        self.label_text = tk.StringVar(value="Index: " + str(self.index))
        self.label = ttk.Label(mainframe, textvariable=self.label_text)
        self.label.grid(column=1, row=0, sticky="WE")

        ttk.Button(mainframe, text="Next", command=self.inc).grid(column=2, row=1, sticky="W")
        ttk.Button(mainframe, text="Prev", command=self.dec).grid(column=0, row=1, sticky="W")

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def update(self):
        self.bitmap.set_bitmap_data(memoryview(self.font_data)[self.index:self.index + self.bitmap.size])
        self.bme.set_bitmap(self.bitmap)
        self.label_text.set("Index: " + str(self.index // self.bitmap.size) +
                            "   Count: " + str(len(self.font_data) // self.bitmap.size))

    def inc(self):
        if self.index < len(self.font_data) - self.bitmap.size:
            self.index += self.bitmap.size
            self.update()

    def dec(self):
        if self.index >= self.bitmap.size:
            self.index -= self.bitmap.size
            self.update()

    def file_open(self):
        self.filename = tk.filedialog.askopenfilename()
        # print(filename)
        file = open(self.filename, "r")
        lines = file.readlines()
        file.close()
        output = False
        width = 8
        height = 8
        self.font_data = bytearray()
        for line in lines:
            # remove whitespace
            line = line.strip()
            if line.find('// font edit end') >= 0:
                output = False
            if output:
                # remove comments
                text = line.split('/', 1)[0]
                # print(text)
                ba = bytearray.fromhex(text.replace('0x', '').replace(',', ''))
                # print(text, ba.hex())
                self.font_data.extend(ba)
            if line.find('// font edit begin') >= 0:
                values = line.split(':')
                try:
                    width = int(values[2])
                    height = int(values[3])
                    output = True
                except:
                    print('Parse error:', values)
        # print(self.font_data.hex(' '))
        print('W:', width, 'H:', height)
        self.bitmap = MonoVlsb(memoryview(self.font_data), width, height)
        self.index = 0
        self.update()

    # Define a function to close the popup window
    def close_win(self, w_entry, h_entry, s_entry):
        print(w_entry.get(), h_entry.get(), s_entry.get())
        self.popup.destroy()

    # Define a function to open the Popup Dialogue
    def popupwin(self):
        # Create a Toplevel window
        self.popup = tk.Toplevel(self.root)

        mainframe = ttk.Frame(self.popup, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="NWES")
        self.popup.columnconfigure(0, weight=1)
        self.popup.rowconfigure(0, weight=1)

        w_entry = ttk.Entry(mainframe, width=10)
        w_entry.grid(row=0, column=0)

        h_entry = ttk.Entry(mainframe, width=10)
        h_entry.grid(row=0, column=1)

        s_entry = ttk.Entry(mainframe, width=10)
        s_entry.grid(row=0, column=2)

        # Create a Button to print something in the Entry widget
        ttk.Button(mainframe, text="Cancel").grid(row=1, column=1)
        # Create a Button Widget in the Toplevel Window
        button = ttk.Button(mainframe, text="Ok", command=lambda: self.close_win(w_entry, h_entry, s_entry))
        button.grid(row=1, column=2)

    def save(self):
        prefix = ''
        postfix = ''
        if self.filename is None:
            prefix = 'const unsigned char binary_data[] = {\n'
            postfix = '};\n'
            self.filename = 'default_monovlsb.h'
        else:
            file = open(self.filename, "r")
            lines = file.readlines()
            file.close()
            for l in lines:
                if l.find('// font edit begin') >= 0:
                    break
                prefix += l
            append = False
            for l in lines:
                if append:
                    postfix += l
                if l.find('// font edit end') >= 0:
                    append = True

        with open(self.filename, 'w', encoding='ISO8859-1') as f:
            f.write(prefix)
            f.write('// font edit begin : monovlsb : ')
            f.write(str(self.bitmap.width) + ' : ' + str(self.bitmap.height))

            for i in range(len(self.font_data) - 1):
                if i % 8 == 0:
                    f.write('\n    ')
                f.write("0x%0.2X" % self.font_data[i] + ', ')
            f.write("0x%0.2X" % self.font_data[-1])
            f.write('\n')

            f.write('// font edit end\n')
            f.write(postfix)

def donothing():
    pass


def run():
    root = tk.Tk()
    root.title("Bitmap/font editor")

    bme = BitmapEditApp(root)

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=bme.popupwin)
    filemenu.add_command(label="Open", command=bme.file_open)
    filemenu.add_command(label="Save", command=bme.save)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    root.mainloop()


if __name__ == '__main__':
    run()

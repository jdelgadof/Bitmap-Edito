import os.path
import tkinter as tk
from tkinter import ttk, filedialog
from bitmapedit import BitmapEdit
from monovlsb import MonoVlsb

PIL_is_installed = True

try:
    import PIL.Image
except ModuleNotFoundError:
    PIL_is_installed = False
    print('You must have Pillow installed to open .png or .bmp files')
    print('To install:  pip install pillow')


class BitmapEditApp:
    def __init__(self, root):
        self.index = 0
        self.popup = None
        self.root = root
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="NWES")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.font_data = bytearray(MonoVlsb.size(8, 8))
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
                            "   Count: " + str(len(self.font_data) // self.bitmap.size) +
                            "   Width: " + str(self.bitmap.width) +
                            "   Height: " + str(self.bitmap.height))

    def inc(self):
        if self.index < len(self.font_data) - self.bitmap.size:
            self.index += self.bitmap.size
            self.update()

    def dec(self):
        if self.index >= self.bitmap.size:
            self.index -= self.bitmap.size
            self.update()

    def file_open(self):
        data, height, width, filename = self.read_data_from_file()
        if data is not None:
            self.font_data = data
            self.bitmap = MonoVlsb(memoryview(self.font_data), width, height)
            self.filename = filename
            self.index = 0
            self.update()

    def read_data_from_file(self):
        filename = tk.filedialog.askopenfilename()
        print(os.path.splitext(filename), os.path.basename(filename))
        extension = os.path.splitext(filename)[1]
        if extension == '.png' or extension == '.bmp':
            if not PIL_is_installed:
                tk.messagebox.showwarning(title='PILLOW not installed',
                                          message='You need to install Pillow to open bitmap files.')
                data, width, height = (None, 0, 0)
            else:
                data, width, height = self.read_bitmap_file(filename)
            # filename = os.path.basename(os.path.splitext(filename)[0]) + '.h'
            # filename = os.path.splitext(filename)[0] + '.h'
            filename = None  # kludge until creating a new file with non-default name is fixed
        else:
            data, width, height = self.read_source_file(filename)

        return data, height, width, filename

    def read_source_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()
        output = False
        width = 8
        height = 8
        data = bytearray()
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
                data.extend(ba)
            if line.find('// font edit begin') >= 0:
                values = line.split(':')
                try:
                    width = int(values[2])
                    height = int(values[3])
                    output = True
                except ValueError:
                    print('Parse error:', values)
        # print(data.hex(' '))
        print('W:', width, 'H:', height)
        byte_count = MonoVlsb.size(width, height)
        if len(data) % byte_count != 0:
            missing = ((len(data) // byte_count) + 1) * byte_count - len(data)
            data.extend(bytearray(missing))
            print("Added", missing, "bytes to align buffer size")
        return data, width, height

    def read_bitmap_file(self, filename):
        image = PIL.Image.open(filename).convert('1')
        data = bytearray(MonoVlsb.size(image.width, image.height))
        bitmap = MonoVlsb(memoryview(data), image.width, image.height)
        for x in range(image.width):
            for y in range(image.height):
                px = image.getpixel((x, y))
                # print(px)
                if px < 127:
                    bitmap.set_pixel(x, y, 1)
        image.close()
        return data, bitmap.width, bitmap.height

    # Define a function to close the popup window
    def close_new_image_popup(self, w_entry, h_entry, s_entry):
        print(w_entry.get(), h_entry.get(), s_entry.get())
        try:
            width = int(w_entry.get())
            height = int(h_entry.get())
            stride = int(s_entry.get())
            print("Values:", width, height, stride)
            self.font_data = bytearray(MonoVlsb.size(width, height, stride))
            self.bitmap = MonoVlsb(memoryview(self.font_data), width, height)
            self.index = 0
            self.update()
        except ValueError:
            print('Incorrect arguments')
        self.popup.destroy()

    # Define a function to open the Popup Dialogue
    def new_image_popup(self):
        # Create a Toplevel window
        self.popup = tk.Toplevel(self.root)

        mainframe = ttk.Frame(self.popup, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="NWES")
        self.popup.columnconfigure(0, weight=1)
        self.popup.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text='Width').grid(row=0, column=0, sticky="WE")
        ttk.Label(mainframe, text='Height').grid(row=0, column=1, sticky="WE")
        ttk.Label(mainframe, text='Stride').grid(row=0, column=2, sticky="WE")

        w_entry = ttk.Entry(mainframe, width=10)
        w_entry.grid(row=1, column=0)
        w_entry.insert(0, "16")

        h_entry = ttk.Entry(mainframe, width=10)
        h_entry.grid(row=1, column=1)
        h_entry.insert(0, "16")

        s_entry = ttk.Entry(mainframe, width=10)
        s_entry.grid(row=1, column=2)
        s_entry.insert(0, "0")

        # Create a Button to print something in the Entry widget
        ttk.Button(mainframe, text="Cancel", command=self.popup.destroy).grid(row=2, column=1)
        # Create a Button Widget in the Toplevel Window
        button = ttk.Button(mainframe, text="Ok", command=lambda: self.close_new_image_popup(w_entry, h_entry, s_entry))
        button.grid(row=2, column=2)

    def save(self):
        prefix = ''
        postfix = ''
        if self.filename is None:
            prefix = 'const unsigned char binary_data[] = {\n'
            prefix += '// font edit begin : monovlsb : ' + self.bitmap.width + ' : ' + str(self.bitmap.height)
            postfix = '// font edit end\n};\n'
            self.filename = 'default_monovlsb.h'
        else:
            with open(self.filename, "r") as file:
                lines = file.readlines()
            for line in lines:
                prefix += line
                if line.find('// font edit begin') >= 0:
                    break
            append = False
            for line in lines:
                if line.find('// font edit end') >= 0:
                    append = True
                if append:
                    postfix += line
            prefix = prefix.strip()  # output will add line feed so strip white space from the end

        with open(self.filename, 'w', encoding='ISO8859-1') as f:
            f.write(prefix)

            for i in range(len(self.font_data) - 1):
                if i % 8 == 0:
                    f.write('\n    ')
                f.write("0x%0.2X" % self.font_data[i] + ', ')
            f.write("0x%0.2X" % self.font_data[-1])
            f.write('\n')

            f.write(postfix)

    def append(self):
        data, height, width, filename = self.read_data_from_file()
        if data is not None and height == self.bitmap.height and width == self.bitmap.width:
            self.bitmap.set_bitmap_data(None)  # remove export of current data
            self.font_data.extend(data)  # extend data
            self.index = 0
            self.update()  # update will re-export the data
        else:
            tk.messagebox.showwarning(title='Incorrect image size',
                                      message="Selected image dimensions don't match the current image.")


def donothing():
    pass


def run():
    root = tk.Tk()
    root.title("Bitmap/font editor")
    print(root.winfo_screenwidth(), root.winfo_screenheight())

    bme = BitmapEditApp(root)

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=bme.new_image_popup)
    filemenu.add_command(label="Open", command=bme.file_open)
    filemenu.add_command(label="Append", command=bme.append)
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

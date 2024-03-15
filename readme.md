# Font / graphics editor for RPI Pico
A simple graphics editor for creating and editing bitmap files. 
Primary target RPI Pico and images/fonts are saved as header files 
containing uint8_t array of bytes. Header file must contain two 
special comments to mark the beginning and end of byte array data.

The main file of the program in gfed.py. Program takes no parameters.

Source file can be in any language as long as the special comments shown below are found in the file. 
If the language does not support C/C++ style comments precede the line (including C/C++ style comment) 
with a supported comment marker. For example, # in Python. 

To mark beginning use:

    // font edit begin : monovlsb : 20 : 20 : 20 

The parameters after the first colon specify the format of the bitmap. At the moment only monovlsb-format 
is supported. The two numbers after the format are width and height of the bitmap in pixels. The third 
number is optional. Stride specifies the number of pixels in the bitmap per row. Usually the number is 
same or close to the width of the bitmap. It is omitted then width of the bitmap is used as stride. 
In monovlsb type width and stride should be equal.


    const unsigned char binary_data[] = {
    // font edit begin : monovlsb : 20 : 20
    0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x08
    // font edit end
    };


The end of byte array is marked with:

    // font edit end

The end marker has no parameters.

The editor preserves the content of the file before the beginning 
and after the end markers.

You can open any text file that has valid begin and end markers.

If you have Pillow installed you can also open .png and .bmp files. 
Note that the width and height of the files should be relatively small 
(less than 150x150 pixels) even though the size of the bitmap is not 
limited by the program. There is only two levels of zoom so editing 
a large bitmap will be impossible due to missing scroll bars. 
The bitmaps are converted to monochrome when they are opened but for 
best results they should be converted to monochrome using a fully featured 
graphics editor before opening with this editor.
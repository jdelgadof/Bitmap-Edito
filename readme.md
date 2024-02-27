# Font / graphics editor for RPI Pico
A simple graphics editor for creating and editing bitmap files. Primary target RPI Pico and images/fonts are saved as header files containing uint8_t array of bytes. Header file must contain two special comments to mark the beginning and end of byte array data.

To mark beginning use:

    // font edit begin : monovlsb : 20 : 20

The parameters after the first colon specify the format of the bitmap. At the moment only monovlsb-format is supported. The two numbers after the format are width and height of the bitmap in pixels.


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

The editor preserves the content of the file before the begin and after the end markers.

You can open any text file that has valid begin and end markers.

If you have Pillow installed you can also open .png and .bmp files. Note that the width and height of the files should be relatively small (less than 150x150 pixels) even though the size of the bitmap is not limited by the program. There is only two levels of zoom so editing a large bitmap will be impossible due to missing scroll bars. The bitmaps are converted to monochrome when they are opened but for best results they should be converted to monochrome using a proper graphics editor.
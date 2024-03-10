class MonoVlsb:
    @staticmethod
    def size(width, height, stride=0):
        if stride < width:
            stride = width
        return stride * (height // 8 + (1 if height % 8 != 0 else 0))

    def __init__(self, data, width, height, stride=0):
        self.width = width
        self.height = height
        self.stride = stride if stride >= width else width
        self.size = MonoVlsb.size(width, height, self.stride)
        self.data = data

    def name(self):
        return "monovlsb"

    def set_bitmap_data(self, data):
        self.data = data

    def set_pixel(self, x, y, color):
        index = (y >> 3) * self.stride + x
        offset = y & 0x07
        if color != 0:
            color = 1
        self.data[index] = (self.data[index] & ~(0x01 << offset)) | (color << offset)

    def get_pixel(self, x, y):
        return (self.data[(y >> 3) * self.stride + x] >> (y & 0x07)) & 0x01

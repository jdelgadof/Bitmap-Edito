class MonoHlsb:
    @staticmethod
    def size(width, height, stride=0):
        if stride < width:
            stride = width
        return height * (stride // 8 + (1 if stride % 8 != 0 else 0))

    def __init__(self, data, width, height, stride=0):
        self.width = width
        self.height = height
        self.stride = stride if stride >= width else width
        if self.stride % 8 != 0:
            self.stride = (self.stride // 8 + 1) * 8
        self.size = MonoHlsb.size(width, height, self.stride)
        self.data = data

    def name(self):
        return "monohlsb"

    def set_bitmap_data(self, data):
        self.data = data

    def set_pixel(self, x, y, color):
        index = (x + y * self.stride) >> 3
        offset = 7 - (x & 0x07)
        self.data[index] = (self.data[index] & ~(0x01 << offset)) | ((color != 0) << offset)

    def get_pixel(self, x, y):
        index = (x + y * self.stride) >> 3
        offset = 7 - (x & 0x07)
        return (self.data[index] >> offset) & 0x01

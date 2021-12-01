from romhacking.common import ROM as GenericROM


class ROM(GenericROM):
    """
        Class to manipulate Nintendo Entertainment System / Famicom / Famicom Disk System
        ROM files
    """

    def __init__(self, filename, endian=None):
        super(ROM, self).__init__(filename, endian)

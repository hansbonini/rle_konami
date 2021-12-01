import sys

from romhacking.common import BitArray, RingBuffer, Compression, LZSS, RLE

class RLEKONAMI(RLE):
    """
        Class to manipulate RLEKONAMI Compression

        Games where this compression is found:
            - [FDS] Dracula II - Noroi no Fuuin
            - [FDS] Ai Senshi Nicol
            - [FDS] Rampart
            - [NES] Akumajou Densetsu
            - [NES] Akumajou Dracula
            - [NES] Akumajou Special - Boku Dracula-kun
            - [NES] Adventures of Bayou Billy
            - [NES] Batman Returns
            - [NES] Bucky O'Hare
            - [NES] Blades of Steel
            - [NES] Castlevania II - Simon's Quest
            - [NES] Castlevania III - Dracula's Curse
            - [NES] Contra
            - [NES] Contra Force
            - [NES] Double Dribble
            - [NES] Ganbare Goemon! - Karakuri Douchuu
            - [NES] Ganbare Goemon 2
            - [NES] Ganbare Goemon Gaiden - Kieta Ougon Kiseru
            - [NES] Gradius II
            - [NES] Gyruss
            - [NES] Jackal
            - [NES] Konami Hyper Soccer
            - [NES] Life Force
            - [NES] Lone Ranger
            - [NES] Parodius
            - [NES] Q-bert
            - [NES] Rampart
            - [NES] Roller Games
            - [NES] Snake's Revenge
            - [NES] Skate or Die
            - [NES] Ski or Die
            - [NES] Stinger
            - [NES] Super Contra
            - [NES] Teenage Mutant Ninja Turtles
            - [NES] Teenage Mutant Ninja Turtles II - The Arcade Game
            - [NES] Teenage Mutant Ninja Turtles III - The Manhattan Project (USA).
            - [NES] Top Gun
            - [NES] Tiny Toon Adventures 2 - Trouble in Wackyland
            - [NES] Wai Wai World
            - [NES] Wai Wai World 2 - SOS!! Paseri Jou

    """
    
    signature = b"\xB1\x00\xC9\xFF\xF0"
    #signature = b"\x29\x7F\x85\x02\xA0\x01\xB1\x00"

    def __init__(self, input_data):
        super(RLEKONAMI, self).__init__(input_data)

    def decompress(self, offset=0, size=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._output = bytearray()
        while True:
            try:
                control = self.DATA.read_8()
                if control == 0xFF:
                    break
                elif control <= 0x80:
                    _readed = self.DATA.read_8()
                    for i in range(control):
                        self._output.append(_readed)
                else:
                    for i in range(control-0x80):
                        self._output.append(self.DATA.read_8())
            except:
                break
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '<'
        self._buffer = bytearray()
        self._output = bytearray()
        self._encoded = 0
        self.MIN_LENGTH = 0x2
        while self._encoded < self.DATA.SIZE:
            rle_match = self.find_best_rle_match(slimit=0x80)
            if rle_match > self.MIN_LENGTH:
                if len(self._buffer) > 0:
                    self.flush_raw()
                self._output.append(rle_match)
                for i in range(rle_match):
                    _readed = self.DATA.read_8()
                self._output.append(_readed)
                self._encoded += rle_match
            else:
                self._buffer.append(self.DATA.read_8())
                if len(self._buffer) > 0x80:
                    self.flush_raw()
                self._encoded += 1                
        self.flush_raw()
        self._output.append(0xFF)
        return self._output
    
    def flush_raw(self):
        length = len(self._buffer)
        self._output.append(0x80+length)
        self._output += self._buffer[0:length]
        self._buffer=bytearray()


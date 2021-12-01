#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import sys
import textwrap
from os import SEEK_CUR, SEEK_END, SEEK_SET
from romhacking.common import TBL
from nes.common import ROM
from nes.data_compression import *
from utils.common import *

cmd = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent('''\
            [NES] KONAMI Compressor / Decompressor
            ----------------------------------------------
            Tool for decompress and recompress graphics
            from games developed by KONAMI using RLE
            algorithm.
            ----------------------------------------------
            List of know compatible games;
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
            ----------------------------------------------
            For decompress:
                python main.py D rom decompressed_file offset
            For compress:
                python main.py C rom decompressed_file offset_to_be_inserted_in_rom
        ''')
  )


def decompress(rom_path, decompressed_data_path, codec=None, *args):
    rom = ROM(rom_path, 'msb')
    algorithm = None
    for compression in FindAllSubclasses(Compression):
        if compression[1] == codec:
            algorithm = compression[0](rom)
    if algorithm:
        out = open(decompressed_data_path, 'wb')
        data = algorithm.decompress(*args)
        data_len = len(data)
        print('[INFO] Decompressed Size: {:08x}'.format(data_len))
        out.seek(0, 0)
        out.write(data)
        out.close()
        print('[INFO] Finished!')

def compress(rom_path, decompressed_data_path, codec=None, *args):
    offset = args[0]
    rom = open(rom_path, 'r+b')
    input = ROM(decompressed_data_path, 'msb')
    algorithm = None
    for compression in FindAllSubclasses(Compression):
        if compression[1] == codec:
            algorithm = compression[0](input)
    if algorithm:
        data = algorithm.compress()
        data_len = len(data)
        print('[INFO] Compressed Size: {:08x}'.format(data_len))
        rom.seek(offset, 0)
        rom.write(data)
        rom.close()
        input.close()
        print('[INFO] Finished!')

if __name__ == "__main__":

    cmd.add_argument(
        'option',
        nargs='?',
        type=str,
        default=None,
        help='"C" for Compression / "D" for Decompression'
    )

    cmd.add_argument(
        'rom',
        nargs='?',
        type=argparse.FileType('rb'),
        default=sys.stdin,
        help='Nintendo Entertainment System / Famicom / Famicom Disk System ROM'
    )

    cmd.add_argument(
        'output',
        nargs='?',
        type=str,
        default=None,
        help='Decompressed file.'
    )

    cmd.add_argument(
        'offset',
        nargs='?',
        type=lambda x: int(x, 0),
        default=None,
        help='Offset'
    )

    args = cmd.parse_args()
    print(cmd.description)
    if args.option not in ['C','D']:
        print('[ERROR] Option must be "C" for Compression or "D" for Decompression')
        sys.exit(0)
    if args.rom.name == '<stdin>':
        print('[ERROR] An Nintendo Entertainment System / Famicom / Famicom Disk System must be specified')
        sys.exit(0)
    if args.output == None:
        print('[ERROR] An Output File must be specified')
        sys.exit(0)
    if args.offset == None:
        print('[ERROR] An Offset must be specified')
        sys.exit(0)
    if (args.option == 'D'):
        print('[INFO] Decompressing at {:08x}...'.format(args.offset))
        decompress(args.rom.name, args.output, 'RLEKONAMI', args.offset)
    else:
        print('[INFO] Compressing and inserting at {:08x}...'.format(args.offset))
        compress(args.rom.name, args.output, 'RLEKPNAMI', args.offset)
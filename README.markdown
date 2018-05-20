# Hexer

Copyright © 2018 Chris Hall

## Introduction

**Hexer** is a command line tool for generating SVG hex grids.

## Installing

Check out the project, install any required dependencies, and run `hexer.py`.

```sh
pip install < requirements.txt
./hexer.py -h
```

## Usage

```sh
./hexer.py -h
usage: hexer.py [-h] [-d DPI] [-s {hexes,crowsfeet}] [-o OUTPUT] width height hex_size

# Generate a 1920 x 1440 pixel grid with 50 pixel hexes:
./hexer.py 1920 1440 50 -o output.svg

# Generate a 36" x 48" grid with 2" hexes, at 150 DPI:
./hexer.py 36 48 2 -d 150 -o output.svg

# Generate a grid with crowsfeet instead of hexes:
./hexer.py 36 48 2 -d 150 -s crowsfeet -o output.svg
```

## License

This program is distributed under the MIT license.

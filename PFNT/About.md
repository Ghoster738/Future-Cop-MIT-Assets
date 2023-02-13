# Info
These files where created from Ghoster738's Python tool.
Each font is drawn with Gimp, and the files where created
using Python to encode to PFNT files.
Each glyph had coordinates entered by hand.

![Demonstration](Usage.png?raw=true "In the top right character displays the font in action.")

# Windows and Macintosh
These files are basically the same. However, the Macintosh version is encoded in big endian.
While the Windows version is encodded in little endian.
For this reason only the Windows version is used in the game. Macintosh is reserved for
future unit testing. In the 'BM Font' folder, the corresponding font is called 'computer.'

![Computer Font](BM%20Font/computer.png?raw=true "This is the computer font.")

# Playstation
This file is to hold important characters. The gamepad characters are included in this font.
However, It is found that the PS1 font of other Future Cop replaces character like '#' with
the square symbol. Thus, this kind of font is needed.

![Playstation Font](BM%20Font/playstation.png?raw=true "This is the computer font.")

# BM Font
This contains the decoded fonts. It can be read by more modern software because of this.

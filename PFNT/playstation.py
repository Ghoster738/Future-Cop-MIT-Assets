import PFNTBuilder

font = {}

font[ord(' ')] = PFNTBuilder.Font( 5, 5, 216, 7, 6 )

for abc in range( ord('A'), ord('Z') + 1 ):
    font[ abc ] = PFNTBuilder.Font()

    font[ abc ].width = 5
    font[ abc ].height = 5
    font[ abc ].left = 6 * (abc - ord('A'))
    font[ abc ].top = 1
    font[ abc ].x_advance = 6

for abc in range( ord('0'), ord('9') + 1 ):
    font[ abc ] = PFNTBuilder.Font()

    font[ abc ].width = 5
    font[ abc ].height = 5
    font[ abc ].left = 156 + 6 * (abc - ord('0'))
    font[ abc ].top = 1
    font[ abc ].x_advance = 6

for abc in range( ord('a'), ord('z') + 1 ):
    font[ abc ] = PFNTBuilder.Font()

    font[ abc ].width = 5
    font[ abc ].height = 5
    font[ abc ].left = 6 * (abc - ord('a'))
    font[ abc ].top = 1
    font[ abc ].x_advance = 6

font[ord('!')] = PFNTBuilder.Font( 5, 5, 216,  1, 6 )
font[ord('#')] = PFNTBuilder.Font( 5, 5, 222,  1, 6 )
font[ord('$')] = PFNTBuilder.Font( 5, 5, 228,  1, 6 )
font[ord('%')] = PFNTBuilder.Font( 5, 5, 234,  1, 6 )
font[ord('^')] = PFNTBuilder.Font( 5, 5, 240,  1, 6 )
font[ord('&')] = PFNTBuilder.Font( 5, 5, 246,  1, 6 )

font[ord('-')]  = PFNTBuilder.Font( 5, 5,   0, 7, 6 )
font[ord('_')]  = PFNTBuilder.Font( 5, 5,   6, 7, 6 )
font[ord('+')]  = PFNTBuilder.Font( 5, 5,  12, 7, 6 )
font[ord('=')]  = PFNTBuilder.Font( 5, 5,  18, 7, 6 )
font[ord('{')]  = PFNTBuilder.Font( 5, 5,  24, 7, 6 )
font[ord('}')]  = PFNTBuilder.Font( 5, 5,  30, 7, 6 )
font[ord('[')]  = PFNTBuilder.Font( 5, 5,  36, 7, 6 )
font[ord(']')]  = PFNTBuilder.Font( 5, 5,  42, 7, 6 )
font[ord(':')]  = PFNTBuilder.Font( 5, 5,  48, 7, 6 )
font[ord(';')]  = PFNTBuilder.Font( 5, 5,  54, 7, 6 )
font[ord('\'')] = PFNTBuilder.Font( 5, 5,  60, 7, 6 )
font[ord('"')]  = PFNTBuilder.Font( 5, 5,  66, 7, 6 )
font[ord('<')]  = PFNTBuilder.Font( 5, 5,  72, 7, 6 )
font[ord('>')]  = PFNTBuilder.Font( 5, 5,  78, 7, 6 )
font[ord(',')]  = PFNTBuilder.Font( 5, 5,  84, 7, 6 )
font[ord('.')]  = PFNTBuilder.Font( 5, 5,  90, 7, 6 )
font[ord('?')]  = PFNTBuilder.Font( 5, 5,  96, 7, 6 )
font[ord('\\')] = PFNTBuilder.Font( 5, 5, 102, 7, 6 )
font[ord('|')]  = PFNTBuilder.Font( 5, 5, 108, 7, 6 )
font[ord('/')]  = PFNTBuilder.Font( 5, 5, 114, 7, 6 )
font[ord('~')]  = PFNTBuilder.Font( 5, 5, 120, 7, 6 )
font[ord('`')]  = PFNTBuilder.Font( 5, 5, 126, 7, 6 )

font[ord('(')]  = PFNTBuilder.Font( 5, 5, 132, 7, 6 )
font[ord(')')]  = PFNTBuilder.Font( 5, 5, 138, 7, 6 )

# 0x7F is the DELete key.
font[0x7F] = PFNTBuilder.Font( 5, 5, 144, 7, 6 )

# The only reason these characters were implemented is because the PS1 CD that I have supports German.
# I would have created French hatted characters if they existed
# 0xC4 is the uppercase German hatted A.
font[0xC4] = PFNTBuilder.Font( 5, 5, 198, 7, 6 )
# 0xE4 is the lowercase German hatted a.
font[0xE4] = PFNTBuilder.Font( 5, 5, 198, 7, 6 )
# 0xD6 is the uppercase German hatted O.
font[0xD6] = PFNTBuilder.Font( 5, 5, 204, 7, 6 )
# 0xE4 is the lowercase German hatted o.
font[0xF6] = PFNTBuilder.Font( 5, 5, 204, 7, 6 )
# 0xD6 is the uppercase German hatted u.
font[0xDC] = PFNTBuilder.Font( 5, 5, 210, 7, 6 )
# 0xE4 is the lowercase German hatted u.
font[0xFC] = PFNTBuilder.Font( 5, 5, 210, 7, 6 )

# The '#' char is the square button symbol.
font[35]  = PFNTBuilder.Font( 5,  5, 174, 7, 6 )
# The '~' char is the triangle button symbol.
font[126] = PFNTBuilder.Font( 5, 5, 180, 7, 6 )
# The '@' char is the circle button symbol.
font[64] = PFNTBuilder.Font( 5, 5, 186, 7, 6 )
# The '*' char is the X button symbol.
font[42] = PFNTBuilder.Font( 5, 5, 192, 7, 6 )

# The '$' char is the "<- ->"
font[36] = PFNTBuilder.Font( 11, 5, 162, 7, 12 )
# The '^' char is the up and down symbol.
font[94] = PFNTBuilder.Font( 11, 5, 150, 7, 12 )

PFNTBuilder.writeFNTFile( "playstation.png", "playstation.fnt", font, PFNTBuilder.Platform.Playstation )

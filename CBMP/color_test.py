from PIL import Image # 9.4.0-2
import CBMPBuilder

def createTestSubImage( blue_level : int, semi_transparent : bool, flip_horz : bool, flip_vertical : bool ):
    size = width, height = 32, 32

    half = 255

    if semi_transparent:
        half = 128

    image = Image.new( "RGBA", size )

    for next_y in range(0, 32):
        for next_x in range(0, 32):
            position = x, y = next_x, next_y

            pixel = image.putpixel( position, (min(next_x * 8, 255), min(next_y * 8, 255), min(blue_level * 8, 255), half ) )

    if flip_horz == True:
        image = image.transpose( Image.Transpose.FLIP_LEFT_RIGHT )
    if flip_vertical == True:
        image = image.transpose( Image.Transpose.FLIP_TOP_BOTTOM )

    return image

def embbedImage( primary_image : Image, source_image : Image, x : int, y : int ):
    position = (x, y)

    primary_image.paste( source_image, position )

def createTestImage():
    size = width, height = 256, 256

    image = Image.new( "RGBA", size )

    for i in range(0, 4):
        embbedImage( image, createTestSubImage( i * 8 + 0, False, False, (i % 2) == 1 ),   0, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 1, False, True,  (i % 2) == 1 ),  32, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 2, False, False, (i % 2) == 1 ),  64, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 3, False, True,  (i % 2) == 1 ),  96, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 4, False, False, (i % 2) == 1 ), 128, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 5, False, True,  (i % 2) == 1 ), 160, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 6, False, False, (i % 2) == 1 ), 192, i * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 7, False, True,  (i % 2) == 1 ), 224, i * 32 )

    for i in range(0, 4):
        embbedImage( image, createTestSubImage( i * 8 + 0, True, False, (i % 2) == 1 ),   0, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 1, True, True,  (i % 2) == 1 ),  32, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 2, True, False, (i % 2) == 1 ),  64, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 3, True, True,  (i % 2) == 1 ),  96, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 4, True, False, (i % 2) == 1 ), 128, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 5, True, True,  (i % 2) == 1 ), 160, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 6, True, False, (i % 2) == 1 ), 192, (i + 4) * 32 )
        embbedImage( image, createTestSubImage( i * 8 + 7, True, True,  (i % 2) == 1 ), 224, (i + 4) * 32 )

    return image

# Write the color test texture
color_test = createTestImage()

CBMPBuilder.writeCBMPFile( color_test, "windows_colors.cbmp", CBMPBuilder.Platform.Windows )
CBMPBuilder.writeCBMPFile( color_test, "macintosh_colors.cbmp", CBMPBuilder.Platform.Macintosh )
# Playstation strictly uses 8 bit indexes for colors, so a cbmp would not encompass the full colors of 16 bits.

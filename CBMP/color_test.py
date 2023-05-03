from PIL import Image # 9.4.0-2
import CBMPBuilder

def createTestSubImage( blue_level : int, semi_transparent : bool ):
    size = width, height = 32, 32

    half = 255

    if semi_transparent:
        half = 128

    image = Image.new( "RGBA", size )

    for next_y in range(0, 32):
        for next_x in range(0, 32):
            position = x, y = next_x, next_y

            pixel = image.putpixel( position, (min(next_x * 8, 255), min(next_y * 8, 255), min(blue_level * 8, 255), half ) )

    return image

def embbedImage( primary_image : Image, source_image : Image, x : int, y : int ):
    position = (x, y)

    primary_image.paste( source_image, position )

def createTestImage():
    size = width, height = 256, 256

    image = Image.new( "RGBA", size )

    for i in range(0, 8):
        embbedImage( image, createTestSubImage( i * 4 + 0, False ),   0, i * 32 )
        embbedImage( image, createTestSubImage( i * 4 + 0,  True ),  32, i * 32 )

        embbedImage( image, createTestSubImage( i * 4 + 1, False ),  64, i * 32 )
        embbedImage( image, createTestSubImage( i * 4 + 1,  True ),  96, i * 32 )

        embbedImage( image, createTestSubImage( i * 4 + 2, False ), 128, i * 32 )
        embbedImage( image, createTestSubImage( i * 4 + 2,  True ), 160, i * 32 )

        embbedImage( image, createTestSubImage( i * 4 + 3, False ), 192, i * 32 )
        embbedImage( image, createTestSubImage( i * 4 + 3,  True ), 224, i * 32 )

    return image

# Write the color test texture
color_test = createTestImage()

CBMPBuilder.writeCBMPFile( color_test, "windows_colors.cbmp", CBMPBuilder.Platform.Windows )
CBMPBuilder.writeCBMPFile( color_test, "macintosh_colors.cbmp", CBMPBuilder.Platform.Macintosh )
# Playstation strictly uses 8 bit indexes for colors, so a cbmp would not encompass the full colors of 16 bits.

import COBJBuilder
import zlib

def generateModel(animation_amount: int):
    model = COBJBuilder.Model()

    face = COBJBuilder.Primitive()
    face.setTypeStar(0, 0, [0xff, 0x00, 0x00])
    face.setStarVertexAmount(4)

    if animation_amount > 0:
        face.setStarAnimationData(True)
        face.getStarAnimationData().setColor( (0x00, 0xff, 0xff) )
        face.getStarAnimationData().setSpeedFactor( 2 )

    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeStar(1, 0, [0x00, 0xff, 0x00])
    face.setStarVertexAmount(8)

    if animation_amount > 1:
        face.setStarAnimationData(True)
        face.getStarAnimationData().setColor( (0xff, 0x00, 0xff) )
        face.getStarAnimationData().setSpeedFactor( 3 )

    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeStar(2, 0, [0x00, 0x00, 0xff])
    face.setStarVertexAmount(12)

    if animation_amount > 2:
        face.setStarAnimationData(True)
        face.getStarAnimationData().setColor( (0xff, 0xff, 0x00) )
        face.getStarAnimationData().setSpeedFactor( 4 )

    model.appendPrimitive(face)

    model.allocateVertexBuffers(1, 3, 0, 1, 0, 0)

    positionBuffer = model.getPositionBuffer(0)
    positionBuffer.setValue(0, ( 0,  64,  0))
    positionBuffer.setValue(1, ( 0, 192,  0))
    positionBuffer.setValue(2, ( 0, 320,  0))

    lengthBuffer = model.getLengthBuffer(0)
    lengthBuffer.setValue(0, 64)

    model.setupChildVertices()

    return model

def test():
    result = True

    expected_crc32 = 0xba1e9e98
    crc32 = zlib.crc32(generateModel(0).makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != expected_crc32:
        result = False
        print("Star failed with", hex(crc32), "expected", hex(expected_crc32))

    expected_crc32 = 0x3463d6d5
    crc32 = zlib.crc32(generateModel(1).makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != expected_crc32:
        result = False
        print("Star failed with", hex(crc32), "expected", hex(expected_crc32))

    expected_crc32 = 0x2f6e2b08
    crc32 = zlib.crc32(generateModel(3).makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != expected_crc32:
        result = False
        print("Star failed with", hex(crc32), "expected", hex(expected_crc32))

    return result

if __name__ == "__main__":
    test()
    generateModel(0).makeFile("stars.cobj", COBJBuilder.ModelFormat.WINDOWS)
    generateModel(1).makeFile("stars_animation.cobj", COBJBuilder.ModelFormat.WINDOWS)
    generateModel(3).makeFile("stars_all_animations.cobj", COBJBuilder.ModelFormat.WINDOWS)

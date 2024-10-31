import COBJBuilder
import zlib

def generateModel():
    model = COBJBuilder.Model()

    face = COBJBuilder.Primitive()
    face.setTypeStar(0, 0, [0xff, 0x00, 0x00])
    face.setStarVertexAmount(4)
    model.appendPrimitive(face)
    face = COBJBuilder.Primitive()
    face.setTypeStar(1, 0, [0x00, 0xff, 0x00])
    face.setStarVertexAmount(8)
    model.appendPrimitive(face)
    face = COBJBuilder.Primitive()
    face.setTypeStar(2, 0, [0x00, 0x00, 0xff])
    face.setStarVertexAmount(12)
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
    crc32 = zlib.crc32(generateModel().makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != expected_crc32:
        result = False
        print("Star failed with", hex(crc32), "expected", hex(expected_crc32))

    return result

if __name__ == "__main__":
    test()
    generateModel().makeFile("star.cobj", COBJBuilder.ModelFormat.WINDOWS)

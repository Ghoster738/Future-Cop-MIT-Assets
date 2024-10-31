import COBJBuilder
import zlib

def generateModel():
    model = COBJBuilder.Model()

    face = COBJBuilder.Primitive()
    face.setTypeStar(0, 0, [0, 0xff, 0])
    face.setStarVertexAmount(4)
    model.appendPrimitive(face)

    model.allocateVertexBuffers(1, 1, 0, 1, 0, 0)

    positionBuffer = model.getPositionBuffer(0)
    positionBuffer.setValue(0, ( 0,  64,  0))

    lengthBuffer = model.getLengthBuffer(0)
    lengthBuffer.setValue(0, 64)

    model.setupChildVertices()

    return model

def test():
    result = True

    expected_crc32 = 0x88eb5888
    crc32 = zlib.crc32(generateModel().makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != expected_crc32:
        result = False
        print("Star failed with", hex(crc32), "expected", hex(expected_crc32))

    return result

if __name__ == "__main__":
    test()
    generateModel().makeFile("star.cobj", COBJBuilder.ModelFormat.WINDOWS)

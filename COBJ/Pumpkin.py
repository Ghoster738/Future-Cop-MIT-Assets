import COBJBuilder
import zlib

def generateModel():
    model = COBJBuilder.Model()

    orange = COBJBuilder.FaceType() # Dark Orange
    orange.setVertexColor(True, [99, 55, 0])
    model.appendFaceType(orange)
    black = COBJBuilder.FaceType() # Blue
    black.setVertexColor(True, [0, 0, 10])
    model.appendFaceType(black)

    face = COBJBuilder.Primitive()
    face.setTypeQuad([2, 3, 1, 0], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(0) # Orange index.
    model.appendPrimitive(face)
    face = COBJBuilder.Primitive()
    face.setTypeQuad([4, 5, 7, 6], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(0) # Orange index.
    model.appendPrimitive(face)
    face = COBJBuilder.Primitive()
    face.setTypeQuad([0, 1, 5, 4], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(0) # Orange index.
    model.appendPrimitive(face)
    face = COBJBuilder.Primitive()
    face.setTypeQuad([5, 1, 3, 7], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(0) # Orange index.
    model.appendPrimitive(face)
    face = COBJBuilder.Primitive()
    face.setTypeQuad([6, 2, 0, 4], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(0) # Orange index.
    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([8, 9, 10], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(1) # Black index.
    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([13, 12, 11], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(1) # Black index.
    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([14, 15, 16], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(1) # Black index.
    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([17, 18, 19], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setMaterialBitfield(2)
    face.setFaceTypeIndex(1) # Black index.
    model.appendPrimitive(face)

    model.allocateVertexBuffers(1, 20, 0, 0, 0, 0)

    positionBuffer = model.getPositionBuffer(0)

    span = 256

    positionBuffer.setValue(0, ( span,  span,  span))
    positionBuffer.setValue(1, ( span,  span, -span))
    positionBuffer.setValue(2, ( span, -span,  span))
    positionBuffer.setValue(3, ( span, -span, -span))
    positionBuffer.setValue(4, (-span,  span,  span))
    positionBuffer.setValue(5, (-span,  span, -span))
    positionBuffer.setValue(6, (-span, -span,  span))
    positionBuffer.setValue(7, (-span, -span, -span))

    positionBuffer.setValue( 8, (int( (3 * span) / 4),  int((3 * span) / 4),  span + 16))
    positionBuffer.setValue( 9, (int( (1 * span) / 4),  int((3 * span) / 4),  span + 16))
    positionBuffer.setValue(10, (int( (1 * span) / 4),  int((1 * span) / 4),  span + 16))

    positionBuffer.setValue(11, (int(-(3 * span) / 4), int((3 * span) / 4),  span + 16))
    positionBuffer.setValue(12, (int(-(1 * span) / 4), int((3 * span) / 4),  span + 16))
    positionBuffer.setValue(13, (int(-(1 * span) / 4), int((1 * span) / 4),  span + 16))

    positionBuffer.setValue(14, (int( (1 * span) / 8), int((1 *  span) / 8), span + 16))
    positionBuffer.setValue(15, (int(-(1 * span) / 8), int((1 *  span) / 8), span + 16))
    positionBuffer.setValue(16, (                   0, int((1 * -span) / 8), span + 16))

    positionBuffer.setValue(17, (int( (3 * span) / 4),  int((1 * -span) / 4),  span + 16))
    positionBuffer.setValue(18, (int(-(3 * span) / 4),  int((1 * -span) / 4),  span + 16))
    positionBuffer.setValue(19, (                  0,   int((3 * -span) / 4),  span + 16))

    model.setupChildVertices()

    return model

def test():
    result = True

    expected_crc32 = 0x8deb1559
    crc32 = zlib.crc32(generateModel().makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != expected_crc32:
        result = False
        print("Pumpkin failed with", hex(crc32), "expected", hex(expected_crc32))

    return result

if __name__ == "__main__":
    test()
    generateModel().makeFile("pumpkin.cobj", COBJBuilder.ModelFormat.WINDOWS)

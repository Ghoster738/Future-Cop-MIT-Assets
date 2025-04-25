import COBJBuilder
import zlib

def generateModel(cbmp_id: int):
    model = COBJBuilder.Model()

    model.setEnvironmentMapSemiTransparent(False)

    testFaceTypes = []
    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0, 0xff, 0])
    model.appendFaceType(testFaceTypes[-1])

    testFaceTypes.clear()

    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0x7f, 0x7f, 0x7f])

    for i in testFaceTypes:
        i.setTexCoords(True, [[0, 0], [0, 0xff], [0xff, 0xff], [0xff, 0]])

        i.setBMPID(cbmp_id)

        model.appendFaceType(i)

    face = COBJBuilder.Primitive()
    face.setTypeQuad([3, 2, 1, 0], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setFaceTypeIndex(0)
    model.appendPrimitive(face)

    number_of_vertices = 4 # quad vertex count multipled by all known primitive types

    model.allocateVertexBuffers(128, number_of_vertices, 1, 0, 0, 0)

    for i in range(0, 128):
        positionBuffer = model.getPositionBuffer(i)

        positionBuffer.setValue(0, (-128, i, -128))
        positionBuffer.setValue(1, ( 128, i, -128))
        positionBuffer.setValue(2, ( 128, i,  128))
        positionBuffer.setValue(3, (-128, i,  128))

        positionBuffer = model.getNormalBuffer(i)
        positionBuffer.setValue(0, (0, 0, 4096))

    model.setupChildVertices()

    return model

def generate():
    generateModel(1).makeFile("animation.cobj", COBJBuilder.ModelFormat.WINDOWS)

def test():
    result = True

    crc32 = zlib.crc32(generateModel(1).makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != 0:
        result = False
        print("failed with", hex(crc32), "expected", hex(0))

    return result

if __name__ == "__main__":
    test()
    generate()

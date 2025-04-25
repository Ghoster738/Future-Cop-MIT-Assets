import COBJBuilder
import zlib

def generateModel(cbmp_id: int):
    model = COBJBuilder.Model()

    model.setEnvironmentMapSemiTransparent(False)

    testFaceTypes = []
    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0, 0xff, 0])
    model.appendFaceType(testFaceTypes[-1])

    for i in range(0, 8):
        testFaceTypes.append( COBJBuilder.FaceType() )
        testFaceTypes[-1].setVertexColor(True, [31 * (8 - i), 0, 31 * i])
        model.appendFaceType(testFaceTypes[-1])

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([2, 1, 0], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setFaceTypeIndex(0)
    model.appendPrimitive(face)

    for i in range(0, 8):
        face = COBJBuilder.Primitive()
        face.setTypeTriangle([3 + i, 12 + i, 4 + i], [0, 0, 0])
        face.setTexture(False)
        face.setReflective(False)
        face.setFaceTypeIndex(1 + i)
        model.appendPrimitive(face)

    base_triangle_vertex_amount = 3
    root_triangles_vertex_amount = 9
    top_triangles_vertex_amount = 8
    number_of_vertices = base_triangle_vertex_amount + root_triangles_vertex_amount + top_triangles_vertex_amount

    model.allocateVertexBuffers(256, number_of_vertices, 1, 0, 0, 0)

    for i in range(0, 256):
        positionBuffer = model.getPositionBuffer(i)

        positionBuffer.setValue(0, (-256, 64, 0))
        positionBuffer.setValue(1, ( 256,  0, 0))
        positionBuffer.setValue(2, ( 256, 64, 0))

        for r in range(0, root_triangles_vertex_amount):
            positionBuffer.setValue(base_triangle_vertex_amount + r, (-256 + 64 * r, 80, 0))

        for r in range(0, top_triangles_vertex_amount):
            level = 80

            if ((1 << r) & i) != 0:
                level = 256

            positionBuffer.setValue(base_triangle_vertex_amount + root_triangles_vertex_amount + r, (-224 + 64 * r, level, 0))

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

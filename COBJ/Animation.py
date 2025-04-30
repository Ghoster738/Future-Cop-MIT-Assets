import COBJBuilder
import zlib

def generateModel( digit_amount : int, width : int = 256):
    color_difference = int(255 / digit_amount)

    base_digit_width = int((2 * width) / digit_amount)
    base_digit_position = -width + int(base_digit_width / 2)

    base_triangle_vertex_amount  = 3
    root_triangles_vertex_amount = digit_amount + 1
    top_triangles_vertex_amount  = digit_amount
    number_of_vertices = base_triangle_vertex_amount + root_triangles_vertex_amount + top_triangles_vertex_amount

    model = COBJBuilder.Model()

    model.setEnvironmentMapSemiTransparent(False)

    testFaceTypes = []
    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0, 0xff, 0])
    model.appendFaceType(testFaceTypes[-1])

    for i in range(0, digit_amount):
        testFaceTypes.append( COBJBuilder.FaceType() )
        testFaceTypes[-1].setVertexColor(True, [color_difference * (digit_amount - i), 0, color_difference * i])
        model.appendFaceType(testFaceTypes[-1])

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([2, 1, 0], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setFaceTypeIndex(0)
    model.appendPrimitive(face)

    face = COBJBuilder.Primitive()
    face.setTypeTriangle([0, 1, 2], [0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setFaceTypeIndex(0)
    model.appendPrimitive(face)

    for i in range(0, digit_amount):
        face = COBJBuilder.Primitive()
        face.setTypeTriangle([3 + i, 4 + digit_amount + i, 4 + i], [0, 0, 0])
        face.setTexture(False)
        face.setReflective(False)
        face.setFaceTypeIndex(1 + i)
        model.appendPrimitive(face)

        face = COBJBuilder.Primitive()
        face.setTypeTriangle([4 + i, 4 + digit_amount + i, 3 + i], [0, 0, 0])
        face.setTexture(False)
        face.setReflective(False)
        face.setFaceTypeIndex(1 + i)
        model.appendPrimitive(face)

    model.allocateVertexBuffers(256, number_of_vertices, 1, 0, 0, 0)

    for i in range(0, 256):
        positionBuffer = model.getPositionBuffer(i)

        positionBuffer.setValue(0, (-width, 64, 0))
        positionBuffer.setValue(1, ( width,  0, 0))
        positionBuffer.setValue(2, ( width, 64, 0))

        for r in range(0, root_triangles_vertex_amount):
            positionBuffer.setValue(base_triangle_vertex_amount + r, (-width + base_digit_width * r, 80, 0))

        for r in range(0, top_triangles_vertex_amount):
            level = 80

            if ((1 << r) & i) != 0:
                level = 256

            positionBuffer.setValue(base_triangle_vertex_amount + root_triangles_vertex_amount + r, (base_digit_position + base_digit_width * r, level, 0))

        positionBuffer = model.getNormalBuffer(i)
        positionBuffer.setValue(0, (0, 0, 4096))

    model.setupChildVertices()

    return model

def generate():
    generateModel(8).makeFile("animation.cobj", COBJBuilder.ModelFormat.WINDOWS)

def test():
    result = True

    crc32 = zlib.crc32(generateModel(8).makeResource(COBJBuilder.ModelFormat.WINDOWS))

    if crc32 != 0xf250b466:
        result = False
        print("failed with", hex(crc32), "expected", hex(0xf250b466))

    return result

if __name__ == "__main__":
    test()
    generate()

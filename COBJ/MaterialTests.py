import COBJBuilder
import zlib

def generateModel(cbmp_id: int, isTextured: bool, hasTextureAnimationChunk: bool, isReflective : bool, isReflectiveSemiTransparent : bool):
    model = COBJBuilder.Model()

    model.setEnvironmentMapSemiTransparent(isReflectiveSemiTransparent)

    testFaceTypes = []
    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0, 0xff, 0])
    model.appendFaceType(testFaceTypes[-1])

    testFaceTypes.clear()

    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0x7f, 0x7f, 0x7f])

    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0x7f, 0, 0])

    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0, 0x7f, 0])

    testFaceTypes.append( COBJBuilder.FaceType() )
    testFaceTypes[-1].setVertexColor(True, [0, 0, 0x7f])

    for i in testFaceTypes:
        if not hasTextureAnimationChunk:
            i.setTexCoords(True, [[0, 0], [0, 0xff], [0xff, 0xff], [0xff, 0]])
        else:
            i.setTexFrameDurationInSeconds(1.0)
            i.setTexCoordFrameCount(4)

            for x in range(2):
                for y in range(2):
                    i.setTexCoords(True, [[x * 127, y * 127], [x * 127, (y + 1) * 127], [(x + 1) * 127, (y + 1) * 127], [(x + 1) * 127, y * 127]], 2 * x + y)

        i.setBMPID(cbmp_id)
        model.appendFaceType(i)

    face = COBJBuilder.Primitive()
    face.setTypeQuad([3, 2, 1, 0], [0, 0, 0, 0])
    face.setTexture(False)
    face.setReflective(False)
    face.setFaceTypeIndex(0)
    model.appendPrimitive(face)

    number_of_test_face_types = 4

    number_of_test_quads = 16

    for t in range(0, number_of_test_face_types):
        for i in range(0, number_of_test_quads):
            if not isTextured and (i == 0 or i == 1 or i == 4 or i == 5 or i == 8 or i == 9 or i == 14 or i == 15):
                continue

            face = COBJBuilder.Primitive()
            face.setTypeQuad([0 + 4 * (i + t * number_of_test_quads), 1 + 4 * (i + t * number_of_test_quads), 2 + 4 * (i + t * number_of_test_quads), 3 + 4 * (i + t * number_of_test_quads)], [0, 0, 0, 0])
            face.setTexture(isTextured)
            face.setReflective(isReflective)
            face.setMaterialBitfield(i)
            face.setFaceTypeIndex(t + 1)
            model.appendPrimitive(face)

    number_of_vertices = 4 * number_of_test_quads * number_of_test_face_types # quad vertex count multipled by all known primitive types

    model.allocateVertexBuffers(1, number_of_vertices, 1, 0, 0, 0)

    positionBuffer = model.getPositionBuffer(0)

    for t in range(0, number_of_test_face_types):
        for i in range(0, number_of_test_quads):
            positionBuffer.setValue(0 + 4 * (i + t * number_of_test_quads), (-64 + 128 * i,   0 + 150 * t, 0))
            positionBuffer.setValue(1 + 4 * (i + t * number_of_test_quads), ( 64 + 128 * i,   0 + 150 * t, 0))
            positionBuffer.setValue(2 + 4 * (i + t * number_of_test_quads), ( 64 + 128 * i, 128 + 150 * t, 0))
            positionBuffer.setValue(3 + 4 * (i + t * number_of_test_quads), (-64 + 128 * i, 128 + 150 * t, 0))

    positionBuffer = model.getNormalBuffer(0)
    positionBuffer.setValue(0, (0, 0, 4096))

    model.setupChildVertices()

    return model

model_defs = [
    (6, False, False, False, False, "stable_vertex_color_only_material_bitfield.cobj",                       0x641aa032),
    (6, False, False,  True, False, "stable_vertex_color_only_reflective_material_bitfield.cobj",            0x5a62be06),
    (6, False, False,  True,  True, "stable_vertex_color_only_semi_reflective_material_bitfield.cobj",       0x9ab00451),
    (6,  True, False, False, False, "vertex_color_texture_material_bitfields.cobj",                          0x1a7e0a25),
    (6,  True, False,  True, False, "vertex_color_texture_reflective_material_bitfields.cobj",               0x15f29941),
    (6,  True, False,  True,  True, "vertex_color_texture_semi_reflective_material_bitfields.cobj",          0x40abfe34),
    (6,  True,  True, False, False, "vertex_color_animated_texture_material_bitfields.cobj",                 0xcdd2ad5d),
    (6,  True,  True,  True, False, "vertex_color_animated_texture_reflective_material_bitfields.cobj",      0x0f5d7220),
    (6,  True,  True,  True,  True, "vertex_color_animated_texture_semi_reflective_material_bitfields.cobj", 0xd13d3079)
]

def generate():
    for i in model_defs:
        generateModel(i[0], i[1], i[2], i[3], i[4]).makeFile(i[5], COBJBuilder.ModelFormat.WINDOWS)

def test():
    result = True

    for i in model_defs:
        crc32 = zlib.crc32(generateModel(i[0], i[1], i[2], i[3], i[4]).makeResource(COBJBuilder.ModelFormat.WINDOWS))

        if crc32 != i[6]:
            result = False
            print(i[5], "failed with", hex(crc32), "expected", hex(i[6]))

    return result

if __name__ == "__main__":
    test()
    generate()

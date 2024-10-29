import COBJBuilder

def generateModel(isReflective : bool, isReflectiveSemiTransparent : bool):
    model = COBJBuilder.COBJModel()

    model.setEnvironmentMapSemiTransparent(isReflectiveSemiTransparent)

    testFaceType = COBJBuilder.COBJFaceType()
    testFaceType.setVertexColor(True, [0, 0xff, 0])
    testFaceType.setTexCoords(True, [[0, 0], [0, 0xff], [0xff, 0xff], [0xff, 0]])
    testFaceType.setBMPID(6)
    model.appendFaceType(testFaceType)

    testFaceType = COBJBuilder.COBJFaceType()
    testFaceType.setVertexColor(True, [0x7f, 0x7f, 0x7f])
    model.appendFaceType(testFaceType)
    testFaceType = COBJBuilder.COBJFaceType()
    testFaceType.setVertexColor(True, [0x7f, 0, 0])
    model.appendFaceType(testFaceType)
    testFaceType = COBJBuilder.COBJFaceType()
    testFaceType.setVertexColor(True, [0, 0x7f, 0])
    model.appendFaceType(testFaceType)
    testFaceType = COBJBuilder.COBJFaceType()
    testFaceType.setVertexColor(True, [0, 0, 0x7f])
    model.appendFaceType(testFaceType)

    face = COBJBuilder.COBJPrimitive()
    face.setTypeQuad([3, 2, 1, 0], [0, 0, 0, 0])
    face.setTexture(True)
    face.setReflective(False)
    face.setFaceTypeIndex(0)
    model.appendPrimitive(face)

    number_of_test_face_types = 4

    number_of_test_quads = 16

    for t in range(0, number_of_test_face_types):
        for i in range(0, number_of_test_quads):
            face = COBJBuilder.COBJPrimitive()
            face.setTypeQuad([0 + 4 * (i + t * number_of_test_quads), 1 + 4 * (i + t * number_of_test_quads), 2 + 4 * (i + t * number_of_test_quads), 3 + 4 * (i + t * number_of_test_quads)], [0, 0, 0, 0])
            face.setTexture(False)
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
    positionBuffer.setValue(0, (4096,   0, 0))

    model.setupChildVertices()

    return model

generateModel(False, False).makeFile("stable_vertex_color_only_material_bitfield.cobj", '<', False)
generateModel( True, False).makeFile("stable_vertex_color_only_reflective_material_bitfield.cobj", '<', False)
generateModel( True,  True).makeFile("stable_vertex_color_only_semi_reflective_material_bitfield.cobj", '<', False)

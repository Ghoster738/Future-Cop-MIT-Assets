import COBJBuilder

def generateModel(cbmp_id: int, isTextured: bool, isReflective : bool, isReflectiveSemiTransparent : bool):
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
        i.setTexCoords(True, [[0, 0], [0, 0xff], [0xff, 0xff], [0xff, 0]])
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

generateModel(6, False, False, False).makeFile("stable_vertex_color_only_material_bitfield.cobj", '<', False)
generateModel(6, False,  True, False).makeFile("stable_vertex_color_only_reflective_material_bitfield.cobj", '<', False)
generateModel(6, False,  True,  True).makeFile("stable_vertex_color_only_semi_reflective_material_bitfield.cobj", '<', False)
generateModel(6,  True, False, False).makeFile("vertex_color_texture_material_bitfields.cobj", '<', False)
generateModel(6,  True,  True, False).makeFile("vertex_color_texture_reflective_material_bitfields.cobj", '<', False)
generateModel(6,  True,  True,  True).makeFile("vertex_color_texture_semi_reflective_material_bitfields.cobj", '<', False)

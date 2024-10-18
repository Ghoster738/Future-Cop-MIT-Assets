# COBJ Format

* [Table of Chunks](#table-of-chunks)
* [Order of Chunks](#order-of-chunks)
* [Chunk Descriptions](#chunk-descriptions)

## Table of Chunks
In Alphabetal Order.
* [**AmnD** Animation Tracks](#amnd)
* [**3DAL** Star Vertex Color Animations](#3dal)
* [**3DBB** Bounding Boxes](#3dbb)
* [**3DHS** Bone Positions (Unused by My Code)](#3dhs)
* [**3DHY** Bone Information & Hierarchy](#3dhy)
* [**3DMI** Bone Positions & Rotations](#3dmi)
* [**3DRF** Vertex Buffer Identifier List](#3drf)
* [**3DRL** Lengths Vertex Buffer](#3drl)
* [**3DTA** Texture Coordinate Animation Chunk](#3dta)
* [**3DTL** Texture/Vertex Colors Polygon Infos](#3dtl)
* [**3DQL** Primitive Data](#3dql)
* [**4DGI** Header](#4dgi)
* [**4DVL** Positions Vertex Buffer](#4dvl)
* [**4DNL** Normals Vertex Buffer](#4dnl)

## Order of Chunks
### All COBJs
* [4DGI](#4dgi)
* [3DTL](#3dtl)
* [3DTA](#3dta) *Optional*
* [3DQL](#3dql)
* [3DAL](#3dal) *Optional*
* [3DRF](#3drf) Holding 4DVL
* [3DRF](#3drf) Holding 4DNL
* [3DRF](#3drf) Holding 3DRL
* For each frame. Note: Static and Skinned Animations has one 4DVL, 4DNL and 3DRL.
  * [4DVL](#4dvl)
  * [4DNL](#4dvl)
  * [3DRL](#3drl)
* [3DBB](#3dbb)

### Skinned COBJs
Right after the 3DBB from "All OBJs" we have this.
* [3DHY](#3dhy)
* [3DMI](#3dmi)
* [3DHS](#3dhs)

### Skinned and Morph-Target COBJs
If the CObj has skin animation then AmnD comes right after 3DHS. If the CObj is a morph target then it is before the 3DBB chunk.
* [AmnD](#amnd)

## Chunk Descriptions
These are the chunk descriptions. All structs in this document are tightly packed for readability.

Structs used throughout this section.
```c
struct vector_2_byte {
  uint8_t x;
  uint8_t y;
};
```

### AmnD
TODO

### 3DAL
TODO

### 3DBB
TODO

### 3DHS
TODO

### 3DHY
TODO

### 3DMI
TODO

### 3DRF
TODO

### 3DRL
TODO

### 3DTA
This holds information that holds texture coordinate animation that overrides [3DTL](#3dtl) data.

#### Data
The first part is the header.
```c
struct chunk_3dta_header {
  uint32_t chunk_id; // Windows/PS1 ATD3. Macintosh 3DTA
  uint32_t tag_size; // Size of whole chunk.
  uint32_t number_of_face_overrides; // The number of face_override_info_3dta structs that would follow after chunk_3dta_header.
};
```
The second part is the face_override_info_3dta structs.
```c
struct face_override_info_3dta {
  uint8_t number_of_frames; // The number of frames the animation uses.
  uint8_t zero_0; // Always zero.
  uint8_t one; // Always one.
  uint8_t unknown_bitfield; // Unknown bitfield. It must have bit 0x01 present for it to be correctly to be interpreted.

  uint16_t frame_duration; // The duration of a single frame. Multiply it by UNITS_TO_SECONDS or 0.001652018 to get the frame time of a single frame.
  uint16_t zero_1; // Always zero.

  uint32_t uv_data_offset; // The offset from the last face_override_info_3dta entry in bytes.
  uint32_t offset_to_3DTL_uv; // Offset to 3DTL UV data. Subtract them by 4 to get the complete 3DQL entry offset.
};
```
The rest of this chunk are vector_2_byte structs.

### 3DTL
This chunk holds information on vertex colors and textures that the primitives of [3DQL](#3dql) could select through offsets. Please see [3DTA](#3dta) for details on UV data animations.

#### Data
The first part is the header.
```c
struct chunk_3dtl_header {
  uint32_t chunk_id; // Windows/PS1 LTD3. Macintosh 3DTL
  uint32_t tag_size; // Size of whole chunk.
  uint32_t one; // Always one.
};
```
After the header these are the rest of the data entries. **They have variable sizes of either 4 bytes or 16 bytes. Read them in sequence and store there offset right after the 3dtl_header struct.**
```c
struct entry_3dtl_color {
  uint8_t opcode; // If 1 then entry_3dtl_texture is not in this entry_3dtl_color struct. 2 and 3 and entry_3dtl_texture follows the entry
  uint8_t red;
  uint8_t green;
  uint8_t blue;
  struct entry_3dtl_texture;
};
```
```c
struct entry_3dtl_texture {
  struct vector_2_byte texture_coordinates[4];
  uint32_t cbmp_id;
};
```

### 3DQL
This holds the primitives which can be stars, triangles, quadrilaterals, billboards and lines.

#### Data Descriptions
These structs are used for the primitives that will be read.
```c
enum vertex_color_mode {
    NON        = 0,
    MONOCHROME = 1, // Warning: I am not sure that this is actually a thing.
    FULL       = 2
};
```
```c
enum visability_mode {
    OPAQUE   = 0,
    ADDITION = 1,
    MIX      = 2
};
```
```c
enum primitive_type {
    STAR          = 0,
    TRIANGLE      = 3,
    QUADRILATERAL = 4,
    BILLBOARD     = 5,
    LINE          = 7
};
```

#### Data
The first part of the chunk holds this data.
```c
struct chunk_3dql {
  uint32_t chunk_id; // Windows/PS1 LQD3. Macintosh 3DQL
  uint32_t tag_size; // Size of whole chunk.
  uint32_t one_0; // Always one.
  uint32_t number_of_primitives; // The number of primitives stored within this chunk.
};
```
The rest of this chunk holds these entries.
```c
struct primitive_3dql {
  uint8_t opcodes[2]; // See Opcodes Decoding sub-section for details.
  uint16_t face_type_offset; // An offset to the 3DTL entry that this primitive uses.
  uint8_t vertex_indexes[4]; // See Primitives sub-section on how to decode this.
  uint8_t normal_indexes[4]; // See Primitives sub-section on how to decode this.
};
```

#### Opcodes Decoding
Opcodes handles what the primitive_types, visability_mode, vertex_color_mode structs. In addition, it could even tell the primitive not to use textures at all. It also could use what seems to be [gouraud shading](https://en.wikipedia.org/wiki/Gouraud_shading).

Opcode[0]
```
win/ps1/mac 8 bitfield: tmmm,muuu

t = texture enabled.
m = materials bitfield
u = Unused bitfield. Guess.
```

Opcode[1]
```
win/ps1 8 bitfield: ruuu,ufff
mac     8 bitfield: pppu,uuur

u = Unused bitfield. Guess.
p = primitive type
r = "reflections" One if you want reflections on the primitive.
```

#### Material Bitfield Decoding
Warning: The knowedge on materials is probably incomplete. I might have made mistakes somewhere.
| Material | Gouraud Shading | Vertex Color | Visability Mode |
| -------: | :-------------: | :----------: | :-------------: |
| 0000     | FALSE           | NONE         | OPAQUE          |
| 0001     | FALSE           | NONE         | MIX             |
| 0010     | FALSE           | MONOCHROME   | OPAQUE          |
| 0011     | FALSE           | NONE         | MIX             |
| 0100     | TRUE            | NONE         | OPAQUE          |
| 0101     | TRUE            | NONE         | MIX             |
| 0110     | TRUE            | FULL         | OPAQUE          |
| 0111     | TRUE            | FULL         | MIX             |
| 1000     | TRUE            | NONE         | OPAQUE          |
| 1001     | TRUE            | NONE         | MIX             |
| 1010     | TRUE            | FULL         | OPAQUE          |
| 1011     | TRUE            | FULL         | OPAQUE          |
| 1100     | FALSE           | FULL         | ADDITION        |
| 1101     | UNKNOWN         | UNKNOWN      | UNKNOWN         |
| 1110     | UNKNOWN         | UNKNOWN      | UNKNOWN         |
| 1111     | UNKNOWN         | UNKNOWN      | UNKNOWN         |

#### Primitives
The primitive data from the Opcode[1] bitfield. This is how the bytes from the primitive_3dql struct be written. It also shows which data these datas are held.
| Primitive Type | Number | Vertex Index 0   | Vertex Index 1   | Vertex Index 2   | Vertex Index 3   | Normal Index 0 | Normal Index 1 | Normal Index 2 | Normal Index 3 |
| -------------- | :----: | :--------------: | :--------------: | :--------------: | :--------------: | :------------: | :------------: | :------------: | :------------: |
| STAR           | 0      | Position Index   | Red              | Green            | Blue             | Length Index   | 0              | 0              | 0              |
| TRIANGLE       | 3      | Position Index 1 | Position Index 2 | Position Index 3 | 0                | Normal Index 1 | Normal Index 2 | Normal Index 3 | 0              |
| QUADRILATERAL  | 4      | Position Index 1 | Position Index 2 | Position Index 3 | Position Index 4 | Normal Index 1 | Normal Index 2 | Normal Index 3 | Normal Index 4 |
| BILLBOARD      | 5      | Position Index   | 0xff             | Length Index     | 0xff             | 0              | 0              | 0              | 0              |
| LINE           | 7      | Position Index 1 | Position Index 2 | Length Index 1   | Length Index 2   | 0              | 0              | 0              | 0              |

#### Star Primitive
The star primitive comprises of a few triangles forming a circle. All the vertices in the circle should have the same color value. The edges of the circle should have its transparency value to zero while the center should have the transparency set to opaque.

The star primitive uses ```struct primitive_3dql```'s ```face_type_offset``` to determine how much triangles this primitive would use. Its usual value range is 4, 8 and 12

```vertex_indexes``` first index is used to get the position index offset. The rest are used for colors.

The length index is used to determine the radius of the star.

#### Triangle Primitive
A triangle primitive uses ```struct primitive_3dql```'s ```face_type_offset``` to get the [face type](#3dtl) to obtain the uv, and texture if present. It also could potentially have color data.

Also, it uses three position indexes and three normal indexes as shown on the [Primitives](#primitives) Table.

#### Quadrilateral Primitive
A quadrilateral primitive uses ```struct primitive_3dql```'s ```face_type_offset``` to get the [face type](#3dtl) to obtain the uv, and texture if present. It also could potentially have color data.

Also, it uses four position indexes and four normal indexes as shown on the [Primitives](#primitives) Table.

#### Billboard Primitive
A billboard primitive always faces the camera. There is no x-axis or y-axis locking.

A billboard primitive uses ```struct primitive_3dql```'s ```face_type_offset``` to get the [face type](#3dtl) to obtain the uv, and texture if present. It also could potentially have color data.

The primitive uses position index to place it. Also the length index is used to determine the billboard size.

#### Line Primitive
A line primitive uses ```struct primitive_3dql```'s ```face_type_offset``` to get the [face type](#3dtl) to obtain the uv, and texture if present. It also could potentially have color data.

A line primitive uses two position indexes to determine where the line begins and ends or ends and begins. The two length indexes are used to determine the size of the beginning and end.

### 4DGI
This is the first chunk that is read. This chunk can be used to query what type of COBJ resource being static, morph-target animation or skinned animations. It also determines if the model has "reflections" and whether it is semi-transparent or not.

#### Data
```c
struct chunk_4dgi {
  uint32_t chunk_id; // Windows/PS1 IGD4. Macintosh 4DGI
  uint32_t tag_size; // Size of whole chunk.
  uint16_t num_frames; // If the number of frames is other than one then it is an animated COBJ.
  uint8_t  id; // 0x01 for Windows; 0x10 for Macintosh.
  uint8_t  bitfield; // See bitfield for more info.
  uint32_t zeros[3]; // Always Zeros
  uint32_t one_0; // Always one.
  uint32_t two_0; // Always two.
  uint32_t one_1; // Always one.
  uint32_t one_2; // Always one.
  uint32_t three_0; // Always three.
  uint8_t position_indexes[4]; // If there is no position data then 0xFF gets filled in each of them.
  uint32_t four_0; // Always four.
  uint32_t five_0; // Always five.
};
```

#### Bitfield
This is the bitfield that the chunk_4dgi stores.
```
win/ps1 8 bitfield: art0,y0s0
mac     8 bitfield: 0s0y,0tra

0 = Unused.
a = Animated. 0 for static COBJ. 1 for Skin or Morph-Target COBJ.
r = Reflections. 1 if you want the "reflections" for the COBJ model. Warning: If this value is set to 0 and you use "reflection" polygons then you might crash Future Cop.
t = Semi-transparent reflections. 1 if you want all the reflections to be partially transparent. 0 if you want all the reflections to be transparent. You have to pick one or the other.
y = This bit is always on. Purpose unknown.
s = Skinned. 1 for skinned animation. 0 for either static or morph-target animations.
```

### 4DVL
TODO

### 4DNL
TODO

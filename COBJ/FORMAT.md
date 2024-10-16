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

  uint16_t frame_duration; // The duration of a single frame. Multiple it by UNITS_TO_SECONDS or 0.001652018 to get a single frame time.
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
TODO

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

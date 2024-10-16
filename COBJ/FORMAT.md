# COBJ Format

* [Table of Chunks](#table-of-chunks)
* [Order of Chunks](#order-of-chunks)
* [Chunk Descriptions](#chunk-descriptions) Note: All structs in this document are tightly packed for readability.

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
These are the chunk descriptions.

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
TODO

### 3DTL
TODO

### 3DQL
TODO

### 4DGI
This is the header chunk. This chunk determines what type of COBJ resource being static, morph-target animation or skinned animations. It also determines if the model has "reflections" and whether it is semi-transparent or not.

#### Data
```c
struct chunk_4dgi {
  uint32_t chunk_id; // In Windows 4DGI in Little Endian is IGD4
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

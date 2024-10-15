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
TODO

### 4DVL
TODO

### 4DNL
TODO

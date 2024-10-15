# COBJ Format

* [Order of Chunks](#order-of-chunks)

## Chunks
In Alphabetal Order.
* [**AmnD** Animation Tracks]()
* [**3DAL** Star Vertex Color Animations]()
* [**3DBB** Bounding Boxes]()
* [**3DHS** Bone Positions (Unused by My Code)]()
* [**3DHY** Bone Information & Hierarchy]()
* [**3DMI** Bone Positions & Rotations]()
* [**3DRF** Vertex Buffer Identifier List]()
* [**3DRL** Lengths Vertex Buffer]()
* [**3DTA** Texture Coordinate Animation Chunk]()
* [**3DTL** Texture/Vertex Colors Polygon Infos]()
* [**3DQL** Primitive Data]()
* [**4DGI** Header]()
* [**4DVL** Positions Vertex Buffer]()
* [**4DNL** Normals Vertex Buffer]()

## Order of Chunks
### All COBJs
* 4DGI
* 3DTL
* 3DTA *Optional*
* 3DQL
* 3DAL *Optional*
* 3DRF Holding 4DVL
* 3DRF Holding 4DNL
* 3DRF Holding 3DRL
* For each frame. Note: Static and Skinned Animations has one 4DVL, 4DNL and 3DRL.
  * 4DVL 
  * 4DNL 
  * 3DRL 
* 3DBB

### Skinned COBJs
Right after the 3DBB from "All OBJs" we have this.
* 3DHY
* 3DMI
* 3DHS
* AmnD

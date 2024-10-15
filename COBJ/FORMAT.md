# COBJ Format

* [Order of Chunks](#order-of-chunks)

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

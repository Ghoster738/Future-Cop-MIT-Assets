# COBJ Format

* [Table of Chunks](#table-of-chunks)
* [Order of Chunks](#order-of-chunks)
* [Chunk Descriptions](#chunk-descriptions)

## Table of Chunks
In Alphabetal Order.
* [**AnmD** Animation Tracks](#anmd)
* [**3DAL** Star Vertex Color Animations](#3dal)
* [**3DBB** Bounding Boxes](#3dbb)
* [**3DHS** Bone Positions](#3dhs)
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
* [AnmD](#anmd)

## Chunk Descriptions
These are the chunk descriptions. All structs in this document are tightly packed for readability.

Structs used throughout this section.
```c
struct vector_2_byte {
  uint8_t x;
  uint8_t y;
};
```

### AnmD
I do not know much about this chunk. However, it contains the animation track data.

#### Data
The first thing that is read is this chunk.
```c
struct chunk_anmd_header {
  uint32_t chunk_id; // Windows/PS1 DmnA. Macintosh AnmD
  uint32_t tag_size; // Size of whole chunk.
  uint32_t one; // Always one.
};
```

The rest of the chunk has.
```c
struct animation_track {
  uint8_t unk_8_0;
  uint8_t un_speed;
  uint8_t unk_8_1;
  uint8_t un_skip_frame; // Wild guess.
  uint16_t from_frame;
  uint16_t to_frame;
  uint8_t unk_8_2;
  uint8_t unk_8_3;
  uint16_t unk_16;
  uint32_t unk_32;
};
```

### 3DAL
This handles vertex color animations for stars. Note: This overrides the star color stored in 3DQL.

#### Data
The first thing that is read is this chunk.
```c
struct chunk_3dal_header {
  uint32_t chunk_id; // Windows/PS1 LAD3. Macintosh 3DAL
  uint32_t tag_size; // Size of whole chunk.
  uint32_t count; // This holds how many star_animation structs are in this chunk. Note: Only a count of one had been observed. It could be that this is only a version number!
};
```

The rest of the chunk comprises of these star animation structs.
```c
struct star_animation {
  uint8_t face_index; // 3DQL index to primative type star
  uint8_t speed_factor; // Please see the 
  uint8_t red_0;
  uint8_t green_0;
  uint8_t blue_0;
  uint8_t red_1;
  uint8_t green_1;
  uint8_t blue_1;
};
```

#### How does it work
```c
float speed_rate;
float time = -1.0f;

void init() {
  speed_rate = 2.0f * (0.0757594 * star_animation.speed_factor + 0.0520309);
}

void loop(float deltaSecond) {
  time += speed_rate * deltaSecond;
  
  if(time >= 1.0f)
    time -= 2.0f;

  color = math_mix(color_option_0, color_option_1, math_abs(time));
}
```

### 3DBB
This holds bounding boxes that the model uses. For static models, there are only one frame of bounding box data. For animated models, they have multiple frames of bounding box data.

At least one bounding box that spans all the 4DVL points is in this chunk for every model. It is the first bounding box in the given frame.

#### Data
The first thing that is read is this chunk.
```c
struct chunk_3dbb_header {
  uint32_t chunk_id; // Windows/PS1 BBD3. Macintosh 3DBB
  uint32_t tag_size; // Size of whole chunk.
  uint32_t bounding_box_per_frame; // These are the bounding boxes per frame.
  uint32_t bounding_box_amount; // This is the total bounding boxes in the chunk.
};
```

This describes the structure of 3DBB.
```c
struct bounding_box {
  int16_t x;
  int16_t y;
  int16_t z;
  uint16_t length_x;
  uint16_t length_y;
  uint16_t length_z;
  uint16_t length_pyth_3; // Roughly (length_x^2 + length_y^2 + length_z^2) square rooted.
  uint16_t length_pyth_2; // Roughly (length_x^2 + length_z^2) square rooted.
};
```

The rest are this.
```c
uint32_t bounding_box_frames = bounding_box_amount / bounding_box_per_frame;

struct bounding_boxes[bounding_box_per_frame][bounding_box_frames];
```

**This is how the bounding boxes are placed.**
```
Frame placement
if bounding_box_per_frame 2 and bounding_box_amount 6 then bounding_box_frames equals 3
struct bounding_boxes[2][3];

This will be the how the bounding boxes are laid out.
bounding_boxes[0][0] // Box 0 frame 0
bounding_boxes[0][1] // Box 0 frame 1
bounding_boxes[0][2] // Box 0 frame 2
bounding_boxes[1][0] // Box 1 frame 0
bounding_boxes[1][1] // Box 1 frame 1
bounding_boxes[1][2] // Box 1 frame 2
```

#### Converting from Fixed-Point to floating point.
Convert all bounding box units with [4DVL](#4dvl)'s FIXED_POINT_UNIT.

### 3DHS
This chunk probably holds child positions for the skinned system. It probably overrides [4DGI](#4dgi) position_indexes array.

#### Data
The first part that is read is this chunk.
```c
struct chunk_3dhs {
  uint32_t chunk_id; // Windows/PS1 SHD4. Macintosh 3DHS
  uint32_t tag_size; // Size of whole chunk.
  uint32_t position_per_frame_amount;
  uint32_t total_positions_in_chunk;
};
```

The rest are these entries. See [4DVL](#4dvl) to convert this into floating point.
```c
struct vertex_buffer {
  int16_t fixed_point_x;
  int16_t fixed_point_y;
  int16_t fixed_point_z;
  int16_t unused_data;
};
```

Frame data is read like this. Unlike [3DBB](#3dbb) they are stored like this.
```
struct vertex_buffer child_positions[total_frames][position_per_frame_amount]

// For example, let total_frames be 3 and position_per_frame_amount be 2.
child_positions[0][0] = (3, 4, 5)
child_positions[0][1] = (-3, -4, -5)
child_positions[1][0] = (7, 4, 5)
child_positions[1][1] = (-7, -4, -5)
child_positions[2][0] = (9, 4, 5)
child_positions[2][1] = (-9, -4, -5)
```

#### Converting from Fixed-Point to floating point.
Convert all position units with [4DVL](#4dvl)'s FIXED_POINT_UNIT.

### 3DHY
This holds the skeleton information for skinned animation.

#### Data
The first part that is read is this chunk.
```c
struct chunk_3dhy {
  uint32_t chunk_id; // Windows/PS1 YHD4. Macintosh 3DHY
  uint32_t tag_size; // Size of whole chunk.
  uint32_t one; // Always 1.
};
```

The rest are these entries.
```c
struct bone {
  uint8_t parent_amount; // There is an algorithm to determine the bone parents.
  uint8_t normal_start; // Where in the 4DNL data to read.
  uint8_t normal_stride;
  uint8_t vertex_start; // Where in the 4DVL data to read.
  uint8_t vertex_stride;
  uint8_t not_sure_length_start;
  uint8_t not_sure_length_stride;
  uint8_t opcode; // This opcode is VERY IMPORTANT.

  // These are constants to be used if 3DMI does not hold the data.
  // These are base indexes to 3DMI if they are not constant.
  int16_t position_x;
  int16_t position_y;
  int16_t position_z;
  int16_t rotation_x;
  int16_t rotation_y;
  int16_t rotation_z;
```

#### Determining the Bone Hierarcy
The current bone will connect with a "bellow" bone with a parent_amount value one less of the current bone.


This is a diagram showing how the skeleton information can be built.
```
I = Bone index
P = Bone parent_amount

I     : P
Bone 0: 0      0                 Initial Bone. It does not have any parents.
              /|\
               |
Bone 1: 1      *-- 1             Bone 1's parent is Bone 0 since Bone 0 has a parent_amount of zero.
               |  /|\
               |   |
Bone 2: 2      |   *-- 2         Bone 2's parent is Bone 1 since Bone 1 has a parent_amount of one.
               |
               |
Bone 3: 1      *-- 1             Bone 3's parent is Bone 0 since Bone 0 has a parent_amount of zero.
                  /|\
                   |
Bone 4: 2          *-- 2         Bone 4's parent is Bone 3 since Bone 3 has a parent_amount of one.
                   |  /|\
                   |   |
Bone 5: 3          |   *-- 3     Bone 5's parent is Bone 4 since Bone 4 has a parent_amount of two.
                   |
                   |
Bone 6: 2          *-- 2         Bone 6's parent is Bone 3 since Bone 3 has a parent_amount of one.
```

#### Decoding opcode for position and rotation data.
To save space, the developers of this Model format.
```
position.x_const = (opcode & 0b00100000);
position.y_const = (opcode & 0b00010000);
position.z_const = (opcode & 0b00001000);
rotation.x_const = (opcode & 0b00000100);
rotation.y_const = (opcode & 0b00000010);
rotation.z_const = (opcode & 0b00000001);
```

If any of these bits are found to be enabled then the game will use the constant instead. 

So if x_const is enabled then the bone x position stays constant throughout every animation.

However, if x_const is not enabled then [3DMI](#3dmi) will hold an *index* to array of x positions. To get the x position in the animation, add the index of the x position with the frame of animation.

#### Converting from Fixed-Point to floating point.
Convert all position units with [4DVL](#4dvl)'s FIXED_POINT_UNIT.

Convert all rotation units using this factor.
```c
const float ANGLE_UNIT = PI / 2048.0;
```

### 3DMI
This chunk holds the animation data buffer for skinned animated models in 16 bit arrays.

#### Data
The first thing that is read is this chunk.
```c
struct chunk_3dmi_header {
  uint32_t chunk_id; // Windows/PS1 IMD3. Macintosh 3DMI
  uint32_t tag_size; // Size of whole chunk.
  uint32_t one;
};
```

The rest of this chunk contains a signed 16 bit data array that will be referenced by [3DHY](#3dhy).

#### Memory Organization

### 3DRF
This chunk holds IDs referncing vertex buffer chunk(s). Vertex Buffer Chunks for this document are [4DVL](#4dvl), [4DNL](#4dnl), and [3DRL](#3drl) chunks.
The game actually uses IDs stored individually in [4DVL](#4dvl), [4DNL](#4dnl), and [3DRL](#3drl) chunks.
Each chunk type has its own namespace.

#### Data
The first thing that is read is this chunk.
```c
struct chunk_3drf_header {
  uint32_t chunk_id; // Windows/PS1 FRD3. Macintosh 3DRF
  uint32_t tag_size; // Size of whole chunk.
  uint32_t reference_number; // 1,    2,    3.
  uint32_t reference_tag;    // 4DVL, 4DNL, 3DRL. 4DNL would have a reference_number of 2. 3DRL would be 3.
  uint32_t count; // A static and skin animation model has only one reference number. Morph target animation has a count that matches its numbers of frames.
};
```

This struct is followed by this array of data.
```
uint32_t 3drf_ids[count]; // This holds IDs
```

#### Static Models/Skin Animation Models
Since there is only one reference per vertex buffer then the chunk then only expect that the Vertex Buffer Chunk being the reference_tag has the correct 3drf ID.

#### Morph Target Models
The morph target models are a little bit more complicated. In the frame index of the animation being played
```
let i be the frame index being used while drawing model.

let 3drf_ids[i] be the ID that is used for the vertex buffer.
```

Please remember that there are three 3DRF's and the three or more 4DVL, 4DNL, and 3DRL chunks.

### 3DRL
This vertex buffer chunk contains length data. It is referenced by [3DRF](#3drf) by ```id```.

#### Data
The first part of the chunk holds this data.
```c
struct chunk_3drl {
  uint32_t chunk_id; // Windows/PS1 LND4. Macintosh 4DNL
  uint32_t tag_size; // Size of whole chunk.
  uint32_t id; // As referenced by a 3DRF frame.
  uint32_t amount_of_lengths;
};
```

The rest of this chunk holds these entries.
```c
uint16_t fixed_point_lengths[amount_of_lengths];
```

#### Converting from Fixed-Point to floating point.
```c
const float FIXED_POINT_UNIT = 1.0 / 512.0;

float floating_point = fixed_point * FIXED_POINT_UNIT;
```

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
u = Unknown bitfield.
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
This vertex buffer chunk contains position data. It is referenced by [3DRF](#3drf) by ```id```.

#### Data
The first part of the chunk holds this data.
```c
struct chunk_4dvl {
  uint32_t chunk_id; // Windows/PS1 LVD4. Macintosh 4DVL
  uint32_t tag_size; // Size of whole chunk.
  uint32_t id; // As referenced by a 3DRF frame.
  uint32_t amount_of_positions;
};
```

The rest of this chunk holds these entries.
```c
struct vertex_buffer {
  int16_t fixed_point_x;
  int16_t fixed_point_y;
  int16_t fixed_point_z;
  int16_t unused_data;
};
```

#### Converting from Fixed-Point to floating point.
```c
const float FIXED_POINT_UNIT = 1.0 / 512.0;

float floating_point = fixed_point * FIXED_POINT_UNIT;
```

### 4DNL
This vertex buffer chunk contains normal data. It is referenced by [3DRF](#3drf) by ```id```.

#### Data
The first part of the chunk holds this data.
```c
struct chunk_4dnl {
  uint32_t chunk_id; // Windows/PS1 LND4. Macintosh 4DNL
  uint32_t tag_size; // Size of whole chunk.
  uint32_t id; // As referenced by a 3DRF frame.
  uint32_t amount_of_normals;
};
```

The rest of this chunk holds these entries.
```c
struct normal_buffer {
  int16_t fixed_point_x;
  int16_t fixed_point_y;
  int16_t fixed_point_z;
  int16_t unused_data;
};
```

#### Converting from Fixed-Point to floating point.
```c
const float FIXED_NORMAL_UNIT = 1.0 / 4096.0;

float floating_point = fixed_point * FIXED_NORMAL_UNIT;
```

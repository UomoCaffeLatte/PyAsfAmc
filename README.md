# PyAsfAmc
Author: Nikhil Reji

generic asf/amc parser following standard version 1.1.

## features:
- ASF parser
- AMC parser
- Simple, Clean data structure.

## Imports
``` Python
    from asfamcparser import ParseASF, ParseAMC
```

## Data Structure
### Joint
Immutable class where every property is optional.
```Python
    JOINT
        - name : str
        - dof  : NamedTuple e.g (rx=(-inf,inf), ry=(-inf,inf), rz=(-inf,inf))
        - direction : Tuple e.g (0.0, 1.2, 2.2)
        - length : float
        - axis : NamedTuple e.g (X=0.0, Y=0.0, Z=0.0)
        - order : Tuple e.g ("X", "Y", "Z")
```
NamedTuple values can be accessed either through their index or their names as follows:
``` Python
    axis.X
```

### ASF
Immutable class.
```Python
    ASF
        - name : str
        - units : NamedTuple e.g ("mass"="kg", "length"="mm", "angle"="Deg")
        - doc : str
        - joints : Tuple[Joint, ...]
        - hierarchy : dict where each key corresponds to a a joint that has children.
```
Individual joints can be retrieved using the dict key method as follows:
``` Python
    LElbowJoint = ASF["LeftElbow"]
```
Also, all joints can be accessed through for iterations:
```Python
    for joint in ASF:
        print( joint.name )
```
### AMC
Immutable class
```Python
    AMC
        - count:int (number of frames)
        - frames: Tuple[dict,...] 
```
Individual frames can be retrieved using the dict key method as follows:
``` Python
    frameTen = AMC[10]
```
Individual frames and specific joint data can be retrieved using the dict key method as follows:
``` Python
    frameTenHead = AMC[10]["Head"]
```
Also, all frames can be accessed through for iterations:
```Python
    for frame in AMC:
        print( frame.count )
```
## Examples:

### ParseASF
The full path to the .asf file is required to parse.
``` Python
    parsedAsf = ParseASF("./recordings/test.asf")
    asf = parsedASF.asf
```
The retrieve asf file can be navigated using its properties described in the data structudre section.

### ParseAMC
The full path to the .amc file is required to parse.
``` Python
    parsedAmc = ParseAmc("./recordings/test.amc")
    amc = parsedAMC.amc
```
The retrieved amc file can be navigated using its properties described in the data structure section.


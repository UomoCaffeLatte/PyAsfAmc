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
```
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
### AMC
```
```

## Examples:

### ParseASF
The full path to the .asf file is required to parse.
``` Python
    parsedAsf = ParseASF("./recordings/test.asf")
    asf = parsedASF.asf
```
The retrieve asf file can be navigated using its properties described in the data structure section.

### ParseAMC


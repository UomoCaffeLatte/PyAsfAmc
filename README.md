# PyAsfAmc
Author: Nikhil Reji

In house asf/amc parser following version 1.1.

## features:
- ASF parser with data structure.
- AMC parser with data structure.
- Joint data structure.

## How to use:

#### Open and parse files
Ensure the .asf and .amc files are located in the same working directory.

```Python
    from asfamcparser import Parser

    wdr = os.path.dirname(os.path.realpath(__file__)) # working directory of current script

    # initalised with the target directory 
    asfamcParser = Parser(wdr)
    # Asf must be opened and parsed first.
    # open and parse asf file, remove extension
    asfamcParser.OpenAsf("TestSkeleton")
    # open and parse amc file, remove extention
    asfamcParser.OpenAmc("TestMotion")

    # Parsed Amc and Asf can be accessed as follows:
    asfamcParser.amc
    asfamcParser.asf
```

#### Explore parsed asf data
The asf data structure have the following properties:
- name
- joints (All bone joints and their corresponding properties.)
- getJointNames (Returns all joint names.)
- units (returns mass, length, and angle units.)
- hierarchy (returns dictionary of with key as only parent joints.)
- docs (returns documentation section)

asf data structure also contains the __getitem__ dunder method. This allows for quick access to joint data using the jointName as a key as follows:

```python
LeftElbowJoint = asfamcParser.asf["LeftElbow"]
```

Each Joint data structure contains the following properties:
- Name
- Direction
- Length (if given child joints.)
- axisOrder (List of chars.)
- axis (List of axis values.)
- dof (Degree of Freedom.)
- limits (Degree of Freedom limits.)

#### Explore parsed amc data
The amc data structure contains the following properties:
- frames (Nested list of frames, where each item in the first level depicts a single frame containing a list of corresponding joint values in the format '["NAME","VAL","VAL","VAL"]', in the second level.)
- frameCount
- duration
- fps

amc data structure also contains the __getitem__ dunder method. This allows for quick access to frame data using the frame index as a key as follows:

```python
frameTenValues = asfamcParser.amc[10]
```

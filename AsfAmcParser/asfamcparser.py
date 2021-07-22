
import logging
from re import split
import re
from sys import float_repr_style

# Each type class is responsible for parsing its own elements
class Joint:
    def __init__(self, name:str) -> None:
        self._name = name
        self._direction = []
        self._length = None
        self._axisOrder = []
        self._axis = {}
        self._dof = {}

    @property
    def name(self):
        return self._name

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value:str):
        """Set direction vector from string,

        Args:
            value (str): direction floats x 3 in string format "\\tvalue\\tvalue\\tvalue"
        """
        splitString = value.split("\t")[1:]
        # Check there are 3 split strings
        if len(splitString) == 3:
            # convert to string and append
            for stringValue in splitString:
                self._direction.append(float(stringValue))
        else:
            logging.error(f"direction values must be of format \\tvalue\\tvalue\\tvalue, instead {len(splitString)} values were provided in string format.")

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value:str):
        if value != "":
            self._length = float(value)
        else:
            logging.error("length value empty!")

    @property
    def axisOrder(self):
        return self._axisOrder

    @axisOrder.setter
    def axisOrder(self,value:str):
        # split characters
        chars = list(value)
        # check three axis given
        if len(chars) == 3:
            self._axisOrder = chars
        else:
            logging.error(f"axisOrder must contain only three axis in the format [Axis1][Axis2][Axis3], instead {len(chars)} values were provided in string format.")
    
    @property
    def axis(self):
        return self._axis
    
    @axis.setter
    def axis(self,value:str):
        # check axisOrder has been set
        if self._axisOrder == []:
            logging.error("Axis order must be set first to enter axis values.")
            return
        splitString = value.split("\t")[1:]
        # Check there are 3 split strings
        if len(splitString) == 3:
            for axis, value in zip(self._axisOrder, splitString):
                self._axis[axis] = float(value)
        else:
            logging.error(f"axis values must be of format \t\tvalue\t\tvalue\t\tvalue, instead {len(splitString)} values were provided in string format.")

    @property
    def dof(self):
        return list(self._dof.keys())
    
    @dof.setter
    def dof(self, value:str):
        stringSplit = value.split("\t")[1:]
        for item in stringSplit:
            self._dof[item] = None
    
    @property
    def limits(self):
        return self._dof
    
    @limits.setter
    def limits(self, value:list):
        # check value is list equal to size of dof
        if self._dof == {}:
            logging.error("dof needs to be set first.")
            return
        if len(value) == len(self._dof):
            for key, limit in zip(list(self._dof.keys()),value):
                # convert to two float list raw format = "(limit limit)"
                splitLimitString = limit.split("\t")
                limitsList = []
                for string in splitLimitString:
                    strings = string.replace(")","(").split("(")
                    # remove empty string
                    for string in strings:
                        if string: limitsList.append(float(string))
                self._dof[key] = limitsList
        else:
            logging.error("Number of limits must match degree of freedoms, check passing in list.")

class ASF:
    def __init__(self, name:str) -> None:
        self._name = name
        self._units = {"mass":"","length":"","angle":""}
        self._docs = ""
        self._joints = []
        self._hierarchy = {}
    
    @property
    def joints(self):
        return self._joints

    @property
    def getJointNames(self):
        return [joint.name for joint in self._joints]
    
    @property
    def name(self):
        return self._name

    @property
    def units(self):
        return self._units

    @property
    def hierarchy(self):
        return self._hierarchy
    
    @property
    def docs(self):
        return self._docs

    @docs.setter
    def docs(self, value:str):
        self._docs = value

    def AddJoint(self, joint:Joint):
        self._joints.append(joint)
    
    def AddMassUnit(self, unit:str):
        self._units["mass"] = unit

    def AddLengthUnit(self, unit:str):
        self._units["length"] = unit

    def AddAngleUnit(self, unit:str):
        self._units["angle"] = unit
    
    def AddJointHierarchy(self, parentJointName:str, hierarchyRaw:str):
        # format: \tName\tName etc
        stringSplit = hierarchyRaw.split("\t")[1:]
        self._hierarchy[parentJointName] = stringSplit

    def __getitem__(self, jointName:str) -> Joint:
        for j in self._joints:
            if j.name == jointName: return j
        logging.error(f"{jointName} joint does not exists.")
        return None

class AMC:
    def __init__(self) -> None:
        self._frameCount = 0
        self._frames = []
        self._fps = 30
        self._duration = 0

    @property
    def frames(self):
        return self._frames
    
    @property
    def frameCount(self):
        return self._frameCount
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def fps(self):
        return self._fps
    
    @fps.setter
    def fps(self, value:int):
        if value > 0:
            self._fps = value
        else:
            logging.error("fps must be greater than 0.")

    def AddFrame(self, values:list):
        # format: ["NAME","VAL","VAL","VAL"]
        frame = {}
        for value in self._SplitJointLine(values):
            frame[value[0]] = [float(x) for x in value[1:]]
        self._frames.append(frame)
        self._frameCount += 1
        self._duration = self._fps * self._frameCount

    def __getitem__(self, frame:int) -> list:
        if frame >= 0 and frame < self._frameCount:
            return self._frames[frame]
        else:
            logging.error("frame index out of bounds.")
    
    def _SplitJointLine(self, values:str):
        # check if dof is set
        listValues = []
        for string in values:
            listValues.append(string.split("\t"))
        return listValues

class Parser:
    def __init__(self, directory:str=None) -> None:
        self._directory = directory
        self._asf = None
        self._amc = None
        self._joints = []

    def asf(self, fileName:str):
        # Read file
        with open(f"{self._directory}{fileName}") as asfFile:
            lines = asfFile.read().splitlines()
        

    def amc(self, fileName:str):
         # Read file
        with open(f"{self._directory}{fileName}") as amcFile:
            lines = amcFile.read().splitlines()
        pass

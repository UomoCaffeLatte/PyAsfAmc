
from dataclasses import dataclass
from collections import namedtuple
from os import linesep
from typing import Tuple, NamedTuple


@dataclass(frozen=True)
class Joint:
    # dataclass that represents a single joint
    name: str
    dof: NamedTuple
    axis: NamedTuple
    direction: NamedTuple
    length: float

@dataclass(frozen=True)
class ASF:
    # dataclass that represents a parsed asf file
    name: str
    units: NamedTuple
    doc: str
    joints: dict
    hierarchy: dict

    def __getitem__(self, jointName:str) -> Joint:
        return self.joints[jointName]

@dataclass(frozen=True)
class AMC:
    # dataclass that represents a parsed amc file
    count: int
    fps: int
    duration: int
    frames: Tuple[Tuple, ...]

    def __getitem__(self, frame:int) -> Tuple:
        if frame < self.count:
            return self.frames[frame]
        raise IndexError(f"Frame index must be < {self.count}.")

# Main logic
class Reader:
    def ReadFile(self, filePath:str) -> Tuple[str, ...]:
        try:
            with open(filePath) as file:
                lines = file.read().splitlines()
            return tuple(lines)
        except Exception as e:
            raise e
    
    def _ReadLine(self, lines:Tuple[str, ...], i:int=0) -> Tuple[str,int]:
        if i >= len(lines): return None, i
        line = lines[i].split()
        i += 1
        return line, i

class ParseASF(Reader):
    def __init__(self, filePath:str) -> ASF:
        super().__init__()
        # check file path exists and read all lines in file
        lines = self.ReadFile(filePath)
        # parse into asf dataclass
        # finish and return
        return None
    
    def _RaiseSyntaxError(self, index:int): raise SyntaxError(f"Asf format incorrect at line {index}.")

    def _Parse(self, lines:Tuple[str, ...]) -> ASF:
        unitsT = namedtuple('units',['mass','length','angle'])
        read = lambda index: self._ReadLine(lines, index)
        line, i = read(0)
        if not line[0] == ":version": self._RaiseSyntaxError(i)
        if not line[1] == "1.10": self._RaiseSyntaxError(i)
        line, i = read(i)
        if not line[0] == ":name": self._RaiseSyntaxError(i)
        name = line[1]
        line, i = read(i)
        if not line[0] == ":units": self._RaiseSyntaxError(i)
        line, i = read(i)
        if not line[0] == "mass": self._RaiseSyntaxError(i)
        mass = line[1]
        if not line[0] == "length": self._RaiseSyntaxError(i)
        length = line[1]
        if not line[0] == "angle": self._RaiseSyntaxError(i)
        angle = line[1]
        units = unitsT(mass, length, angle)
        line, i = read(i)
        if not line[0] == ":documentation": self._RaiseSyntaxError(i)
        doc = ""
        while line[0] != ":root":
            line, i = read(i)
            doc += line + ""
        



class ParseAMC(Reader):
    def __init__(self, filePath:str) -> AMC:
        super().__init__()
        # check file path exists and read all lines in file
        lines = self.ReadFile(filePath)
        # parse into amc dataclass
        # finish and return
        return None
    
    def _Parse(self, lines:Tuple[str, ...]) -> AMC:
        pass
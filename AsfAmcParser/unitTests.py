from visualiser import visualiser
from abc import abstractmethod
import unittest
from unittest.case import TestCase
from unittest.main import main
from asfamcparser import Joint, AMC, ASF, Parser
from math import inf
import os

class ASFUnitTests(unittest.TestCase):
    
    def test_docsSetter(self):
        asfType = ASF("Test")
        docs = "fps:30"
        asfType.docs = docs
        self.assertEqual(asfType.docs, docs)
        self.assertEqual(asfType._docs, docs)

    def test_AddJoint(self):
        asfType = ASF("Test")
        testJoint1 = Joint("Test")
        asfType.AddJoint(testJoint1)
        self.assertEqual(asfType.joints,[testJoint1])
        testJoint2 = Joint("Test2")
        asfType.AddJoint(testJoint2)
        self.assertEqual(asfType.joints,[testJoint1,testJoint2])
    
    def test_AddMassUnit(self):
        asfType = ASF("Test")
        asfType.AddMassUnit("MM")
        self.assertEqual(asfType.units["mass"],"MM")

    def test_AddLengthUnit(self):
        asfType = ASF("Test")
        asfType.AddLengthUnit("m")
        self.assertEqual(asfType.units["length"],"m")

    def test_AddAngleUnit(self):
        asfType = ASF("Test")
        asfType.AddAngleUnit("deg")
        self.assertEqual(asfType.units["angle"],"deg")

    def test_AddJointHierarchy(self):
        asfType = ASF("Test")
        teststring = "\tbone2\tbone3\tbone4"
        asfType.AddJointHierarchy("bone1",teststring)
        self.assertEqual(asfType.hierarchy["bone1"], ["bone2","bone3","bone4"])

    def test_GetItemDunder(self):
        asfType = ASF("Test")
        testJoint1 = Joint("Test1")
        testJoint2 = Joint("Test2")
        asfType.AddJoint(testJoint1)
        asfType.AddJoint(testJoint2)
        self.assertEqual(asfType["Test1"], testJoint1)
        self.assertEqual(asfType["Test2"], testJoint2)
    
    def test_GetJointNames(self):
        asfType = ASF("Test")
        testJoint1 = Joint("Test1")
        testJoint2 = Joint("Test2")
        asfType.AddJoint(testJoint1)
        asfType.AddJoint(testJoint2)
        self.assertEqual(asfType.getJointNames, ["Test1","Test2"])
        
class AMCUnitTests(unittest.TestCase):
    
    def test_fpsSeter(self):
        testAMC = AMC()
        testAMC.fps = 30
        self.assertEqual(testAMC.fps, 30)

    def test_AddFrame(self):
        testAMC = AMC()
        teststring = ["Test1\t0.3\t5.5\t9.9","Test2\t0.7\t9.0\t10.0"]
        testAMC.AddFrame(teststring)
        self.assertEqual(testAMC.frames[0], {"Test1":[0.3,5.5,9.9],"Test2":[0.7,9.0,10.0]})

    def test_GetItemDunder(self):
        testAMC = AMC()
        teststring = ["Test1\t0.3\t5.5\t9.9","Test2\t0.7\t9.0\t10.0"]
        testAMC.AddFrame(teststring)
        self.assertEqual(testAMC[0], {"Test1":[0.3,5.5,9.9],"Test2":[0.7,9.0,10.0]})

    def test_SplitJointLine(self):
        testAMC = AMC()
        teststring = ["Test1\t0.3\t5.5\t9.9","Test2\t0.7\t9.0\t10.0"]
        self.assertEqual(testAMC._SplitJointLine(teststring), [["Test1","0.3","5.5","9.9"],["Test2","0.7","9.0","10.0"]])

class ParserUnitTests(unittest.TestCase):
    
    def test_parseASF(self):
        wdr = os.path.dirname(os.path.realpath(__file__))
        print(wdr)
        asfamcParser = Parser(wdr)
        
        with open(f"{wdr}\Test.asf") as asfFile:
            lines = asfFile.read().splitlines()
            asfamcParser._ParseAsf(lines)

        self.assertEqual(asfamcParser.asf.name,"0101")
        self.assertEqual(len(asfamcParser.asf.getJointNames),19)
        self.assertEqual(asfamcParser.asf.units["mass"], "kg")
        self.assertEqual(asfamcParser.asf.units["length"], "m")
        self.assertEqual(asfamcParser.asf.units["angle"], "deg")

    def test_parseAMC(self):
        wdr = os.path.dirname(os.path.realpath(__file__))
        asfamcParser = Parser(wdr)
        
        with open(f"{wdr}\Test.amc") as amcFile:
            lines = amcFile.read().splitlines()
            asfamcParser._ParseAmc(lines)
        
        self.assertEqual(asfamcParser.amc.frameCount, 300)
        self.assertEqual(asfamcParser.amc.duration, 300/30)

    def test_OpenAsf(self):
        wdr = os.path.dirname(os.path.realpath(__file__))
        asfamcParser = Parser(wdr)
        lines = asfamcParser.OpenAsf("test")
        self.assertEqual(lines[0],":version\t1.10")
        self.assertEqual(lines[len(lines)-1],"\tend")

    def test_OpenAMC(self):
        wdr = os.path.dirname(os.path.realpath(__file__))
        asfamcParser = Parser(wdr)
        lines = asfamcParser.OpenAmc("test")

class JointUnitTests(unittest.TestCase):
    
    def test_nameGetter(self):
        testJoint = Joint("Test")
        self.assertEqual(testJoint.name,"Test")

    def test_directionSetter(self):
        testJoint = Joint("Test")
        testString = "\t1.3\t4.5\t6.7"
        testJoint.direction = testString
        self.assertEqual(testJoint.direction[0],1.3)
        self.assertEqual(testJoint.direction[1],4.5)
        self.assertEqual(testJoint.direction[2],6.7)
    
    def test_lengthSetter(self):
        testJoint = Joint("Test")
        testString = "14.5"
        testJoint.length = testString
        self.assertEqual(testJoint.length,14.5)
    
    def test_axisOrderSetter(self):
        testJoint = Joint("Test")
        testString = "XYZ"
        testJoint.axisOrder = testString
        self.assertEqual(testJoint.axisOrder, ["X","Y","Z"])

    def test_axisSetter(self):
        testJoint = Joint("Test")
        testString = ["5.5","5.6","6.8"]
        testJoint._axisOrder = ["X","Y","Z"]
        testJoint.axis = testString
        self.assertDictEqual(testJoint.axis, {"X":5.5,"Y":5.6,"Z":6.8})

    def test_dofSetter(self):
        testJoint = Joint("Test")
        testJoint.dof = ["rx","ry","rz"]
        self.assertEqual(testJoint.dof, ["rx","ry","rz"])

    def test_limitsSetter(self):
        testJoint = Joint("Test")
        testJoint._dof = {"rx":None, "ry":None, "rz":None}
        testJoint.limits = ["(-inf\tinf)","(-inf\tinf)","(-inf\tinf)"]
        self.assertDictEqual(testJoint.limits, {"rx":[-inf,inf],"ry":[-inf,inf],"rz":[-inf,inf]})

class VisualiserTests(unittest.TestCase):
    
    def test_CreateSkeletalVectors(self):
        wdr = os.path.dirname(os.path.realpath(__file__))

        asfamcParser = Parser(wdr)
        
        asfamcParser.OpenAsf("TestSkeleton")
        asfamcParser.OpenAmc("TestMotion")

        viz = visualiser(asf=asfamcParser.asf, amc=asfamcParser.amc)
        viz.visualiseBaseSkeleton()
        print(asfamcParser.amc.frameCount)
        viz.visualiseFrame(10)
        
if __name__ == "__main__":
    unittest.main()
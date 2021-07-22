import unittest
from unittest.main import main
from asfamcparser import Joint, AMC, ASF, Parser
from math import inf

class ASFUnitTests(unittest.TestCase):
    pass

class AMCUnitTests(unittest.TestCase):
    pass

class ParserUnitTests(unittest.TestCase):
    pass

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
        testString = "\t5.5\t5.6\t6.8"
        testJoint._axisOrder = ["X","Y","Z"]
        testJoint.axis = testString
        self.assertDictEqual(testJoint.axis, {"X":5.5,"Y":5.6,"Z":6.8})

    def test_dofSetter(self):
        testJoint = Joint("Test")
        testJoint.dof = "\trx\try\trz"
        self.assertEqual(testJoint.dof, ["rx","ry","rz"])

    def test_limitsSetter(self):
        testJoint = Joint("Test")
        testJoint._dof = {"rx":None, "ry":None, "rz":None}
        testJoint.limits = ["(-inf\tinf)","(-inf\tinf)","(-inf\tinf)"]
        self.assertDictEqual(testJoint.limits, {"rx":[-inf,inf],"ry":[-inf,inf],"rz":[-inf,inf]})

    def test_valuesSetter(self):
        testJoint = Joint("Test")
        testJoint._dof = {"rx":None, "ry":None, "rz":None}
        testJoint.values = "\t5.6\t7.8\t9.0"
        self.assertDictEqual(testJoint.values, {"rx":5.6, "ry":7.8, "rz":9.0})

if __name__ == "__main__":
    unittest.main()
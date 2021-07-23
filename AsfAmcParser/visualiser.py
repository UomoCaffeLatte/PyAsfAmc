import logging
from asfamcparser import Joint, AMC, ASF
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3
from transforms3d.euler import euler2mat

class visualiser:
    def __init__(self, asf:ASF, amc:AMC) -> None:
        self._asf = asf
        self._amc = amc
        self._vectors = {}
        self._baseVectors = {}
        self.CreateSkeletalVectors()

    def CreateSkeletalVectors(self, joint="root", parentJoint="None"):
        # calculate position
        # pass into child joints

        if joint == "root":
            rootPos = [self._asf["root"].axis["TX"], self._asf["root"].axis["TY"], self._asf["root"].axis["TZ"]]
            self._baseVectors["root"] = rootPos
        else:
            parentPos = self._baseVectors[parentJoint]
            self._baseVectors[joint] = [sum(x) for x in zip(parentPos, self._asf[joint].direction)]

        children = self._asf.hierarchy.get(joint,None) 
        if children != None:
            for childJoint in children:
                self.CreateSkeletalVectors(joint=childJoint, parentJoint=joint)

    def CreateFrameVectors(self, frame:int=0):
        frameValues = self._amc.frames[frame]

        if len(self._baseVectors) == 0:
            logging.error("baseSkeleton vectors not created. Run CreateSkeletalVectors first!")
            return
        
        for joint in self._asf.getJointNames:
            value = frameValues[joint]
            if joint == "root":
                value = frameValues[joint][3:]
            
            rotEulerRad = np.deg2rad(value)
            rotMat = euler2mat(*rotEulerRad)
            self._vectors[joint] = rotMat.dot(self._baseVectors[joint])

    def visualiseBaseSkeleton(self) -> None:
        # check vectors not empty
        if len(self._baseVectors) == 0:
            logging.error("Vectors empty. Cannot visualise.")
            return
        # plot
        self._viz(self._baseVectors)

    def visualiseFrame(self):
        if len(self._vectors) == 0:
            logging.error("No frame data read. Run CreateFrameVectors first.")
        # plot
        self._viz(self._vectors)

    def _viz(self,values:dict):
        # create figure
        fig = plt.figure(figsize=(4,4))
        # create 3d axes
        ax = fig.add_subplot(111, projection="3d")
        for joint, children in self._asf.hierarchy.items():
            parentPos = values[joint]
            for child in children:
                childPos = values[child]
                ax.plot([parentPos[0],childPos[0]],[parentPos[1],childPos[1]],[parentPos[2],childPos[2]],"r-")

        ax.plot([x[0] for _,x in values.items()],[x[1] for _,x in values.items()],[x[2] for _,x in values.items()],"go")
        plt.show()
    
    def _animation(self):
        pass
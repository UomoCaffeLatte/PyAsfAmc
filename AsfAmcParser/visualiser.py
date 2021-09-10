import logging

from numpy.core.fromnumeric import amax
from asfamcparser import Joint, AMC, ASF
import numpy as np
from matplotlib import interactive, lines, pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3
from transforms3d.euler import euler2mat
from asfamcparser import Parser
import os

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
            # get parent position, first case will be root post
            parentPos = self._baseVectors[parentJoint]
            # look at direction of vector and create new vector based on the bone length
            self._baseVectors[joint] = [sum(x) for x in zip(parentPos, self._asf[joint].direction)]

        children = self._asf.hierarchy.get(joint,None) 
        if children != None:
            for childJoint in children:
                self.CreateSkeletalVectors(joint=childJoint, parentJoint=joint)

    def _CreateFrameVectors(self, frame:int=0):
        # create joint vector based on joint value at current frame
        frameValues = self._amc.frames[frame]

        if len(self._baseVectors) == 0:
            logging.error("baseSkeleton vectors not created. Run CreateSkeletalVectors first!")
            return
        
        for joint in self._asf.getJointNames:
            value = frameValues[joint]

            parentJoint = None
            # Find joint value parent if given one, NOT PERFORMANT DO THIS ONCE BEFORE?
            for parent, children in self._asf.hierarchy.items():
                for child in children:
                    if child == joint:
                        parentJoint = parent

            if joint == "root":
                value = frameValues[joint][3:]
            
            # Apply parent rotation
            if parentJoint != None:
                parentRotEulerRad = np.deg2rad(frameValues[parentJoint])
                parentRotMat = euler2mat(parentRotEulerRad[0],parentRotEulerRad[1],parentRotEulerRad[2],axes= 'sxyz')
                self._vectors[joint] =parentRotMat.dot(self._baseVectors[joint])

            # Apply local rotation
            rotEulerRad = np.deg2rad(value)
            rotMat = euler2mat(rotEulerRad[0],rotEulerRad[1],rotEulerRad[2],axes= 'sxyz')
            self._vectors[joint] = rotMat.dot(self._baseVectors[joint])
        
        return self._vectors

    def visualiseBaseSkeleton(self) -> None:
        # check vectors not empty
        if len(self._baseVectors) == 0:
            logging.error("Vectors empty. Cannot visualise.")
            return
        # plot
        self._viz(self._baseVectors)

    def visualiseFrame(self, frame:int=0):
        # create frame vectors
        self._CreateFrameVectors(frame=frame)
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
    
    def play(self):
        # create figure
        fig = plt.figure()
        # create 3d axes
        ax = p3.Axes3D(fig, azim=117, elev=17)
        # setup axis labels 
        ax.set_xlabel("X")
        ax.set_xlim3d([-500,500])
        ax.set_ylabel("Z")
        ax.set_ylim3d([-500,500])
        ax.set_zlabel("Y")
        ax.set_zlim3d([-500,500])
        # joint plot
        points, = ax.plot([],[],[],"go")
        # time plot top right
        time_text = ax.text3D(100,-100,100,'')
        # bone plots, each plot is one line plot
        bonePlots = [ax.plot([],[],[],"r-")[0] for i in range(0, len(self._asf.getJointNames))]

        def animate(i):
            frameValues = self._amc.frames[i]
            jointValues = {}

            for j in self._asf.getJointNames:
                value = frameValues[j]
                parentJoint = None
                # Find joint value parent if given one, NOT PERFORMANT DO THIS ONCE BEFORE?
                for parent, children in self._asf.hierarchy.items():
                    for child in children:
                        if child == j:
                            parentJoint = parent

                if j == "root":
                    value = frameValues[j][3:]
                    parentJoint = None
                
                # Apply parent rotation and position
                if parentJoint != None:
                    posValue = frameValues[parentJoint]
                    parentRotEulerRad = np.deg2rad(posValue)

                    if parentJoint == "root":
                        posValue = frameValues[parentJoint][3:]
                        parentRotEulerRad = np.deg2rad(posValue)
                    
                    parentRotMat = euler2mat(*parentRotEulerRad)
                    jointValues[j] = parentRotMat.dot(self._baseVectors[j])

                # Apply local rotation
                rotEulerRad = np.deg2rad(value)
                rotMat = euler2mat(*rotEulerRad)
                if parentJoint != None:
                    jointValues[j] = rotMat.dot(jointValues[j])
                else:
                    jointValues[j] = rotMat.dot(self._baseVectors[j])

            # add joint line if any children
            bonePlotsCounter = 0
            for parent in self._asf.hierarchy.keys():
                for child in self._asf.hierarchy[parent]:
                        childPos = jointValues[child]
                        parentPos = jointValues[parent]
                        pointSet = [[parentPos[0],childPos[0]],[parentPos[1],childPos[1]],[parentPos[2], childPos[2]]]
                        bonePlots[bonePlotsCounter].set_data(np.array(pointSet[0]), np.array(pointSet[1]))
                        bonePlots[bonePlotsCounter].set_3d_properties(np.array(pointSet[2]))
                        bonePlotsCounter += 1

            # set points
            x = np.array([jointValues[j][0] for j in self._asf.getJointNames])
            y = np.array([jointValues[j][1] for j in self._asf.getJointNames])
            z = np.array([jointValues[j][2] for j in self._asf.getJointNames])
            points.set_data(x,y)
            points.set_3d_properties(z)
            # set time text
            time_text.set_text(f"Time (s): {i/self._amc.fps:0.2f}")
            return points,time_text, *bonePlots
        
        animJoints = FuncAnimation(fig, animate, frames = self._amc.frameCount, interval=(1000/self._amc.fps), blit=True)
        plt.show()


if __name__ == "__main__":
    wdr = os.path.dirname(os.path.realpath(__file__))

    asfamcParser = Parser(wdr)
    
    asfamcParser.OpenAsf("146")
    asfamcParser.OpenAmc("146_ArmClapOverHead")

    viz = visualiser(asf=asfamcParser.asf, amc=asfamcParser.amc)
    viz.visualiseFrame(36)
    viz.play()
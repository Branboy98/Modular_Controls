from maya import cmds
from Modular_Controls import Control

#This creates a baseWindow class for a groundwork for other UIs
class baseWindow(object):
    
    windowName = "BaseWindow"


# show method to have user see UI
    def show(self):
        
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()

    def buildUI(self):

        pass

    def reset(self, *args):
        
        pass


# close method to delete the UI
    def close(self, *args):
        cmds.deleteUI(self.windowName)


class ControlUI(baseWindow):

    windowName = "ControlWindow"

    def __init__(self):
        self.control = None

    def buildUI(self):
        #columns and rows setup how the UI looks
        column = cmds.columnLayout()
        cmds.text(label="Use the slider for the amount of Controls")

        cmds.rowLayout(numberOfColumns=4)
        # Defaults the slider's label to 3 
        self.label = cmds.text(label="3")
        # Creates the slider that on drag will run a method to in real time change out what the label shows
        self.slider = cmds.intSlider(min=1, max=15, value=3, step=1, dragCommand=self.modifyControlNum)
        # Creates button to automatically change slider depending on how long the joint chain is
        cmds.button(label="Auto-Amount", command=self.autoControlNum)
        # Button to reset slider to start
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        # Button to make the controls for the joints
        cmds.button(label="Make Controls", command=self.makeControls)
        
        
        cmds.setParent(column)
        # Button to close the UI
        cmds.button(label="Close", command=self.close)

    # Method to change the label for the slider when slider is moved
    def modifyControlNum(self, jointAmount):
        cmds.text(self.label, edit=True, label=jointAmount)

    # Method that will autochange the label and slider to the joint chain length, a bit messy but works!
    def autoControlNum(self, *args):
        selectedJoints=cmds.ls(selection=True, dag=True, long=False)
        jointsNum = len(selectedJoints)
        cmds.intSlider(self.slider, edit=True, value=jointsNum)
        cmds.text(self.label, edit=True, label=jointsNum)

    # Method to run the methods within the Control class from the CtrlinatorClassCreator.py file to make the controls down the chain! 
    def makeControls(self, *args):
        jointAmount = cmds.intSlider(self.slider, query=True, value=True)

        self.control = Control()

        self.control.controlChain(jointAmount=jointAmount)

    # Method to reset the slider and the label
    def reset(self, *args):
        self.control = None
        cmds.intSlider(self.slider,edit=True, value=3 )
        cmds.text(self.label, edit=True, label=3)





import maya.cmds as cmds

class Control(object):
    # However this CLASS is setup is causing the syntax error in Python3, NOT importing it!
    
    # This makeControl function takes selectedJoint as an argument and uses it's position and radius to scale/position a new 
    # control with an offset and grp group above it! 

    """
    This is a Control object that lets us create and modify controls that go down a joint chain
    """

    def __init__(self):

        # The init method lets us set default values
        
        self.selectedJoints = 0        
        self.jointAmount = 0 
        

    def makeControl(self,selectedJoint):
        
        jointRadius = cmds.getAttr('%s.radius' % selectedJoint)
        
        # var that holds the control's name and the cmds command to create the circle! The 180 rotates the control to lineup for
        # when it's snapped to the joint
        ctrlName = selectedJoint+"_ctrl"
        cmds.circle( n=ctrlName, nr=(180, 0, 0), c=(0, 0, 0) )
        
        # Scales the control by the jointRadius so the control isn't too big or small
        cmds.setAttr('%s.scale' % ctrlName, jointRadius,jointRadius,jointRadius) 
        
        # Freezes transforms so control doesn't have non 1 Scale
        cmds.makeIdentity(ctrlName, apply=True)
        
        # Deletes history so control is clean
        cmds.delete(ctrlName, constructionHistory=True)
        
        # Creates offset group's name in a var then creates the group itself.
        offsetName = selectedJoint+"_offset"
        cmds.group( em=True, name=offsetName )
        
        # Creates grp group's name in a var then creates the group itself.
        groupName = selectedJoint+"_grp"
        cmds.group( em=True, name=groupName )
        
        # Parents the ctrl to the offset and the offset to the grp!
        cmds.parent(ctrlName,offsetName)
        cmds.parent(offsetName,groupName)
        

        
        # Creates a parentconstraint between joint and grp to snap it to the joint and the next line removes the constraint
        cmds.parentConstraint(selectedJoint, groupName, maintainOffset = False)
        cmds.parentConstraint(selectedJoint, groupName, remove=True)
        
        # Creates a parentconstraint where now the joint is being constrained by the joint!
        cmds.parentConstraint(ctrlName, selectedJoint)
        
        # Returns a LIST with 0 holding the ctrlName and 1 holding the groupName
        return [ctrlName,groupName]
    
        
    # Creates var to hold all the selected joints, which is ALL joints that are parented to the selected one.

    def controlChain(self,jointAmount=0):

        selectedJoints=cmds.ls(selection=True, dag=True, long=False)


        Outputs = []
        i = 0
        
        while i < jointAmount:
            
            print (i)
        # Makes short list called Output to hold grp and ctrl
            Output = self.makeControl(selectedJoints[i])
        
        # Appends the Outputs list with the grp and ctrl from Output
            Outputs.append(Output[0])
            Outputs.append(Output[1])
        
        # Equation that gives list number for the right Grp   
            chainGrp = i*2 + 1
        
        # Equation that gives list number for the right Ctrl  
    
            chainCtrl = i*2 - 2
            

        # After first loop this parents the Grp of object on the
        # lower chain to the Ctrl of the higher one
            if i >= 1:    
                cmds.parent(Outputs[chainGrp], Outputs[chainCtrl])

            
            
        # Increase i by 1 each loop   
            i += 1
            print (Outputs)
    
            

    #controlChain(selectedJoints, jointAmount)
    
    









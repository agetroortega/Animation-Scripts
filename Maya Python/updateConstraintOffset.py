# This only works for parent constraints (at the moment)
from maya import cmds

def updateConstraintOffset():
    """
    Update the slaves' offset, AKA constraint compensation.
    
    Steps to use:
    1) Reposition the salve\slaves you want to update
    2) Select them all
    3) Run the code
    
    This code will find every constraint in those slaves and update their offset to the new position.
    """
    
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.warning("Select something first")
        return
    
    updated_count = 0
    
    for obj in selection:
        constraint_list = cmds.listRelatives(obj, type='constraint')
        if not constraint_list:
            continue
        
        for constraint in constraint_list:
            # get target list AKA parent(s)  
            target_list = cmds.parentConstraint(constraint, query=True, targetList=True)

            # Do the actual updating of the offset
            cmds.parentConstraint(target_list, constraint, edit=True, maintainOffset = True)

            updated_count += 1
            
            
    if not updated_count:
        cmds.warning("No constraints found")
        return
        
    print "Updated {0} constraint{1}".format(updated_count, ["s",""][updated_count==1])
            
            
# Call function to run the code
updateConstraintOffset()
        

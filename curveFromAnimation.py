from maya import cmds
import logging

logger = logging.getLogger('CurveToolTest')

def curveFromAnim(animatedObject ,startFrame, endFrame, curveName='', cleanCurve=False):
    """
    Test, a bit hacky and messy.
    Go through the timeline, get the global translation of the object
    for each frame and use that to make a curve
    
    animatedObject (string): object to use to create curve
    startFrame (int): First frame number in range
    endFrame (int): Last frame number in range
    curveName (string): Give your curve a name, just put it between quotation marks
    cleanCurve (bool): Set to True (capitalized) to try to let maya try to rebuild the curve
    """
    cmds.select(animatedObject)
    # current frame to go back to
    currentFrame = cmds.currentTime(q=True) 
    
    frame_range = xrange(startFrame, endFrame)
    
    # points for the curve, dictionary {frmNumber: [p1, p2, p3]}
    points = {}
    
    # gather points per frame
    for frame in frame_range:
        cmds.currentTime(frame)
        tr_matrix = cmds.xform(animatedObject, q=True, translation=True)
        points[frame] = tr_matrix
        
    # put all points together in a list    
    pointList = [tuple(points[k]) for k in sorted(points.keys())]
    
    # create curve
    newCurve = cmds.curve( point=pointList, worldSpace=True, degree=2)
    # maya will rebuild as nicely as possible
    if cleanCurve:
        logger.info("Rebuilding curve..")
        cmds.rebuildCurve(newCurve, rt=0)
        
    if curveName:
        curveName = cmds.rename(newCurve, curveName)
       
    # back to original frame
    cmds.currentTime(currentFrame)
    
    logger.info("Create curve: '%s'", curveName or newCurve)
    
    return curveName or newCurve

def curveFromSelection(startFrame, endFrame, curveName='', cleanCurve=False):
    """
    Creates curves on all selected objs
    startFrame (int): First frame number in range
    endFrame (int): Last frame number in range
    curveName (string): Give your curve a name, just put it between quotation marks
    cleanCurve (bool): Set to True (capitalized) to try to let maya try to rebuild the curve
    """
    sel = cmds.ls(selection=True)
    if not sel:
        logger.warning("Nothing selected")
        return []
    
    createdCurves = []
    for obj in sel:
        newCurve = curveFromAnim(obj ,startFrame, endFrame, curveName, cleanCurve)
        createdCurves.append(newCurve)
    return createdCurves

# usage: Select objects, pick your frames, run
# 1 - Simplest one
curveFromSelection(startFrame=1, endFrame=20)

# 2 - Try to rebuild\clean the curve
curveFromSelection(startFrame=1, endFrame=20, cleanCurve=True)

# 3 - Name the curves
curveFromSelection(startFrame=1, endFrame=20, curveName='superCurve')

# 4 - Name and try to rebuild\clean
curveFromSelection(startFrame=1, endFrame=20, curveName='superCurve', cleanCurve=True)

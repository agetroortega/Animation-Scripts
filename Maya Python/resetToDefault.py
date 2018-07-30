"""
Resets attributes to their defualt, instead of to 0.
You can paste this script as it is into Maya and it will work.
"""


from maya import cmds

def getSelectedChannels():
    """
    Returns selected attributes in the channel box.
    Queries the main, the shape and the input attrs.
    
    Returns list of selected channels.
    """
    channel_box = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')	#fetch maya's main channelbox
    selectedAttrs = []
    
    shapeAttrs = cmds.channelBox(channel_box, q=True, selectedShapeAttributes=True)
    mainAttrs = cmds.channelBox(channel_box, q=True, selectedMainAttributes=True)
    inputAttrs = cmds.channelBox(channel_box, q=True, selectedHistoryAttributes=True)
    
    if shapeAttrs:
        selectedAttrs.extend(shapeAttrs)
        
    if mainAttrs:
        selectedAttrs.extend(mainAttrs)
        
    if inputAttrs:
        selectedAttrs.extend(inputAttrs)
    
    return selectedAttrs

def resetToDefault():
    """
    Resets selected attributes to their default values. If no attributes are selected
    it resets all of them.
    """
    # get selection
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning('Select something first')
        return

    for ctrl in selection:
        # reset selected channels, if nothing is selected them reset all keyable    
        attrsToReset = getSelectedChannels() or cmds.listAttr(ctrl, keyable=True)
    
        if not attrsToReset:
            cmds.warning('Nothing to reset')
            return
        
        for attr in attrsToReset:
            attrFullName = "{0}.{1}".format(ctrl, attr)
            # TODO - Check if attr exists in the selection, try except for now
            # TODO 2 - Get input or shared attrs if nothing is selected
            try:
                # get default value
                defaultValue = cmds.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                # reset to default
                cmds.setAttr(attrFullName, defaultValue)
            except:
                pass
            
resetToDefault()
    
    

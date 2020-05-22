"""
Toggles between current viewport's camera and perspective.

To use, the the following 2 lines in a hotkey, shelf, etc:
import cam_toggle
cam_toggle.toggleCurrentCamera()
"""

import maya.cmds as cmds


class SavedCam(object):
    camName = ''

    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init()
        return it

    def init(self):
        pass


def getActiveViewport():
    activePanel = cmds.getPanel(withFocus=True)
    panelType = cmds.getPanel(typeOf=activePanel)
    if not panelType == 'modelPanel':
        cmds.warning('No viewport active')
        return
    return activePanel


def getViewportCam(viewport):
    return cmds.modelPanel(viewport, query=True, camera=True)


def setViewportCam(viewport, camName):
    msg = 'Switched to {}'.format(camName)
    cmds.inViewMessage(statusMessage=msg, fade=True)
    cmds.modelPanel(viewport, edit=True, camera=camName)


def toggleCurrentCamera():
    activeViewport = getActiveViewport()
    if activeViewport is None:
        return
    currentCam = getViewportCam(activeViewport)
    savedCam = SavedCam().camName
    if currentCam == 'persp':
        if not savedCam:
            cmds.warning('Do not know which camera to go to')
            return
        setViewportCam(activeViewport, savedCam)
        return

    if currentCam != savedCam:
        SavedCam().camName = currentCam

    setViewportCam(activeViewport, 'persp')

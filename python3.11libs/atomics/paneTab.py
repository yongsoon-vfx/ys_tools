import hou


def underCursor():
    return hou.ui.paneTabUnderCursor()


def underCursorNetwork():
    return hou.ui.paneTabUnderCursor().pwd()


def firstNetworkEditor():
    return hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)


def firstNetworkEditorNetwork():
    return hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd()

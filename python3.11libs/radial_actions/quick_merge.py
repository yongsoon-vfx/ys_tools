import hou


def make_merge(node: hou.Node):
    panetab_under_cursor = hou.ui.paneTabUnderCursor()
    cursor_pos = panetab_under_cursor.cursorPosition()
    current_node = panetab_under_cursor.pwd()
    obj_merge = current_node.createNode("object_merge")
    obj_merge.parm("objpath1").set(node.path())
    obj_merge.setPosition(cursor_pos)
    panetab_under_cursor.flashMessage(
        "hicon:/SVGIcons.index?STATUS_yes.svg",
        f"Created object_merge for {node.path()}",
        1,
    )
    hou.setSessionModuleSource("del(_grab_node)")
    return 0


def main(kwargs):
    print(kwargs)
    panetab_under_cursor = hou.ui.paneTabUnderCursor()
    try:
        grabbed_node = hou.session._grab_node
    except AttributeError:
        grabbed_node = hou.selectedNodes()[0] if hou.selectedNodes() else None
        if grabbed_node:
            append_str = f"_grab_node = hou.node('{grabbed_node.path()}')"
            hou.setSessionModuleSource(append_str)
            panetab_under_cursor.flashMessage(
                "hicon:/SVGIcons.index?BUTTONS_list_info.svg",
                f"Currently Grabbing {grabbed_node.path()}",
                5,
            )
            return 0
        else:
            panetab_under_cursor.flashMessage(
                "hicon:/SVGIcons.index?DIALOG_question.svg",
                "No node selected",
                1,
            )
            return 1

    make_merge(grabbed_node)
    return 0

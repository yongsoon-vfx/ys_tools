import hou

load_callback_script = r"""
current_node = kwargs["node"]
import json
data_node = hou.node(current_node.parm("__data_path").eval())
parm_str = data_node.userData("savedparm_%i")
if parm_str:
    parm_data = json.loads(parm_str)

    current_node.setFromData(parm_data)
    print("Loaded Parm Set %i")
else:
    print("Parm Set %i is empty")
"""

save_callback_script = r"""
current_node = kwargs["node"]
node_parm_data = current_node.asData()
import json
data_str = json.dumps(node_parm_data, indent=4)

data_node = hou.node(current_node.parm("__data_path").eval())
data_node.setUserData("savedparm_%i",data_str)
print("Saved Parm Set %i")
"""


def callback_cleanup(event_type, **kwargs):
    # print(kwargs)
    current_node = kwargs["node"]
    data_node = hou.node(current_node.parm("__data_path").eval())
    print(f"Deleting linked object {data_node.path()}")
    data_node.destroy()
    print("Sucessfully cleaned up data node.")


def main(kwargs):
    NODE: hou.OpNode = hou.selectedNodes()[-1]

    parmTemplateGroup = NODE.parmTemplateGroup()
    node_name = NODE.name()
    parent_node = NODE.parent()

    # print(f"node name {node_name}")
    data_node_name = f"_{node_name}_store_parms_"
    data_node = parent_node.createNode(
        "null",
        data_node_name,
    )

    data_node_path = data_node.path()
    NODE.setUserData("_parms_data_", data_node_path)
    NODE.addEventCallback((hou.nodeEventType.BeingDeleted,), callback_cleanup)
    data_node.hide(True)

    folder = hou.FolderParmTemplate("__storeparms", "Stored Parms")
    data_node_parm = hou.StringParmTemplate(
        "__data_path",
        "Data Node Path",
        1,
        is_hidden=True,
    )

    save_folder = hou.FolderParmTemplate("__saveparms", "Save Parms")
    load_folder = hou.FolderParmTemplate("__loadparms", "Load Parms")
    save_folder.setFolderType(hou.folderType.Simple)
    load_folder.setFolderType(hou.folderType.Simple)

    for i in range(10):
        if i != 4:
            join_row = True
        else:
            join_row = False

        save_btn = hou.ButtonParmTemplate(
            f"savebtn_{i}",
            f"{i}",
            script_callback_language=hou.scriptLanguage.Python,
            join_with_next=join_row,
        )
        save_btn.setScriptCallback(save_callback_script.replace("%i", str(i)))
        save_folder.addParmTemplate(save_btn)

        load_btn = hou.ButtonParmTemplate(
            f"loadbtn_{i}",
            f"{i}",
            script_callback_language=hou.scriptLanguage.Python,
            join_with_next=join_row,
        )
        load_btn.setScriptCallback(load_callback_script.replace("%i", str(i)))
        load_folder.addParmTemplate(load_btn)

    folder.addParmTemplate(data_node_parm)
    folder.addParmTemplate(save_folder)
    folder.addParmTemplate(load_folder)

    parmTemplateGroup.append(folder)
    NODE.setParmTemplateGroup(parmTemplateGroup)
    NODE.parm("__data_path").set(data_node_path)

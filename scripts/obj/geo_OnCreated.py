node = kwargs['node']
def name_changed(node,event_type,**kwargs):
    import re
    node_name = node.name()
    x = re.search(r"^RNDR",node_name)
    if x:
        node.setColor(hou.Color([1,0,0]))
        node.setUserData('nodeshape','circle')
    


if node:
    node.addEventCallback((hou.nodeEventType.NameChanged, ),name_changed)


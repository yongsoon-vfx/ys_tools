node = kwargs['node']
def changeColor(node,event_type,**kwargs):
    r = node.parm('colorr').eval()
    g = node.parm('colorg').eval()
    b = node.parm('colorb').eval()
    node.setColor(hou.Color([r,g,b]))


if node:
    node.addParmCallback(changeColor,['color'])



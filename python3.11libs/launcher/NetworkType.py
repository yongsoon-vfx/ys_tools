from enum import Enum

import hou


class NetworkType(Enum):
    OBJ = "obj"
    SOP = "sop"
    SHOP = "shop"
    COP = "cop"
    VOP = "vop"
    DOP = "dop"
    CHOP = "chop"
    ROP = "rop"
    TOP = "top"
    LOP = "lop"

    @staticmethod
    def get_network_type(node: hou.Node):
        if node.childTypeCategory() == hou.sopNodeTypeCategory():
            return NetworkType.SOP
        elif node.childTypeCategory() == hou.objNodeTypeCategory():
            return NetworkType.OBJ
        elif node.childTypeCategory() == hou.shopNodeTypeCategory():
            return NetworkType.SHOP
        elif node.childTypeCategory() == hou.copNodeTypeCategory():
            return NetworkType.COP
        elif node.childTypeCategory() == hou.vopNodeTypeCategory():
            return NetworkType.VOP
        elif node.childTypeCategory() == hou.dopNodeTypeCategory():
            return NetworkType.DOP
        elif node.childTypeCategory() == hou.chopNodeTypeCategory():
            return NetworkType.CHOP
        elif node.childTypeCategory() == hou.ropNodeTypeCategory():
            return NetworkType.ROP
        elif node.childTypeCategory() == hou.topNodeTypeCategory():
            return NetworkType.TOP
        elif node.childTypeCategory() == hou.lopNodeTypeCategory():
            return NetworkType.LOP
        return None

node = kwargs["node"]
exec(node.type().definition().sections()["OnCreated"].contents())

node.parm("xn__redshiftlightRSL_lightGroup_control_4xbf").set("$OS")

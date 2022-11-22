复制以下代码到maya脚本中，注意：在Maya17下使用、将第一行路径'/mnt/public/Share/qinlingbo/python/maya_script'替换为transfer uv文件甲之上的路径。比如把此文件甲放在了f盘下，那就把下面路
径改成F:文件夹在自己本地的路径

。如果运行报错，将__init__.py此文件考到transfer uv文件甲之上的路径也就是F盘下，即可



import sys

sys.path.append('/mnt/public/Share/qinlingbo/python/maya_script')
from  transfer_uv import transfer_uv_tools;
reload(transfer_uv_tools);
window = transfer_uv_tools.showWindow()



#####





以下是简单说明：
第一个选项卡：transform_uv_by_group，在组之间传递UV，选中一系列组，点击按钮，会将第一个组的uv传递给其他组。

第二个选项卡：选中一个组，点击analyze，
将会选中组中唯一的物体，然后展uv，还想选中唯一的物体，点击：select unique objects，transform_uv将会把唯一拓扑物体的uv传递给组内其他物体。

第三个选项卡：
选中一个物体（可以加选你想寻找的组），look for unique object，会选中和所选物体拓扑一致的物体，tranform_uv传递uv。

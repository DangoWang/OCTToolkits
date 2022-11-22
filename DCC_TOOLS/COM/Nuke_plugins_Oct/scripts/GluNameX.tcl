#rev 0.1

proc GluNameX {} {

set node [selected_node]

if {[class $node] == "Write"} {

set shot_name [regsub -all "(_v\[0-9\]+)" [file rootname [file tail [value root.name]]] ""]

set shot_name_1 [regsub -all "_comp" $shot_name ""]

set shot_vers [version_get [file tail [value root.name]] "v"]

knob $node.file X:/SAVVA/result/Feature/$shot_name_1/comp/v$shot_vers/$shot_name_1\_comp_v$shot_vers\_%v.%04d.jpg

knob $node.file_type jpg

knob $node._jpeg_quality 1

file mkdir [file dirname [filename $node]]

}

}
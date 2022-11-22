proc GluWriteTab {} {
	set curNode [stack 0]
 addUserKnob node $curNode 20 Add
 addUserKnob node $curNode 26 "" l "Work"
 addUserKnob node $curNode 32 GluName l "Disk_X" t "Name for test files" -STARTLINE T GluNameX
 addUserKnob node $curNode 32 GluName l "Disk_D" t "Name for test files" -STARTLINE T GluNameD
 addUserKnob node $curNode 26 "" l "Final"
 addUserKnob node $curNode 32 GluName l "Exr" t "Name for final files" -STARTLINE T GluNameFinal
 addUserKnob node $curNode 32 GluName l "Jpg" t "Name for final files" -STARTLINE T GluNameFinalJpg
 
}
from maya import cmds

def MGP_Translate(idStr):
    if not hasattr(cmds, 'MGPickerService'):
        return idStr

    return cmds.MGPickerService(tr=idStr)


def MGP_Translate_rep1(idStr, sub):
    if not hasattr(cmds, 'MGPickerService'):
        return idStr
    
    return cmds.MGPickerService(tr1=(idStr, sub))


def MGP_Translate_rep2(idStr, sub1, sub2):
    if not hasattr(cmds, 'MGPickerService'):
        return idStr
    
    return cmds.MGPickerService(tr2=(idStr, sub1, sub2))
    

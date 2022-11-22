def Xable(list,list2):
    trigger = True
    
    for i in list:
        Buf = nuke.Tab_Knob("Buffer")
        Ex = nuke.String_Knob("expr", "expr")

        if i['disable'].hasExpression():
            expr = i['disable'].toScript()
            if expr != '{"\$gui"}':
                i.addKnob(Buf)
                i.addKnob(Ex)
                i['expr'].setValue(expr)
                i['disable'].setExpression('$gui')
                
                break
           
            i['disable'].setExpression('')
            i['disable'].clearAnimated()

            if(i.knob('expr')):
                exp = i.knob('expr')
                user = i.knob('Buffer')
                expr = i['expr'].toScript()
                expr=expr.replace('{','')
                expr=expr.replace('}','')
                i['disable'].setExpression(expr)
                i.removeKnob(exp)
                i.removeKnob(user)
                if i.clones():
                    for j in list2:
                        if j.name() == i.name() and j.knob('expr'):
                            j.removeKnob(exp)
                            j.removeKnob(user)
            trigger = False
       

    if(trigger):
        
        for i in list:
            if i['disable'].hasExpression():
               i['disable'].setExpression('')
               i['disable'].clearAnimated()
            else:
                if(i.knob('expr')):
                    exp = i.knob('expr')
                    user = i.knob('Buffer')
                    expr = i['expr'].toScript()
                    expr=expr.replace('{','')
                    expr=expr.replace('}','')
                    i['disable'].setExpression(expr)
                    i.removeKnob(exp)
                    i.removeKnob(user)
                    break
            i['disable'].setExpression('$gui')

def GUI():
    
    ListRaw = nuke.selectedNodes()
    ListClone,idd=[],[]
    for i in ListRaw:
        if i.clones():
            for j in nuke.allNodes():
                if i.name() == j.name():
                    if id(j) in idd:
                        break
                    else:
                        idd.append(id(j))
                        ListClone.append(j)
        else:
            ListClone.append(i)
    if ListClone:
        ListRaw = ListClone 

    rsmb  = nuke.allNodes('OFXcom.revisionfx.rsmb_vectors_v3')
    Zdof   = nuke.allNodes('ZDefocus2')
    
    if ListRaw == []:
        for i in Zdof:
            rsmb.append(i)
        ListRaw = rsmb
    ListClean = set([i.name() for i in ListRaw])
    ListClean = [nuke.toNode(i) for i in ListClean]
    
    Xable(ListClean,ListRaw)

GUI()
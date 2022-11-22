import subprocess

#----------------------------------------------------------------------
def MG_StartProcess( programFile, args ):
    """"""
    argList = args.split(' ')	
    argList.insert(0,programFile)
    #print argList
    subprocess.Popen(argList)

#MG_StartProcess ("E:/MGTools3-Project/MG-Login/release/MG-Login.exe", "-mode quite -action logout")

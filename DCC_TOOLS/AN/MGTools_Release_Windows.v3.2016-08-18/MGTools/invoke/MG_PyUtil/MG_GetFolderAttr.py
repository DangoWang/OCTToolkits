import os
def MGgetFolderReadable(folder):
  return os.access(folder, os.R_OK)  

def MGgetFolderWritable(folder):
  return os.access(folder, os.W_OK)

#if __name__ == '__main__':
#    MGgetFolderReadable ('E:/Data/Char')    
#    MGgetFolderWritable ('E:/Data/Char')    

import urllib
import maya.mel as mel
import thread
import maya.utils as utils

def MG_executeMelCallback(melCallback):
    if len(melCallback):
        mel.eval(melCallback)

def MG_downloadFile_Async (fileUrl, localTargetPath, melSuccessCallback = '', melFailCallback = ''):
    """This function should be invoked in main thread"""
    thread.start_new_thread(MG_downloadFile_doit,(fileUrl, localTargetPath,melSuccessCallback,melFailCallback))


def MG_downloadFile_doit (fileUrl, localTargetPath, melSuccessCallback, melFailCallback):
    """The function should be called within other thread, not main thread"""
    try:
        urllib.urlretrieve(fileUrl,localTargetPath)
        if len(melSuccessCallback):
            partFunc = (lambda : MG_executeMelCallback(melSuccessCallback)) 
            utils.executeInMainThreadWithResult(partFunc)
    except:
        if len(melFailCallback):
            partFunc = (lambda : MG_executeMelCallback(melFailCallback)) 
            utils.executeInMainThreadWithResult(partFunc)

def MG_downloadFileList_Async (urlList, localPathList, melSuccessCallbackList = [], melFailCallbackList = []):
    """
    This function should be invoked in main thread.
    widgetList is used to be update the widget using the downloaded file.
    melSuccessCallback should something like global proc  procName (string $localPath, string $widget);
    """
    thread.start_new_thread(MG_downloadFileList_doit,(urlList, localPathList, melSuccessCallbackList,melFailCallbackList))

def MG_downloadFileList_doit (urlList, localPathList, melSuccessCallbackList, melFailCallbackList):
    """The function should be called within other thread, not main thread"""
    minCount = min(len(urlList), len(localPathList))
    successFallbackLen = len(melSuccessCallbackList)
    failCallbackLen = len(melFailCallbackList)

    if not minCount:
        return

    for i in range(minCount):
        try:
            urllib.urlretrieve(urlList[i], localPathList[i])
        except:
            if i < failCallbackLen and len(melFailCallbackList[i]):
                partFunc = (lambda : MG_executeMelCallback(melFailCallbackList[i]))
                utils.executeInMainThreadWithResult(partFunc)
        finally:
            if i < successFallbackLen and len(melSuccessCallbackList[i]):
                partFunc = (lambda : MG_executeMelCallback(melSuccessCallbackList[i]))
                utils.executeInMainThreadWithResult(partFunc)
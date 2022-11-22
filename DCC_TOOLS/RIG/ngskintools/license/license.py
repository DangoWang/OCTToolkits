#
#    ngSkinTools
#    Copyright (c) 2009-2017 Viktoras Makauskas.
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by EULA.
#         
#    A copy of EULA can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

import os
from maya import cmds
from ngSkinTools.license import fileFormat
from ngSkinTools.log import getLogger
from ngSkinTools.ui.events import Signal

from ngSkinTools.ui.options import PersistentValueModel
from ngSkinTools.utils import Utils

savedLicensePath = PersistentValueModel("ngSkinToolsOption_licensePath")

log = getLogger("license")

class LicenseType:
    RLM = "rlm-ez"
    NGSTKEY = "ngstKey"

class Status:
    '''
    given licensePath, track license status.
    works both with ngstKey licenses and RLM licenses
    '''


    def __init__(self):
        '''
        :param str licensePath:
        :param Server licenseServerInterface:
        '''
        self.licensePath = None
        self.status = None
        self.changed = Signal("licenseStatus")

    def setLicensePath(self, licensePath):
        self.licensePath = licensePath
        self.recalculate()

    def setStatus(self, status):
        log.info("changing license status to %s", status)
        self.status = status
        self.changed.emit()

    def recalculate(self):
        if self.licensePath is None:
            self.licensePath = getLicensePath()

        ngstKeyLicenses = fileFormat.discoverLicenseFiles(self.licensePath)
        if len(ngstKeyLicenses) == 0:
            # no ngstkey licenses found, checking RLM
            self.setStatus(cmds.ngSkinToolsLicense(validateLicense=True, licensePath=self.licensePath))
        else:
            for license in ngstKeyLicenses:
                status = cmds.ngSkinToolsLicense(validateLicense=True,
                                                      hostid=license.get('hostid'),
                                                      licenseKey=license.get('licensekey'),
                                                      licenseType=license.get('licenseType'),
                                                      signature=license.get('sig')
                                                      )
                if status == 0:
                    self.setStatus(status)
                    break

        return self.status

    def isLicenseActive(self):
        return self.status == 0

    def getDefaultLicenseFileName(self):
        return os.path.join(self.licensePath, "ngskintools.lic")

class Downloader:
    def __init__(self):
        self.licenseServer = 'https://licensing.ngskintools.com/api/projects/ngskintools/licenses/'

    def getNgstKeyHostId(self):
        result = cmds.ngSkinToolsLicense(q=True, hostid=True)
        return result

    def getRlmHostId(self):
        '''
        executes RLM host id and returns the result
        '''
        import subprocess
        import os.path as path
        toolsPath = path.abspath(path.join(path.dirname(__file__), "..", "tools"))

        operatingSystem = Utils.getOs()

        isLinux = operatingSystem == "linux"
        isOsx = operatingSystem == 'mac'
        useTemporaryExecutable = isLinux or isOsx

        rlmHostId = "rlmhostid.exe"
        if isLinux:
            rlmHostId = "rlmhostid-linux"
        if isOsx:
            rlmHostId = "rlmhostid-osx"

        executeCommand = [path.join(toolsPath, rlmHostId)]
        executeCommand.append("-q")

        if useTemporaryExecutable:
            # some instalation methods (extracting a zip) might not set the executable flags,
            # and we are probably better of just making a temporary executable with proper flags
            # ...and we've just discovered that the executable needs to be called exactly "rlmhostid"
            import tempfile, shutil, os
            temporaryDirectory = tempfile.mkdtemp()
            temporaryExecutable = os.path.join(temporaryDirectory, "rlmhostid")

            shutil.copy2(executeCommand[0], temporaryExecutable)
            executeCommand[0] = temporaryExecutable
            os.chmod(executeCommand[0], 0777)

        try:
            result = subprocess.check_output(executeCommand, stdin=subprocess.PIPE).strip()
        finally:
            if useTemporaryExecutable:
                os.unlink(temporaryExecutable)
                os.rmdir(temporaryDirectory)

        # rlmhostid returns zero even in case of errors; rely on the output to detect execution errors
        if "rlmhostid" in result:  # probably some kind of errors showing tool usage
            raise Exception("rlmhostid failed to execute.")
        return result

    def guessHostId(self):
        licenseFileType = 'ngstKey'
        hostId = self.getNgstKeyHostId()

        if hostId is None:
            licenseFileType = 'rlm-ez'
            hostId = self.getHostId()

        return hostId, licenseFileType

    def downloadLicenseFile(self, licenseKey, licenseFileType, hostId, fileLocation):
        '''
        exchanges licenseKey+hostId for a licenseFile online.
        Operation will fail if license file already exists (won't overwrite)
        '''

        if os.path.exists(fileLocation):
            raise Exception("License file '{0}' already exists".format(fileLocation))

        # download now
        import urllib2
        import json
        try:
            req = urllib2.Request(self.licenseServer + licenseKey)
            resp = urllib2.urlopen(req, json.dumps({"hostId": hostId, "licenseFileType": licenseFileType}))
            result = json.load(resp)
            contents = result['licenseFile']
        except urllib2.HTTPError, err:
            message = str(err)
            try:
                message = json.load(err)['message']
            except:
                pass
            raise Exception("Failed downloading license file ({0}): {1}".format(err.getcode(), message))
        except Exception, err:
            raise Exception("Failed downloading license file: unknown error ({0})".format(str(err)))

            # save to file
        with open(fileLocation, "w") as f:
            f.write(contents)


def setCustomLicensePath(path):
    savedLicensePath.set(path)
    status.setLicensePath(path)


def getLicensePath():
    '''
    returns license path, checking configuration in priority:
        Maya's optionVar 'ngSkinToolsOption_licensePath'
        environment variable NGSKINTOOLS_LICENSE_PATH
        environment variable RLM_LICENSE
        Maya's user app dir
    '''

    def parsePathFromRlmLicense(licensePath):
        '''
        take a value in form of:

            license_spec1:license_spec2:license_spec3: .... :license_specN (UNIX)
            license_spec1;license_spec2;license_spec3; .... ;license_specN (Windows)

        ...and return first entry that is an existing directory.
        '''
        paths = licensePath.split(os.path.pathsep)
        for p in paths:
            if os.path.isdir(p):
                return p

        return None

    licensePath = savedLicensePath.get()
    if licensePath is None:
        licensePath = os.getenv("NGSKINTOOLS_LICENSE_PATH", None)
    if licensePath is None:
        licensePath = os.getenv("RLM_LICENSE", None)
        if licensePath is not None:
            licensePath = parsePathFromRlmLicense(licensePath)

    if licensePath is None:
        licensePath = cmds.internalVar(userAppDir=True)

    licensePath = os.path.normpath(licensePath)

    return licensePath

status = Status()

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

from ngSkinTools.license import license


class ActivationDialogModel(object):
    def __init__(self):
        self.licenseKey = ''
        self.errors = []

    def getLicenseFileLocation(self):
        return license.status.licensePath

    def reportError(self, error):
        self.errors.append(error)


    def getErrors(self):
        result = self.errors
        self.errors = []
        return result

    def setLicenseFileLocation(self, path):
        path = path.strip()
        if not os.path.isdir(path):
            self.reportError("Please select an existing directory for license file location")
            return

        license.setCustomLicensePath(path)

    def setLicenseKey(self, key):
        self.licenseKey = key.strip()
        if self.licenseKey == "":
            self.reportError("Enter license key to proceed")

    def downloadLicense(self):
        try:
            downloader = license.Downloader()
            downloader.downloadLicenseFile(licenseKey=self.licenseKey,
                                           licenseFileType=license.LicenseType.NGSTKEY,
                                           hostId=downloader.getNgstKeyHostId(),
                                           fileLocation=license.status.getDefaultLicenseFileName())
            license.status.recalculate()
        except Exception, err:
            self.reportError(str(err))

    def buildActivationEmailText(self):
        downloader = license.Downloader()
        return """
                <p>To: support@ngskintools.com</p>
                <p><b>License file request</b></p>

                <p>Please issue a license file for:</p>
                <ul>
                <li>License key: {licenseKey}</li>
                <li>Host id: {hostId}</li>
                </ul>
                """.format(licenseKey=self.licenseKey, hostId=downloader.getNgstKeyHostId())

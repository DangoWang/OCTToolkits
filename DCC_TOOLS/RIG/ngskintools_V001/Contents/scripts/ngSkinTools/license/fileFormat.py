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


def parseLicenseFile(contents):
    '''

    Example valid contents:

    LICENSE ngstkey ngskintools 1 standalone hostid=123-123
        sig=363c8f7f19679efc324b5ec713ffcf8968b3f4741b3b0d64f62436f8de799ec5

    For historical reasons, this is not a JSON.

    :param str contents:
    '''

    values = contents.split()
    if len(values) < 6:
        return None

    result = {}
    for index, v in enumerate(['stamp', 'fileType', 'product', 'productVersion', 'licenseType']):
        result[v] = values[index]

    if result['stamp'] != 'LICENSE':
        return None

    if result['fileType'] != 'ngstkey':
        return None

    for value in values[5:]:
        k, v = value.split("=", 2)
        result[k] = v

    # signature is required
    if result.get('sig', None) == None:
        return None

    if result.get('hostid', None) == None:
        return None

    return result


def discoverLicenseFiles(path):
    '''
    given a dir or file path, discover ngstkey license contents in files. only files that look like license files are parsed,
    and only those that match ngstkey file format are used.
    '''

    if os.path.isfile(path):
        contents = ""
        with open(path) as f:
            contents = f.read(7)
            if contents != 'LICENSE':
                return []
            contents += f.read()

        parsedContents = parseLicenseFile(contents)
        if parsedContents is None:
            return []

        return [parsedContents]

    if os.path.isdir(path):
        result = []
        for i in os.listdir(path):
            fileName = os.path.join(path, i)
            if os.path.isfile(fileName):
                result.extend(discoverLicenseFiles(fileName))

        return result

    return []

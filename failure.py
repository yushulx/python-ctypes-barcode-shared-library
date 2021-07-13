import os
import platform
from ctypes import *

system = platform.system()

class SamplingImageData(Structure):
    _fields_ = [("bytes", POINTER(c_byte)), ("width", c_int), ("height", c_int)]

class ExtendedResult(Structure):
    _fields_ = [("resultType", c_int),
                ("barcodeFormat", c_int),
                ("barcodeFormatString", c_char_p),
                ("barcodeFormat_2", c_int),
                ("barcodeFormatString_2", c_char_p),
                ("confidence", c_int),
                ("bytes", POINTER(c_byte)),
                ("bytesLength", c_int),
                ("accompanyingTextBytes", POINTER(c_byte)),
                ("accompanyingTextBytesLength", c_int),
                ("deformation", c_int),
                ("detailedResult", c_void_p),
                ("samplingImage", SamplingImageData),
                ("clarity", c_int),
                ("reserved", c_char * 40),
                ]

class LocalizationResult(Structure):
    _fields_ = [("terminatePhase", c_int), 
    ("barcodeFormat", c_int),
    ("barcodeFormatString", c_char_p),
    ("barcodeFormat_2", c_int),
    ("barcodeFormatString_2", c_char_p),
    ("x1", c_int),
    ("y1", c_int),
    ("x2", c_int),
    ("y2", c_int),
    ("x3", c_int),
    ("y3", c_int),
    ("x4", c_int),
    ("y4", c_int),
    ("angle", c_int),
    ("moduleSize", c_int),
    ("pageNumber", c_int),
    ("regionName", c_char_p),
    ("documentName", c_char_p),
    ("resultCoordinateType", c_int),
    ("accompanyingTextBytes", POINTER(c_byte)),
    ("accompanyingTextBytesLength", c_int),
    ("confidence", c_int),
    ("reserved", c_char * 52),
    ]

class TextResult(Structure):
    _fields_ = [("barcodeFormat", c_int), 
    ("barcodeFormatString", c_char_p), 
    ("barcodeFormat_2", c_int), 
    ("barcodeFormatString_2", c_char_p), 
    ("barcodeText", c_char_p), 
    ("barcodeBytes", POINTER(c_byte)),
    ("barcodeBytesLength", c_int),
    ("localizationResult", POINTER(LocalizationResult)),
    ("detailedResult", c_void_p),
    ("resultsCount", c_int),
    ("results", POINTER(POINTER(ExtendedResult))),
    ("exception", c_char_p),
    ("isDPM", c_int),
    ("isMirrored", c_int),
    ("reserved", c_char * 44),
    ]


class TextResultArray(Structure):
    _fields_= [("resultsCount",c_int),
              ("results", POINTER(POINTER(TextResult)))]

def load_dll(dll_path, dll_name):
    os.environ['path'] += ';' + dll_path
    if 'Windows' in system:                   
        dll = windll.LoadLibrary(dll_path + '\\' + dll_name)
    else:
        dll = CDLL(os.path.join(dll_path, dll_name))
    return dll

dbr = None
if 'Windows' in system:         
    os.environ['path'] += ';' + os.path.join(os.path.abspath('.'), r'bridge\lib\Windows')
    dbr = windll.LoadLibrary('DynamsoftBarcodeReaderx64.dll')
else:
    dbr = CDLL(os.path.join(os.path.abspath('.'), 'bridge/lib/Linux/libDynamsoftBarcodeReader.so'))

# DBR_CreateInstance
DBR_CreateInstance = dbr.DBR_CreateInstance
DBR_CreateInstance.restype = c_void_p
instance = dbr.DBR_CreateInstance()

# DBR_InitLicense
DBR_InitLicense = dbr.DBR_InitLicense
DBR_InitLicense.argtypes = [c_void_p, c_char_p] 
DBR_InitLicense.restype = c_int
ret = DBR_InitLicense(instance, c_char_p('t0069fQAAAG1B1nLfAP6tE+J0FJCkhEnDg5eWbRtiICRrEsGSw4GewLbJQK+CSWIz1xtHp3hexsbwGZUPQ+PZV+U2kU/H+JL2'.encode('utf-8')))
print(ret)

# DBR_DecodeFile
DBR_DecodeFile = dbr.DBR_DecodeFile
DBR_DecodeFile.argtypes = [c_void_p, c_char_p, c_char_p]
DBR_DecodeFile.restype = c_int
ret = DBR_DecodeFile(instance, c_char_p('test.png'.encode('utf-8')), c_char_p(''.encode('utf-8')))
print(ret)

####################################################################################
# Failed to get barcode detection results
# DBR_GetAllTextResults
pResults = POINTER(TextResultArray)()
DBR_GetAllTextResults = dbr.DBR_GetAllTextResults
DBR_GetAllTextResults.argtypes = [c_void_p, POINTER(POINTER(TextResultArray))]
DBR_GetAllTextResults.restype = c_int
ret = DBR_GetAllTextResults(instance, byref(pResults))
print(ret)

resultsCount = pResults.contents.resultsCount
print(resultsCount)
results = pResults.contents.results
print(results)

if bool(results):
    for i in range(resultsCount):
        result = results[i] 
        if bool(result):
            print(result)
            print('Format: %s' % result.contents.barcodeFormatString.decode('utf-8'))                   
            print('Text: %s' % result.contents.barcodeText.decode('utf-8'))

# DBR_FreeTextResults
DBR_FreeTextResults = dbr.DBR_FreeTextResults
DBR_FreeTextResults.argtypes = [POINTER(POINTER(TextResultArray))]
if bool(pResults):
    DBR_FreeTextResults(byref(pResults)) 

####################################################################################       

# DBR_DestroyInstance
DBR_DestroyInstance = dbr.DBR_DestroyInstance
DBR_DestroyInstance.argtypes = [c_void_p]
DBR_DestroyInstance(instance)
import os
import platform
from ctypes import *

class ResultInfo(Structure):
    _fields_ = [("format", c_char_p), ("text", c_char_p)]

class ResultList(Structure):
    _fields_ = [("size", c_int), ("pResultInfo", POINTER(POINTER(ResultInfo)))]

system = platform.system()

dbr = None
bridge = None
if 'Windows' in system:                   
    os.environ['path'] += ';' + os.path.join(os.path.abspath('.'), r'bridge\lib\Windows')
    dbr = windll.LoadLibrary('DynamsoftBarcodeReaderx64.dll')
    bridge = windll.LoadLibrary(os.path.join(os.path.abspath('.'), r'bridge\build\Debug\bridge.dll'))
else:
    dbr = CDLL(os.path.join(os.path.abspath('.'), 'bridge/lib/Linux/libDynamsoftBarcodeReader.so'))
    bridge = CDLL(os.path.join(os.path.abspath('.'), 'bridge/build/libbridge.so'))

# DBR_CreateInstance
DBR_CreateInstance = dbr.DBR_CreateInstance
DBR_CreateInstance.restype = c_void_p
instance = dbr.DBR_CreateInstance()

# DBR_InitLicense
DBR_InitLicense = dbr.DBR_InitLicense
DBR_InitLicense.argtypes = [c_void_p, c_char_p] 
DBR_InitLicense.restype = c_int
ret = DBR_InitLicense(instance, c_char_p('LICENSE-KEY'.encode('utf-8'))) # https://www.dynamsoft.com/customer/license/trialLicense?product=dbr
print(ret)

# DBR_DecodeFile
DBR_DecodeFile = dbr.DBR_DecodeFile
DBR_DecodeFile.argtypes = [c_void_p, c_char_p, c_char_p]
DBR_DecodeFile.restype = c_int
ret = DBR_DecodeFile(instance, c_char_p('test.png'.encode('utf-8')), c_char_p(''.encode('utf-8')))
print(ret)

# dbr_get_results  
dbr_get_results = bridge.dbr_get_results
dbr_get_results.argtypes = [c_void_p]
dbr_get_results.restype = c_void_p
address = dbr_get_results(instance)
data = cast(address, POINTER(ResultList))
size = data.contents.size
results = data.contents.pResultInfo

for i in range(size):   
    result = results[i]                
    print('Format: %s' % result.contents.format.decode('utf-8'))                   
    print('Text: %s' % result.contents.text.decode('utf-8'))

# dbr_free_results
dbr_free_results = bridge.dbr_free_results
dbr_free_results.argtypes = [c_void_p]
if bool(address):
    dbr_free_results(address)        

# DBR_DestroyInstance
DBR_DestroyInstance = dbr.DBR_DestroyInstance
DBR_DestroyInstance.argtypes = [c_void_p]
DBR_DestroyInstance(instance)
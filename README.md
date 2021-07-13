# Python Ctypes for Dynamsoft Barcode Shared Library
An experiment demonstrates how to load and use Dynamsoft Barcode shared libraries by Python Ctypes.

## Why Ctypes?
Dynamsoft Barcode Reader for Python is implemented using CPython and has been released to pypi.org:

```bash
pip install dbr
```

The reason behind using Ctypes is to try another way to invoke C APIs in shared libraries in pure Python.

## Usage
1. Build the CMake project `bridge` which is located in the root directory of the project.
    
    ```bash
    # Windows
    cmake -DCMAKE_GENERATOR_PLATFORM=x64 ..
    cmake --build .

    # Linux
    cmake ..
    cmake --build .
    ```    

2. Get a valid license key from [Dynamsoft website](https://www.dynamsoft.com/customer/license/trialLicense?product=dbr) and update the line in `success.py`.

    ```python
    DBR_InitLicense(instance, c_char_p('LICENSE-KEY'.encode('utf-8')))
    ```

3. Run the `success.py` file.
    
    ```bash
    python success.py
    ```



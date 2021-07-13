# include "DynamsoftBarcodeReader.h"

#if !defined(_WIN32) && !defined(_WIN64)
#define EXPORT_API
#else
#define EXPORT_API __declspec(dllexport)
#endif

typedef struct {
    char* format;
    char* text;
} ResultInfo;

typedef struct {
    int size;
    ResultInfo** pResultInfo;
} ResultList;

EXPORT_API ResultList* dbr_get_results(void* barcodeReader);
EXPORT_API void dbr_free_results(ResultList* resultList);
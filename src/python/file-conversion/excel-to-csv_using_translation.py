from xlrd import open_workbook
import csv
import enum 
import os
import uuid

class DataType(enum.Enum): 
    header = 1
    value = 2

def stringTranslation(data : str, dataType: DataType, translations: dict) -> str:
    print(data)
    if dataType == DataType.header:
        data = data.replace("%", "Porc")
    return data.translate(translations)

# cambiar aqui la ruta y nombre del archivo fuente de datos
inputFile = "data/preciosEESS_es.xls"

fileDir, fileName = os.path.split(inputFile)
print("input file: " + inputFile)

try:
    wb = open_workbook(inputFile)
    sheetNames = [sheetName for sheetName in wb.sheet_names()]
    print(sheetNames)
    print("===========================")
    for idx, sheetName in enumerate(sheetNames):
        print("indice: {} - sheetName: {}".format(idx, sheetName))
    print("===========================")
    #for i in range(1, wb.nsheets):
        #sheet = wb.sheet_by_index(i)

    translations = str.maketrans("áéíóú ", "aeiou_")
    for sheetName in sheetNames:
        print("sheetName: {}".format(sheetName))
        sheet = wb.sheet_by_name(sheetName)
        print("nro filas: {} - nro columnas: {}".format(sheet.nrows, sheet.ncols))
        #print(sheet.name)
        outputFile = "data/out/{}-{}-{}.csv".format(fileName.replace(".xls", "0"), sheet.name.replace(" ",""), uuid.uuid4().hex)
        print("output file: " + outputFile)
        with open(outputFile, "w", newline='', encoding="utf-8") as csvfile:
            #writer = csv.writer(csvfile, delimiter = ";")
            writer = csv.writer(csvfile, delimiter=';', quotechar='', quoting=csv.QUOTE_NONE, escapechar='\\')
            headers = [stringTranslation(cell.value, DataType.header, translations) for cell in sheet.row(3)]
            print(headers)
            print('Col at 4th position: {}'.format(headers[4]))
            print('Col at 5th position: {}'.format(headers[5]))
            writer.writerow(headers)
            for row_idx in range(4, sheet.nrows):
                row = [int(cell.value) if isinstance(cell.value, float) else cell.value for cell in sheet.row(row_idx)]
                row[4] = stringTranslation(row[4], DataType.value, str.maketrans(";", "."))
                row[-1] = stringTranslation(row[-1], DataType.value, str.maketrans(";", ","))
                #print(row)
                writer.writerow(row)
except Exception as error:
    print("error!!!")
    print(error)

print("finish!!")

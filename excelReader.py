from xlrd import open_workbook


def readExcel(sheet_path):
    if sheet_path == "":
        return ""
    data = open_workbook(sheet_path)
    sheet = data.sheets()[0]
    rows = []
    max_rows = sheet.nrows
    for row in range(1,max_rows):
        row_value = sheet.row_values(row)[1:]
        if '' not in row_value:
            rows.append(row_value)
    return rows


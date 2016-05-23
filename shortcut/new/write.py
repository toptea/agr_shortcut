"""
The module contains functions that relies on Excel workbook COM object (wb)
to write data onto the jobcard. eg:

>>> import win32com.client
>>> excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
>>> wb = excel.Workbooks.Open(TEMPLATE)
"""
import logging

from . import load


def assy_tabs(wb, tabs):
    """
    using the pre-existing template, create a new jobcard with the
    assembly tabs defined
    """
    logging.info('creating new jobcard')
    for tab in sorted(tabs, reverse=True):
        logging.info('creating ' + str(tab) + ' worksheet')
        wb.Worksheets('-000-').Copy(After=wb.Worksheets('-000-'))
        wb.Worksheets('-000- (2)').Name = tab

    return wb


def __example(wb):
    """win32com excel example found online"""
    # excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
    # excel.Visible = True
    # wb = excel.Workbooks.Open(OUTPUT)
    ws = wb.Worksheets("Overview")
    ws.Cells(1, 1).Value = "Cell A1"
    ws.Cells(1, 1).Offset(2, 4).Value = "Cell D2"
    ws.Range("A2").Value = "Cell A2"
    ws.Range("A3:B4").Value = "A3:B4"
    ws.Range("A6:B7,A9:B10").Value = "A6:B7,A9:B10"
    # wb.SaveAs(OUTPUT)
    # excel.Application.Quit()
    return wb


def proj_head(wb, proj_head_data):
    """write project header data in jobcard's Overview tab"""
    logging.info("write project header in 'Overview'")
    print(proj_head_data)
    ws = wb.Worksheets("Overview")
    ws.Cells(5, 3).Value = proj_head_data['code']
    ws.Cells(6, 3).Value = proj_head_data['name']
    ws.Cells(7, 3).Value = proj_head_data['client']
    ws.Cells(8, 3).Value = proj_head_data['ijn']
    ws.Cells(12, 9).Value = proj_head_data['delivery_date']
    return wb


def assy_head(wb, assy_head_data):
    """write assembly header data in jobcard's Overview tab"""
    logging.info("write assembly header in 'Overview'")
    ws = wb.Worksheets("Overview")
    rows = assy_head_data.shape[0]
    cols = assy_head_data.shape[1]
    for row in range(0, rows):
        for col in range(0, cols):
            ws.Cells(row+13, col+1).Value = assy_head_data.iloc[row, col]
            col += 1
        row += 1
    return wb


def assy_part(wb, proj, top_lvl_assy, assy_head_data, cost_data):
    """
    while looping between the different assembly tabs in the jobcard,
    write the manufacture bom data in each section. Automatically insert
    more rows for large BOMs and indent cells to show sub-assemblies based
    on BOM level number.
    """
    dfs = {}
    for index, row in assy_head_data.iterrows():
        dfs[row.tab_name] = (
            load.assy_part(proj, top_lvl_assy, row.partcode, cost_data))

    for key in sorted(dfs):
        logging.info('write BOM in ' + str(key) + ' worksheet')
        ws = wb.Worksheets(key)

        rows = dfs[key].shape[0]
        if rows > 38:
            for i in range(rows-38):
                ws.Range("A30").EntireRow.Insert()

        initial_lvl = int(dfs[key].loc[0, 'lvl'])
        for index, row in dfs[key].iterrows():
            index = int(index)  # prevent MemoryError: CreatingSafeArray
            ws.Cells(index+21, 1).Value = row.partcode
            ws.Cells(index+21, 2).Value = row.rev
            ws.Cells(index+21, 3).Value = row.qty
            ws.Cells(index+21, 4).Value = row.desc
            ws.Cells(index+21, 5).Value = row.material
            ws.Cells(index+21, 8).Value = row.avg_time
            if row.lvl > initial_lvl:
                indent = row.lvl - initial_lvl
                ws.Cells(index+21, 1).InsertIndent(indent)
                ws.Cells(index+21, 4).InsertIndent(indent)

    return wb


def assy_name(wb, raw, top_lvl_assy):
    """write assembly name in overiew (assy_head missed this out)"""
    try:
        desc = raw[raw.partcode == top_lvl_assy].desc.values[0]
        ws = wb.Worksheets("Overview")
        ws.Cells(12, 5).Value = desc.strip()
    except:
        pass
    return wb

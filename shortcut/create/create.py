import win32com.client
import os

from . import load
from . import check
from . import write

TEMPLATE = r'C:\code\python\create_jobcard\test\jobcard.xls'
OUTPUT = r'C:\code\python\create_jobcard\test'


def get_filename(raw, proj, top_lvl_assy, ijn):
    try:
        desc = raw[raw.partcode == top_lvl_assy].desc.values[0]
        desc = desc.strip()
        desc = top_lvl_assy + ' ' + str(desc) + '.xls'
    except:
        desc = 'AGR' + str(proj[4:]) + '-' + str(ijn) + ' Assembly.xls'
    return desc


def jobcard(proj, assy, ijn):

    assy_head = load.assy_head(proj, assy)
    proj_head = load.proj_head(ijn)
    coop_data = load.coop_bom_directly(proj)
    cost_data = load.cost()

    for index, row in assy_head.iterrows():
        check.bom_for_duplication(coop_data, assy=row.partcode)

    filename = get_filename(coop_data, proj, assy, ijn)

    excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = False
    try:
        wb = excel.Workbooks.Open(TEMPLATE)
        wb = write.assy_tabs(wb, assy_head.tab_name.values)
        wb = write.proj_head(wb, proj_head)
        wb = write.assy_name(wb, coop_data, assy)
        wb = write.assy_head(wb, assy_head)
        wb = write.assy_part(wb, proj, assy, assy_head, cost_data)
    finally:
        wb.SaveAs(os.path.join(OUTPUT, filename))
        excel.Application.Quit()

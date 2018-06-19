"""
The main module. create.jobcard() combines all the decoupled function
found in load, check and write modules.
"""
import win32com.client
import os

from . import load
from . import check
from . import write


TEMPLATE = r'C:\Users\GARY\Documents\templates\jobcard.xls'
OUTPUT = r'C:\Users\GARY\Desktop'


def get_filename(raw, proj, assy, ijn):
    """return jobcard filename"""
    try:
        desc = raw[raw.partcode == assy].desc.values[0]
        desc = desc.strip()
        desc = assy + ' ' + str(desc) + '.xlsx'
    except:
        desc = 'AGR' + str(proj[4:]) + '-' + str(ijn) + ' Assembly.xlsx'
    return desc


def jobcards(proj, assy, ijn):
    """
    create manufacture jobcard with everything defined based on the
    user input

    Parameters
    ----------
    proj : str
        AGR project number (eg. 'AGR-1288')
    assy: str
        Top level assembly (eg. 'AGR1288-010-00')
    ijn : int
        Internal job number (eg. '44080')
    """
    proj_head = load.proj_head(ijn)
    assy_head = load.assy_head(proj, assy, proj_head)
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
        wb, df = write.assy_part(wb, proj, assy, assy_head, cost_data, proj_head)
    finally:
        wb.SaveAs(os.path.join(OUTPUT, filename), FileFormat=51)
        excel.Application.Quit()
        write.consolidated_bom(
            filename=os.path.join(OUTPUT, 'consolidated ' + filename),
            proj=proj,
            top_lvl_assy=assy,
            assy_head_data=assy_head,
            proj_head_dict=proj_head,
            cost_data=cost_data
        )
        # df.to_excel(os.path.join(OUTPUT, 'consolidated ' + filename + 'x'), sheet_name='raw', index=False)
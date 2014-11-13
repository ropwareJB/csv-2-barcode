# Barcode Generator Tool
# Josh Brown, 2014 EPIDEV
#
# Python 3.4 

from fpdf import FPDF
import csv
INPUT_FILE = "data.csv"


class product:
    def __init__(self):
        pass


columns = False
rows = []
with open(INPUT_FILE, 'rU') as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    for row in reader:
        if columns == False: 
            columns = row
            continue
        rows.append(row)

print rows

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial','B',16)
pdf.cell(40,10,'Hello World!')

pdf.image("http://barcode.tec-it.com/barcode.ashx?code=Code128&modulewidth=fit&data=ABC-abc-1234&dpi=96&imagetype=png&rotation=0&color=&bgcolor=&fontcolor=&quiet=0&qunit=mm", x=0, y=0, type='png', link='')
pdf.output('tuto1.pdf','F')

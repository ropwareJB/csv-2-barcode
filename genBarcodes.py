# Barcode Generator Tool
# Josh Brown, 2014 EPIDEV
#
# Python 2.7 

from fpdf import FPDF
import csv
INPUT_FILE = "data.csv"


class product:
    def __init__(self):
        self.



with open(INPUT_FILE, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

#pdf = FPDF()
#pdf.add_page()
#pdf.set_font('Arial','B',16)
#pdf.cell(40,10,'Hello World!')
#pdf.output('tuto1.pdf','F')

#$pdf->Image('http://chart.googleapis.com/chart?cht=p3&chd=t:60,40&chs=250x100&chl=Hello|World',60,30,90,0,'PNG');

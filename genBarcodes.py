# CSV-2-barcode -> Barcode Generator Tool
# Josh Brown, 2014 EPIDEV
#
# Dependencies:
#       - Python 2.7
#       - Python Imaging Library    http://www.pythonware.com/products/pil/
#       - PyPDF                     https://code.google.com/p/pyfpdf/
#

from fpdf import FPDF
import csv
import sys

# Default values - can be overridden using cmd switches
INPUT_FILE = "data.csv"
OUTPUT_FILE = "out.pdf"
FONT = 'Helvetica'

FONT_SRC = ''
FONT_SRC_BOLD = ''

# python genBarcodes.py -o output.pdf -f Helvatica
# python genBarcodes.py -i input.csv --font-src font_reg.ttf --font-bold-src font_bold.ttf
if len(sys.argv) > 1:
    args = sys.argv[1:]
    for x in range(len(args[:-1])):
        if args[x] == '-o':
            OUTPUT_FILE = args[x+1]
        elif args[x] == '-i':
            INPUT_FILE = args[x+1]
        elif args[x] == '-f' :
            FONT = args[x+1]
        elif args[x] == '--font-src':
            FONT_SRC = args[x+1]
        elif args[x] == '--font-bold-src':
            FONT_SRC_BOLD = args[x+1]

if FONT_SRC != '' and FONT_SRC_BOLD == '': FONT_SRC_BOLD = FONT_SRC

# Font sizes for the respective data segments
COLLECTION_SIZE = 38
SKU_SIZE = 38
PRODUCT_SIZE = 18
BARCODE_SIZE = 8
SUBTXT_SIZE = 8
REG_SIZE = 17

# X,Y posiitons of the origin and barcode
# The base padding applied to all elements
# Barcode dimensions, (x, y) position relative to BASE
# Further padding for text items
BASE_Y=3
BASE_X=3
BARCODE_X=BASE_X+15
BARCODE_Y=BASE_Y
BARCODE_H=3
PADDING_X = 0
PADDING_Y = 0

# y-levels for the inline-text segments
y_1= BASE_Y+1.5
y_2= y_1+2
y_3= y_2+1.25
y_4= y_3+2.5
y_5= y_4+0.85
y_6= y_5+1.2
y_7= y_6+0.85

# x-levels for the inline-text segments
x_1=0
x_2=11
x_3=18

# Product Model Class
# Just a simple wrapper for each product for superior code readability
# Doesn't do any function other than extraction from the CSV array
class Product:
    def __init__(self, data):
        self.sku = data[0]
        self.collection = data[1]
        self.product = data[2]
        self.colour = data[3]
        self.length = data[4]
        self.width = data[5]
        self.height = data[6]
        self.weight = data[7]
        self.parcelNo = data[8]
        self.parcelPcs = data[9]
        self.poNo = data[10]
        self.destination = data[11]
        self.origin = data[12]

# Extraction of all the data and paring it into
#                       a list of Product instances.
columns = False
rows = []
with open(INPUT_FILE, 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        if columns == False: 
            columns = row
            continue
        rows.append(Product(row))

# Begin the PDF production, Letter page
pdf = FPDF('L', unit='cm', format='Letter')
pdf.set_margins(PADDING_X, PADDING_Y)

# Set the fonts that we would like to use, and override the Bold
# option for the font.
if FONT_SRC != '' and FONT_SRC_BOLD != '':
    pdf.add_font(FONT, '', fname=FONT_SRC, uni=True)
    pdf.add_font(FONT, 'B', fname=FONT_SRC_BOLD, uni=True)

# For each product, add a page and on that page, 
# scrape a bracode from barcode.tec-it.com and insert it,
# then write the Collection, SKU and other product details
n=0
maxN = len(rows)
for cProduct in rows:
    n=n+1
    pdf.add_page()
    img = "http://barcode.tec-it.com/barcode.ashx?code=Code128&modulewidth=fit&data="+cProduct.sku+"&dpi=96&imagetype=png&rotation=0&color=&bgcolor=&fontcolor=&quiet=0&qunit=mm"
    pdf.image(img, x=BARCODE_X, y=BARCODE_Y, type='png', link='', h=BARCODE_H)
    pdf.set_font(FONT,'', COLLECTION_SIZE)
    pdf.set_fill_color(255)
    pdf.set_xy(BARCODE_X, BARCODE_Y+BARCODE_H-1*BARCODE_H/3.0) 
    pdf.cell(0, 2, fill=1)

    pdf.set_font(FONT,'B', COLLECTION_SIZE)
    pdf.text(BASE_X, y_1, cProduct.collection.upper());

    pdf.set_font(FONT,'', SKU_SIZE)
    pdf.text(BASE_X, y_2, cProduct.sku);

    pdf.set_font(FONT,'', PRODUCT_SIZE)
    pdf.text(BASE_X, y_3, "%s, %s" % (cProduct.product, cProduct.colour));

    pdf.set_font(FONT,'', BARCODE_SIZE)
    pdf.text(BARCODE_X+0.85*BARCODE_H, BARCODE_Y+BARCODE_H-0.4, cProduct.sku);

    pdf.set_font(FONT,'', SUBTXT_SIZE)
    pdf.text(BASE_X+x_1, y_4, "PARCEL DIMENSIONS");
    txt="PARCEL NO."
    tw = pdf.get_string_width(txt)
    pdf.text(BASE_X+x_2-tw/2, y_4, txt);
    pdf.text(BASE_X+x_3, y_4, "PO NO.");
    pdf.set_font(FONT, 'U', REG_SIZE)
    pdf.text(BASE_X+x_1, y_5, "%sL x %sW x %sH cm" % (cProduct.length, cProduct.width, cProduct.height));
    txt=cProduct.parcelNo
    tw = pdf.get_string_width(txt)
    pdf.text(BASE_X+x_2-tw/2, y_5, txt);
    pdf.text(BASE_X+x_3, y_5, cProduct.poNo);

    pdf.set_font(FONT,'', SUBTXT_SIZE)
    pdf.text(BASE_X+x_1, y_6, "G.W.");
    txt="PCS/PARCEL"
    tw = pdf.get_string_width(txt)
    pdf.text(BASE_X+x_2-tw/2, y_6, txt);
    pdf.text(BASE_X+x_3, y_6, "DESTINATION");
    pdf.set_font(FONT, 'U', REG_SIZE)
    pdf.text(BASE_X+x_1, y_7, "%s kg"%cProduct.weight);
    txt=cProduct.parcelPcs
    tw = pdf.get_string_width(txt)
    pdf.text(BASE_X+x_2-tw/2, y_7, txt);
    pdf.text(BASE_X+x_3, y_7, cProduct.destination);

    pdf.set_font(FONT,'', SUBTXT_SIZE)
    pdf.text(BASE_X+x_3+2.2, y_7+0.65, cProduct.origin);
    print "[ %3d / %-3d  ] %3.2f%%" % (n, maxN, n/float(maxN)*100)
pdf.output(OUTPUT_FILE, 'F')
print "Complete.\n"

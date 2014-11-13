# Barcode Generator Tool
# Josh Brown, 2014 EPIDEV
#
# Python 3.4 

from fpdf import FPDF
import csv
INPUT_FILE = "data.csv"
FONT = 'Helvetica'
COLLECTION_SIZE = 38
SKU_SIZE = 38
PRODUCT_SIZE = 18
BARCODE_SIZE = 8

SUBTXT_SIZE = 8
REG_SIZE = 17



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

columns = False
rows = []
with open(INPUT_FILE, 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        if columns == False: 
            columns = row
            continue
        rows.append(Product(row))

BASE_Y=3
BASE_X=3

BARCODE_X=BASE_X+15
BARCODE_Y=BASE_Y
BARCODE_H=3

PADDING_X = 0
PADDING_Y = 0

y_1= BASE_Y+1.5
y_2= y_1+2
y_3= y_2+1.25
y_4= y_3+2.5
y_5= y_4+0.85
y_6= y_5+1.2
y_7= y_6+0.85

x_1=0
x_2=11
x_3=18

cProduct = rows[0]

pdf = FPDF('L', unit='cm')
pdf.set_margins(PADDING_X, PADDING_Y)

for cProduct in rows:
    pdf.add_page()
#pdf.add_font('DejaVu', '', fname='reqs/Brandon_thin.otf')
#pdf.add_font('Brandon Grotesque', '', fname='Brandon_reg.otf')
    img = "http://barcode.tec-it.com/barcode.ashx?code=Code128&modulewidth=fit&data="+cProduct.sku+"&dpi=96&imagetype=png&rotation=0&color=&bgcolor=&fontcolor=&quiet=0&qunit=mm"

    pdf.image(img, x=BARCODE_X, y=BARCODE_Y, type='png', link='', h=BARCODE_H)
    pdf.set_font(FONT,'', COLLECTION_SIZE)
    pdf.set_fill_color(255)
    pdf.set_xy(BARCODE_X, BARCODE_Y+BARCODE_H-1*BARCODE_H/3.0) 
    pdf.cell(0, 2, fill=1)

    pdf.set_font(FONT,'B', COLLECTION_SIZE)
    pdf.text(BASE_X, y_1, cProduct.collection);

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
    pdf.set_font(FONT,'U', REG_SIZE)
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
    pdf.set_font(FONT,'U', REG_SIZE)
    pdf.text(BASE_X+x_1, y_7, "%s kg"%cProduct.weight);
    txt=cProduct.parcelPcs
    tw = pdf.get_string_width(txt)
    pdf.text(BASE_X+x_2-tw/2, y_7, txt);
    pdf.text(BASE_X+x_3, y_7, cProduct.destination);

    pdf.set_font(FONT,'', SUBTXT_SIZE)
    pdf.text(BASE_X+x_3+2.2, y_7+0.65, cProduct.origin);

pdf.output('out.pdf','F')

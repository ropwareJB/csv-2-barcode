# CSV-2-barcode 
A Python Barcode Generator

Generates a PDF with a series of barcode tags 

## Disclaimer
This software uses TEC-IT's barcode generator (http://barcode.tec-it.com/)
You must purchase a license to use this software, or modify this software such
that it does not use TEC-IT's tool.

## Dependencies
1. Python2.7

2. Python Imaging Library - http://www.pythonware.com/products/pil/
> pip install PIL --allow-external PIL --allow-unverified PI

3. PyPDF                  - https://github.com/reingart/pyfpdf

## Usage
```
python genBarcodes.py -i input.csv -o barcodes.pdf
python genBarcodes.py -i input.csv -o barcodes.pdf -f Ariel
python genBarcodes.py --font-src font_reg.ttf
```


<?php
  // CSV-2-barcode -> Barcode Generator Tool
  // Josh Brown, 2014 EPIDEV
  //
  // Dependencies:
  //       - fPDF    https://http://f$pdf->org/
  //

require('fpdf-php/fpdf.php');

# Default values - can be overridden using cmd switches
$INPUT_FILE = "data.csv";
$OUTPUT_FILE = "out.pdf";
$FONT = 'Helvetica';

$FONT_SRC = '';
$FONT_SRC_BOLD = '';

# php genBarcodes.php -o output.pdf
# php genBarcodes.php -i input.csv --font-src font_reg.ttf --font-bold-src font_bold.ttf
if(isset($_GET['font'])) $FONT_SRC = $_GET['font'];
if(isset($_GET['font-bold'])) $FONT_SRC_BOLD = $_GET['font-bold'];
if(isset($_GET['input-file'])) $INPUT_FILE = $_GET['input-file'];
if(isset($_GET['output-file'])) $OUTPUT_FILE = $_GET['output-file'];
if($FONT_SRC != '' && $FONT_SRC_BOLD == '') $FONT_SRC_BOLD = $FONT_SRC;

# Font sizes for the respective data segments
$COLLECTION_SIZE = 38;
$SKU_SIZE = 38;
$PRODUCT_SIZE = 18;
$BARCODE_SIZE = 8;
$SUBTXT_SIZE = 8;
$REG_SIZE = 17;

# X,Y posiitons of the origin and barcode
# The base padding applied to all elements
# Barcode dimensions, (x, y) position relative to BASE
# Further padding for text items
$BASE_Y=3;
$BASE_X=3;
$BARCODE_X=$BASE_X+15;
$BARCODE_Y=$BASE_Y;
$BARCODE_H=3;
$PADDING_X = 0;
$PADDING_Y = 0;

# y-levels for the inline-text segments
$y_1= $BASE_Y+1.5;
$y_2= $y_1+2;
$y_3= $y_2+1.25;
$y_4= $y_3+2.5;
$y_5= $y_4+0.85;
$y_6= $y_5+1.2;
$y_7= $y_6+0.85;

# x-levels for the inline-text segments

$x_1=0;
$x_2=11;
$x_3=18;

# Product Model Class
# Just a simple wrapper for each product for superior code readability
# Doesn't do any function other than extraction from the CSV array
class Product{
    public $sku;
    public $collection;
    public $product;
    public $colour;
    public $length;
    public $width;
    public $height;
    public $weight;
    public $parcelNo;
    public $parcelPcs;
    public $poNo;
    public $destination;
    public $origin;
    function Product($data){
        $this->sku = $data[0];
        $this->collection = $data[1];
        $this->product = $data[2];
        $this->colour = $data[3];
        $this->length = $data[4];
        $this->width = $data[5];
        $this->height = $data[6];
        $this->weight = $data[7];
        $this->parcelNo = $data[8];
        $this->parcelPcs = $data[9];
        $this->poNo = $data[10];
        $this->destination = $data[11];
        $this->origin = $data[12];
    }
}

# Extraction of all the data and paring it into
#                       a list of Product instances.
$columns = False;
$rows = array();

$input = file_get_contents($INPUT_FILE);
$rows = str_getcsv($input, "\r"); //parse the rows 
foreach($rows as &$row) $row = new Product(str_getcsv($row, ",")); //parse the items in rows 
array_shift($rows);

# Begin the PDF production, Letter page
$pdf = new FPDF('L', 'cm', 'A4');
$pdf->SetMargins($PADDING_X, $PADDING_Y);

# Set the fonts that we would like to use, and override the Bold
# option for the font.
if($FONT_SRC != '' && $FONT_SRC_BOLD != ''){
    $pdf->AddFont($FONT, '', $FONT_SRC);
    $pdf->AddFont($FONT, 'B', $FONT_SRC_BOLD);
}

# For each product, add a page and on that page, 
# scrape a bracode from barcode.tec-it.com and insert it,
# then write the Collection, SKU and other product details
$n=0;
$maxN = count($rows);
foreach($rows as $cProduct){
    $n++;
    $pdf->AddPage();
    $imgURL = "http://barcode.tec-it.com/barcode.ashx?code=Code128&modulewidth=fit&data=".$cProduct->sku."&dpi=96&imagetype=png&rotation=0&color=&bgcolor=&fontcolor=&quiet=0&qunit=mm";
    $pdf->Image($imgURL, $BARCODE_X, $BARCODE_Y, 0, $BARCODE_H, 'png');
    $pdf->SetFont($FONT,'', $COLLECTION_SIZE);
    $pdf->SetFillColor(255);
    $pdf->SetXY($BARCODE_X, $BARCODE_Y+$BARCODE_H-1*$BARCODE_H/3.0);
    $pdf->Cell(0, 2, '', 0, 0, 'L', 1);

    $pdf->SetFont($FONT,'B', $COLLECTION_SIZE);
    $pdf->Text($BASE_X, $y_1, strtoupper($cProduct->collection));

    $pdf->SetFont($FONT,'', $SKU_SIZE);
    $pdf->Text($BASE_X, $y_2, $cProduct->sku);

    $pdf->SetFont($FONT,'', $PRODUCT_SIZE);
    $pdf->Text($BASE_X, $y_3, sprintf("%s, %s", $cProduct->product, $cProduct->colour));

    $pdf->SetFont($FONT,'', $BARCODE_SIZE);
    $pdf->Text($BARCODE_X+0.85*$BARCODE_H, $BARCODE_Y+$BARCODE_H-0.4, $cProduct->sku);

    $pdf->SetFont($FONT,'', $SUBTXT_SIZE);
    $pdf->Text($BASE_X+$x_1, $y_4, "PARCEL DIMENSIONS");

    $txt="PARCEL NO.";
    $tw = $pdf->GetStringWidth($txt);
    $pdf->Text($BASE_X+$x_2-$tw/2, $y_4, $txt);
    $pdf->Text($BASE_X+$x_3, $y_4, "PO NO.");
    $pdf->SetFont($FONT, 'U', $REG_SIZE);
    $pdf->Text($BASE_X+$x_1, $y_5, sprintf("%s L x %s W x %s H cm", $cProduct->length, $cProduct->width, $cProduct->height));
    $txt=$cProduct->parcelNo;
    $tw = $pdf->GetStringWidth($txt);
    $pdf->Text($BASE_X+$x_2-$tw/2, $y_5, $txt);
    $pdf->Text($BASE_X+$x_3, $y_5, $cProduct->poNo);

    $pdf->SetFont($FONT,'', $SUBTXT_SIZE);
    $pdf->Text($BASE_X+$x_1, $y_6, "G.W.");
    $txt="PCS/PARCEL";
    $tw = $pdf->GetStringWidth($txt);
    $pdf->Text($BASE_X+$x_2-$tw/2, $y_6, $txt);
    $pdf->Text($BASE_X+$x_3, $y_6, "DESTINATION");
    $pdf->SetFont($FONT, 'U', $REG_SIZE);
    $pdf->Text($BASE_X+$x_1, $y_7, sprintf("%s kg", $cProduct->weight));
    $txt= $cProduct->parcelPcs;
    $tw = $pdf->GetStringWidth($txt);
    $pdf->Text($BASE_X+$x_2-$tw/2, $y_7, $txt);
    $txt = $cProduct->destination;
    $pdf->Text($BASE_X+$x_3, $y_7, $txt);

    $tw = $pdf->GetStringWidth($txt);

    $pdf->SetFont($FONT, '', $SUBTXT_SIZE);
    $txt= $cProduct->origin;
    $twx = $pdf->GetStringWidth($txt);
    $pdf->Text($BASE_X+$x_3+$tw-$twx, $y_7+0.65, $txt);
    printf("[ %3d / %-3d  ] %3.2f%%", $n, $maxN, $n/(float)$maxN*100);
}

$pdf->output($OUTPUT_FILE, 'F');
print("Complete.\n");

?>

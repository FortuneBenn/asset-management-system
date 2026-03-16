import os
from barcode import Code128
from barcode.writer import ImageWriter
from django.conf import settings

def generate_barcode(asset):
    """
    Generates a barcode image for a given asset.
    """
    barcode_path = os.path.join(settings.MEDIA_ROOT, 'barcodes', f'{asset.university_barcode}.png')
    os.makedirs(os.path.dirname(barcode_path), exist_ok=True)

    Code128(asset.university_barcode, writer=ImageWriter()).save(barcode_path)
    return barcode_path

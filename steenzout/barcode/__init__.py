# -*- coding: utf-8 -*-
"""This package provides a simple way to create standard bar codes.

It needs no external packages to be installed,
the bar codes are created as SVG objects.

If PIL (Python Imaging Library) is installed,
the bar codes can also be rendered as images
(all formats supported by PIL).
"""


from .errors import BarcodeNotFoundError
from .codex import Code39, PZN, Code128
from .ean import EAN8, EAN13, JAN
from .isxn import ISBN10, ISBN13, ISSN
from .upc import UPCA
from .version import __version__

try:
    _strbase = basestring  # lint:ok
except NameError:
    _strbase = str


__BARCODE_MAP = dict(
    ean8=EAN8,
    ean13=EAN13,
    ean=EAN13,
    gtin=EAN13,
    jan=JAN,
    upc=UPCA,
    upca=UPCA,
    isbn=ISBN13,
    isbn13=ISBN13,
    gs1=ISBN13,
    isbn10=ISBN10,
    issn=ISSN,
    code39=Code39,
    pzn=PZN,
    code128=Code128,
)

PROVIDED_BARCODES = list(__BARCODE_MAP.keys())
PROVIDED_BARCODES.sort()


def get(name, code=None, writer=None):
    try:
        barcode = __BARCODE_MAP[name.lower()]
    except KeyError:
        raise BarcodeNotFoundError('The barcode {0!r} you requested is not '
                                   'known.'.format(name))
    if code is not None:
        return barcode(code, writer)
    else:
        return barcode


def get_class(name):
    return get_barcode(name)


def generate(name, code, writer=None, output=None, writer_options=None):
    options = writer_options or {}
    barcode = get_barcode(name, code, writer)
    if isinstance(output, _strbase):
        fullname = barcode.save(output, options)
        return fullname
    else:
        barcode.write(output, options)


get_barcode = get
get_barcode_class = get_class
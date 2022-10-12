import os
from copy import copy
from typing import Optional

from openpyxl.styles import Alignment
from openpyxl.styles import Border
from openpyxl.styles import Font
from openpyxl.styles import Side

BASE_FONT = Font(
    name="Times New Roman",
    size=12,
)

BOLD_FONT = copy(BASE_FONT)
BOLD_FONT.bold = True

ALIGNMENT_CENTER = Alignment(
    horizontal="center",
    vertical="center",
)

ALIGNMENT_LEFT = copy(ALIGNMENT_CENTER)
ALIGNMENT_LEFT.horizontal = "left"

ALIGNMENT_RIGHT = copy(ALIGNMENT_CENTER)
ALIGNMENT_RIGHT.horizontal = "right"


def get_module_path(module):
    return os.path.abspath(os.path.dirname(module))


def set_cell(
    cell, value, number_format=None, font=None, alignment=None, wrap_text: Optional[bool] = True, allow_null=False
):
    if value is not None and (value != 0 or allow_null):
        cell.value = value

        if number_format is not None:
            cell.number_format = number_format

    if font is not None:
        cell.font = font

    if alignment is not None:
        alignment.wrap_text = wrap_text
        cell.alignment = alignment


def set_border(ws, cell_range):
    border = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000"),
    )

    rows = ws[cell_range]
    for row in rows:
        for cell in row:
            cell.border = border

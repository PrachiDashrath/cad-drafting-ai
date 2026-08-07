"""
layout_engine.py

Automatically positions projected views on the drawing sheet.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.drawing.drawing_sheet import DrawingSheet


@dataclass(slots=True)
class ViewLayout:

    x: int
    y: int
    width: int
    height: int


class LayoutEngine:

    def generate(
        self,
        sheet: DrawingSheet,
        width: int,
        height: int,
    ) -> dict:

        margin = 25

        title_block = 90

        usable_height = height - title_block - 2 * margin

        usable_width = width - 2 * margin

        half_w = usable_width // 2
        half_h = usable_height // 2

        return {

            "top": ViewLayout(
                margin,
                margin,
                half_w,
                half_h,
            ),

            "front": ViewLayout(
                margin,
                margin + half_h,
                half_w,
                half_h,
            ),

            "right": ViewLayout(
                margin + half_w,
                margin + half_h,
                half_w,
                half_h,
            ),

            "isometric": ViewLayout(
                margin + half_w,
                margin,
                half_w,
                half_h,
            ),
        }
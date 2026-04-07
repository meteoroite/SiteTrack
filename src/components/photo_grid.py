"""
Photo grid component - displays photos in a grid layout
"""

import flet as ft
import os

class PhotoGrid:
    """UI component displaying photos in grid layout"""
    
    @staticmethod
    def build(photos, on_photo_click=None, on_delete=None):
        """Build photo grid"""
        if not photos:
            return ft.Container(
                content=ft.Text(
                    "No photos added yet",
                    color=ft.colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=20,
            )
        
        photo_items = []
        for idx, photo_path in enumerate(photos):
            if os.path.exists(photo_path):
                photo_item = ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src=photo_path,
                                width=150,
                                height=150,
                                fit=ft.ImageFit.COVER,
                                border_radius=8,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        "zoom_in",
                                        icon_size=20,
                                        on_click=lambda e, p=photo_path: PhotoGrid._view_photo(p) if on_photo_click else None,
                                    ),
                                    ft.IconButton(
                                        "delete",
                                        icon_size=20,
                                        on_click=lambda e, idx=idx: on_delete(idx) if on_delete else None,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=8,
                )
                photo_items.append(photo_item)
        
        return ft.GridView(
            controls=photo_items,
            runs_count=2,
            spacing=10,
            run_spacing=10,
            child_aspect_ratio=1,
        )
    
    @staticmethod
    def _view_photo(photo_path):
        """View individual photo"""
        print(f"Viewing photo: {photo_path}")

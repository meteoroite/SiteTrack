"""
SiteTrack - Main Entry Point
A mobile-first app for engineers and inspectors to create professional reports on-site
"""

import flet as ft
from src.main_app import FieldReportApp

def main(page: ft.Page):
    app = FieldReportApp()
    app.setup_routes(page)

if __name__ == "__main__":
    ft.app(target=main)

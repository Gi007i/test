#!/usr/bin/env python3
"""
Moderner Taschenrechner mit Flet GUI Framework.
Unterstützt Tastatur- und Mauseingaben auf ARM64 Windows 11.
"""

import flet as ft
import operator
from typing import Optional


class Calculator:
    """Hauptklasse für den Flet-Taschenrechner."""

    def __init__(self):
        """Initialisiere den Taschenrechner."""
        self.display_value = "0"
        self.current_number = ""
        self.previous_number = ""
        self.operation = None
        self.reset_display = False

        # Operatoren-Mapping
        self.operations = {
            "+": operator.add,
            "−": operator.sub,  # Minus-Zeichen
            "×": operator.mul,  # Mal-Zeichen
            "÷": operator.truediv  # Geteilt-Zeichen
        }

    def main(self, page: ft.Page):
        """Hauptfunktion für die Flet-App."""
        page.title = "Moderner Taschenrechner"
        page.window_width = 320
        page.window_height = 480
        page.window_resizable = False
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.bgcolor = ft.Colors.GREY_100

        # Display für Berechnungen
        self.display = ft.Text(
            value=self.display_value,
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
            color=ft.Colors.BLACK,
            width=280,
            height=60
        )

        # Display-Container
        display_container = ft.Container(
            content=self.display,
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.all(10)
        )

        # Button-Definitionen
        buttons = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        # Button-Rows erstellen
        button_rows = []
        for row in buttons:
            button_row = []
            for button_text in row:
                if button_text == "0":
                    # Zero-Button nimmt zwei Spalten ein
                    btn = ft.ElevatedButton(
                        text=button_text,
                        width=140,
                        height=60,
                        on_click=lambda e, text=button_text: self.on_button_click(e, text),
                        style=self.get_button_style(button_text)
                    )
                elif button_text == "=":
                    # Equals-Button nimmt zwei Spalten ein
                    btn = ft.ElevatedButton(
                        text=button_text,
                        width=140,
                        height=60,
                        on_click=lambda e, text=button_text: self.on_button_click(e, text),
                        style=self.get_button_style(button_text)
                    )
                else:
                    btn = ft.ElevatedButton(
                        text=button_text,
                        width=60,
                        height=60,
                        on_click=lambda e, text=button_text: self.on_button_click(e, text),
                        style=self.get_button_style(button_text)
                    )
                button_row.append(btn)
            button_rows.append(ft.Row(button_row, spacing=10, alignment=ft.MainAxisAlignment.CENTER))

        # Haupt-Layout
        page.add(
            ft.Column([
                display_container,
                ft.Container(
                    content=ft.Column(button_rows, spacing=10),
                    padding=ft.padding.all(10)
                )
            ], spacing=0, alignment=ft.MainAxisAlignment.START)
        )

        # Tastatur-Event-Handler
        page.on_keyboard_event = self.on_keyboard
        page.update()

    def get_button_style(self, text: str) -> ft.ButtonStyle:
        """Gibt den Button-Style basierend auf dem Button-Text zurück."""
        if text in ["÷", "×", "−", "+", "="]:
            # Operator-Buttons
            return ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.ORANGE,
                shape=ft.RoundedRectangleBorder(radius=15)
            )
        elif text in ["C", "±", "%"]:
            # Funktion-Buttons
            return ft.ButtonStyle(
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.GREY_300,
                shape=ft.RoundedRectangleBorder(radius=15)
            )
        else:
            # Zahlen-Buttons
            return ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREY_700,
                shape=ft.RoundedRectangleBorder(radius=15)
            )

    def on_button_click(self, e, text: str):
        """Behandelt Button-Klicks."""
        self.handle_input(text)

    def on_keyboard(self, e: ft.KeyboardEvent):
        """Behandelt Tastatureingaben."""
        if e.key == "Escape":
            self.handle_input("C")
        elif e.key == "Enter":
            self.handle_input("=")
        elif e.key == "Backspace":
            self.handle_backspace()
        elif e.key in "0123456789":
            self.handle_input(e.key)
        elif e.key == ".":
            self.handle_input(".")
        elif e.key == "+":
            self.handle_input("+")
        elif e.key == "-":
            self.handle_input("−")
        elif e.key == "*":
            self.handle_input("×")
        elif e.key == "/":
            self.handle_input("÷")

    def handle_input(self, value: str):
        """Behandelt Eingaben von Buttons und Tastatur."""
        if value in "0123456789":
            self.handle_number(value)
        elif value == ".":
            self.handle_decimal()
        elif value in self.operations:
            self.handle_operation(value)
        elif value == "=":
            self.handle_equals()
        elif value == "C":
            self.handle_clear()
        elif value == "±":
            self.handle_plus_minus()
        elif value == "%":
            self.handle_percent()

        self.update_display()

    def handle_number(self, number: str):
        """Behandelt Zahleneingaben."""
        if self.reset_display:
            self.display_value = number
            self.reset_display = False
        else:
            if self.display_value == "0":
                self.display_value = number
            else:
                self.display_value += number

    def handle_decimal(self):
        """Behandelt Dezimalpunkt-Eingabe."""
        if self.reset_display:
            self.display_value = "0."
            self.reset_display = False
        elif "." not in self.display_value:
            self.display_value += "."

    def handle_operation(self, op: str):
        """Behandelt Operator-Eingaben."""
        if self.operation and not self.reset_display:
            self.handle_equals()

        self.previous_number = self.display_value
        self.operation = op
        self.reset_display = True

    def handle_equals(self):
        """Behandelt Gleichheits-Operation."""
        if self.operation and self.previous_number:
            try:
                current = float(self.display_value)
                previous = float(self.previous_number)

                if self.operation == "÷" and current == 0:
                    self.display_value = "Fehler"
                else:
                    result = self.operations[self.operation](previous, current)
                    # Formatiere Ergebnis
                    if result.is_integer():
                        self.display_value = str(int(result))
                    else:
                        self.display_value = f"{result:.10g}"  # Entferne unnötige Nullen

                self.operation = None
                self.previous_number = ""
                self.reset_display = True

            except (ValueError, ZeroDivisionError, OverflowError):
                self.display_value = "Fehler"
                self.reset_display = True

    def handle_clear(self):
        """Behandelt Clear-Operation."""
        self.display_value = "0"
        self.current_number = ""
        self.previous_number = ""
        self.operation = None
        self.reset_display = False

    def handle_plus_minus(self):
        """Behandelt Vorzeichenwechsel."""
        if self.display_value != "0" and not self.display_value.startswith("Fehler"):
            if self.display_value.startswith("-"):
                self.display_value = self.display_value[1:]
            else:
                self.display_value = "-" + self.display_value

    def handle_percent(self):
        """Behandelt Prozent-Operation."""
        try:
            value = float(self.display_value)
            result = value / 100
            if result.is_integer():
                self.display_value = str(int(result))
            else:
                self.display_value = f"{result:.10g}"
            self.reset_display = True
        except ValueError:
            self.display_value = "Fehler"
            self.reset_display = True

    def handle_backspace(self):
        """Behandelt Backspace-Taste."""
        if len(self.display_value) > 1 and not self.display_value.startswith("Fehler"):
            self.display_value = self.display_value[:-1]
        else:
            self.display_value = "0"
        self.update_display()

    def update_display(self):
        """Aktualisiert das Display."""
        # Begrenze Display-Länge
        if len(self.display_value) > 12:
            try:
                # Versuche wissenschaftliche Notation
                value = float(self.display_value)
                self.display_value = f"{value:.5e}"
            except ValueError:
                self.display_value = self.display_value[:12]

        self.display.value = self.display_value
        self.display.update()


def main():
    """Startet die Taschenrechner-App."""
    calculator = Calculator()
    ft.app(target=calculator.main)


if __name__ == "__main__":
    main()
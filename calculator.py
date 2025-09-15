#!/usr/bin/env python3
"""
Moderner Taschenrechner mit CustomTkinter GUI Framework.
Unterstützt Tastatur- und Mauseingaben auf ARM64 Windows 11.
"""

import customtkinter as ctk
import operator
from typing import Optional


class Calculator:
    """Hauptklasse für den CustomTkinter-Taschenrechner."""

    def __init__(self):
        """Initialisiere den Taschenrechner."""
        self.display_value = "0"
        self.current_number = "0"
        self.previous_number = ""
        self.operation = None
        self.reset_display = False
        self.show_operation = False  # Zeige Eingabe im Display
        self.calculation_history = ""  # Vollständiger Berechnungsstring

        # Operatoren-Mapping
        self.operations = {
            "+": operator.add,
            "−": operator.sub,  # Minus-Zeichen
            "×": operator.mul,  # Mal-Zeichen
            "÷": operator.truediv  # Geteilt-Zeichen
        }

        self.setup_gui()

    def setup_gui(self):
        """Erstellt die GUI-Komponenten."""
        # Hauptfenster
        self.root = ctk.CTk()
        self.root.title("Moderner Taschenrechner")
        self.root.geometry("260x340")
        self.root.resizable(False, False)

        # Helles Theme setzen
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Display für Berechnungen
        self.display_frame = ctk.CTkFrame(self.root, width=240, height=60, corner_radius=10)
        self.display_frame.pack(pady=10, padx=10)
        self.display_frame.pack_propagate(False)

        self.display_label = ctk.CTkLabel(
            self.display_frame,
            text=self.display_value,
            font=("Arial", 24, "normal"),
            text_color="black",
            anchor="e"
        )
        self.display_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Button-Frame
        self.button_frame = ctk.CTkFrame(self.root, width=240, height=250)
        self.button_frame.pack(pady=5, padx=10, fill="both", expand=True)
        self.button_frame.pack_propagate(False)

        # Buttons manuell erstellen für präzise Kontrolle
        button_data = [
            # Row 0
            [("C", 0, 0), ("±", 0, 1), ("%", 0, 2), ("÷", 0, 3)],
            # Row 1
            [("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3)],
            # Row 2
            [("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("−", 2, 3)],
            # Row 3
            [("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3)],
            # Row 4 - spezielle Behandlung
            [(".", 4, 1), ("=", 4, 2)]
        ]

        # Standard-Buttons erstellen
        for row in button_data:
            for button_text, row_pos, col_pos in row:
                if button_text == "=":
                    # Equals-Button nimmt zwei Spalten ein
                    btn = ctk.CTkButton(
                        self.button_frame,
                        text=button_text,
                        height=40,
                        corner_radius=20,
                        font=("Arial", 18, "bold"),
                        command=lambda text=button_text: self.handle_input(text),
                        **self.get_button_style(button_text)
                    )
                    btn.grid(row=row_pos, column=col_pos, columnspan=2, padx=2, pady=2, sticky="ew")
                else:
                    btn = ctk.CTkButton(
                        self.button_frame,
                        text=button_text,
                        height=40,
                        corner_radius=20,
                        font=("Arial", 18, "bold"),
                        command=lambda text=button_text: self.handle_input(text),
                        **self.get_button_style(button_text)
                    )
                    btn.grid(row=row_pos, column=col_pos, padx=2, pady=2, sticky="ew")

        # Zero-Button separat erstellen (Row 4, Column 0, 2 Spalten breit)
        zero_btn = ctk.CTkButton(
            self.button_frame,
            text="0",
            height=40,
            corner_radius=20,
            font=("Arial", 18, "bold"),
            command=lambda: self.handle_input("0"),
            **self.get_button_style("0")
        )
        zero_btn.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky="ew")

        # Grid-Konfiguration für gleichmäßige Spalten
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Tastatur-Events binden
        self.root.bind("<Key>", self.on_keyboard)
        self.root.focus_set()

    def get_button_style(self, text: str) -> dict:
        """Gibt den Button-Style basierend auf dem Button-Text zurück."""
        if text in ["÷", "×", "−", "+", "="]:
            # Operator-Buttons
            return {
                "fg_color": "#FF9500",
                "text_color": "white",
                "hover_color": "#E6840A"
            }
        elif text in ["C", "±", "%"]:
            # Funktion-Buttons
            return {
                "fg_color": "#D4D4D2",
                "text_color": "black",
                "hover_color": "#BFBFBD"
            }
        else:
            # Zahlen-Buttons
            return {
                "fg_color": "#505050",
                "text_color": "white",
                "hover_color": "#404040"
            }

    def on_keyboard(self, event):
        """Behandelt Tastatureingaben."""
        key = event.keysym

        if key == "Escape":
            self.handle_input("C")
        elif key == "Return":
            self.handle_input("=")
        elif key == "BackSpace":
            self.handle_backspace()
        elif key in "0123456789":
            self.handle_input(key)
        elif key == "period":
            self.handle_input(".")
        elif key == "plus":
            self.handle_input("+")
        elif key == "minus":
            self.handle_input("−")
        elif key == "asterisk":
            self.handle_input("×")
        elif key == "slash":
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
        if self.show_operation:
            # Nach einem Operator: Neue Zahl zur Historie hinzufügen
            self.calculation_history += f" {number}"
            self.current_number = number
            self.show_operation = False
        elif self.reset_display:
            # Nach Equals: Neue Berechnung starten
            self.calculation_history = number
            self.current_number = number
            self.reset_display = False
        elif self.display_value == "0":
            # Erste Eingabe oder nach Clear
            self.current_number = number
            self.calculation_history = number
        else:
            # Erweitere aktuelle Zahl
            self.current_number += number
            # Aktualisiere die letzte Zahl in der Historie
            if self.calculation_history:
                parts = self.calculation_history.split()
                if parts:
                    parts[-1] = self.current_number
                    self.calculation_history = " ".join(parts)
            else:
                self.calculation_history = self.current_number

        # Display zeigt IMMER die komplette Historie
        self.display_value = self.calculation_history

    def handle_decimal(self):
        """Behandelt Dezimalpunkt-Eingabe."""
        if self.reset_display:
            self.current_number = "0."
            self.calculation_history = "0."
            self.reset_display = False
        elif "." not in self.current_number:
            self.current_number += "."
            # Aktualisiere die letzte Zahl in der Historie
            if self.calculation_history:
                parts = self.calculation_history.split()
                if parts:
                    parts[-1] = self.current_number
                    self.calculation_history = " ".join(parts)
            else:
                self.calculation_history = self.current_number

        # Display zeigt IMMER die komplette Historie
        self.display_value = self.calculation_history

    def handle_operation(self, op: str):
        """Behandelt Operator-Eingaben."""
        if not self.calculation_history:
            # Erste Operation: Starte mit aktueller Zahl
            self.calculation_history = f"{self.current_number} {op}"
        else:
            # Weitere Operationen: Hänge einfach an
            self.calculation_history += f" {op}"

        self.operation = op
        self.show_operation = True

        # Display zeigt IMMER die komplette Historie
        self.display_value = self.calculation_history

    def handle_equals(self):
        """Behandelt Gleichheits-Operation."""
        if self.calculation_history:
            try:
                # Parsen und berechnen der gesamten Kette
                parts = self.calculation_history.split()
                if len(parts) < 3:  # Mindestens "Zahl Operator Zahl"
                    return

                # Erste Zahl als Startpunkt
                result = float(parts[0])

                # Durchlaufe alle Operationen in der Reihenfolge
                i = 1
                while i < len(parts) - 1:
                    operator_str = parts[i]
                    next_number = float(parts[i + 1])

                    # Division durch Null prüfen
                    if operator_str == "÷" and next_number == 0:
                        self.display_value = "Fehler"
                        self.calculation_history = ""
                        self.reset_display = True
                        self.show_operation = False
                        return

                    # Operation ausführen
                    result = self.operations[operator_str](result, next_number)
                    i += 2

                # Formatiere Ergebnis
                if result.is_integer():
                    result_str = str(int(result))
                else:
                    result_str = f"{result:.10g}"

                # Zeige vollständige Berechnung mit Ergebnis
                self.display_value = f"{self.calculation_history} = {result_str}"

                # Für nächste Berechnung: Ergebnis als Startwert
                self.calculation_history = result_str
                self.operation = None
                self.previous_number = ""
                self.reset_display = True
                self.show_operation = False

            except (ValueError, ZeroDivisionError, OverflowError):
                self.display_value = "Fehler"
                self.calculation_history = ""
                self.reset_display = True
                self.show_operation = False

    def handle_clear(self):
        """Behandelt Clear-Operation."""
        self.display_value = "0"
        self.current_number = "0"
        self.previous_number = ""
        self.operation = None
        self.reset_display = False
        self.show_operation = False
        self.calculation_history = ""

    def handle_plus_minus(self):
        """Behandelt Vorzeichenwechsel."""
        if self.display_value != "0" and not self.display_value.startswith("Fehler"):
            if self.display_value.startswith("-"):
                self.display_value = self.display_value[1:]
            else:
                self.display_value = "-" + self.display_value
        self.update_display()

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
        # Intelligente Display-Längen-Begrenzung
        if len(self.display_value) > 20:
            # Bei langen Berechnungs-Strings: Zeige die letzten Teile
            if " " in self.display_value:
                parts = self.display_value.split()
                # Zeige so viele Teile von rechts wie möglich
                display_parts = []
                current_length = 0
                for part in reversed(parts):
                    if current_length + len(part) + 1 <= 20:
                        display_parts.insert(0, part)
                        current_length += len(part) + 1
                    else:
                        break
                if len(display_parts) < len(parts):
                    self.display_value = "..." + " ".join(display_parts)
                else:
                    self.display_value = " ".join(display_parts)
            else:
                self.display_value = self.display_value[-20:]

        self.display_label.configure(text=self.display_value)

    def run(self):
        """Startet die GUI-Hauptschleife."""
        self.root.mainloop()


def main():
    """Startet die Taschenrechner-App."""
    calculator = Calculator()
    calculator.run()


if __name__ == "__main__":
    main()
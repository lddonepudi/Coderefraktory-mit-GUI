import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os

class PlotManager:
    def __init__(self, settings_file="settings.json"):
        """Initialisiert den PlotManager und lädt die Einstellungen."""
        self.settings = self.load_settings(settings_file)

    def load_settings(self, file):
        """Lädt Einstellungen aus einer JSON-Datei oder verwendet Standardwerte."""
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Einstellungen nicht gefunden. Standardwerte werden verwendet.")
            return {}

    def load_data(self, file, aggregation="Summe"):
        """Lädt Daten aus CSV, JSON oder Excel und aggregiert die Werte."""
        if not os.path.exists(file):
            raise FileNotFoundError("❌ Datei nicht gefunden!")

        ext = os.path.splitext(file)[-1].lower()

        try:
            if ext == ".csv":
                df = pd.read_csv(file)
            elif ext == ".json":
                df = pd.read_json(file)
            elif ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                raise ValueError("❌ Unterstützte Formate: .csv, .json, .xlsx")

            # Sicherstellen, dass die Datei nicht leer ist
            if df.empty:
                raise ValueError("❌ Die Datei enthält keine Daten!")

            # Erste Spalte als Kategorien, restliche Werte numerisch
            categories = df.columns[1:]
            data = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

            # Aggregation: Summe oder Mittelwert
            if aggregation == "Mittelwert":
                aggregated_data = data.mean()
            else:
                aggregated_data = data.sum()

            return df.iloc[:, 0].values, aggregated_data.values, categories

        except Exception as e:
            raise ValueError(f"❌ Fehler beim Laden der Datei: {e}")

    def plot_bar(self, labels, values, title="Balkendiagramm"):
        """Erstellt ein Balkendiagramm."""
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(labels, values, color=self.settings.get("bar_color", "blue"))
        ax.set_xlabel("Werte")
        ax.set_title(title)
        plt.show()

    def plot_pie(self, labels, values, title="Kreisdiagramm"):
        """Erstellt ein Kreisdiagramm."""
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=self.settings.get("pie_colors", None))
        ax.set_title(title)
        plt.show()

    def plot_stacked_bar(self, labels, values, categories, title="Gestapeltes Balkendiagramm"):
        """Erstellt ein gestapeltes Balkendiagramm."""
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.set_title(title)

        bottoms = np.zeros(len(labels))
        for i, (colname, color) in enumerate(zip(categories, plt.cm.tab10.colors)):
            ax.barh(labels, values[i], left=bottoms, label=colname, color=color)
            bottoms += values[i]

        ax.legend()
        plt.show()

# Beispiel für die Nutzung
if __name__ == "__main__":
    plot_manager = PlotManager()
    try:
        labels, values, categories = plot_manager.load_data("example.csv", "Summe")
        plot_manager.plot_bar(labels, values, "Beispiel Balkendiagramm")
    except Exception as e:
        print(e)

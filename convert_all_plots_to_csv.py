import pandas as pd
import os

# Ordner, in dem sich die Plot-Skripte befinden
plot_folder = os.path.join(os.getcwd(), "PlotCodes")

# Liste aller Python-Skripte in `PlotCodes`
plot_files = [os.path.join(plot_folder, f) for f in os.listdir(plot_folder) if f.endswith(".py")]

def extract_data_from_plot(script_name):
    """Extrahiert Daten aus einem gegebenen `plotX.py`-Skript."""
    data = None
    category_names = None

    # Starte das Skript und extrahiere die Daten
    try:
        namespace = {}
        with open(script_name, "r", encoding="utf-8") as file:
            exec(file.read(), namespace)

        # Überprüfen, ob `results` und `category_names` existieren
        if "results" in namespace and "category_names" in namespace:
            data = namespace["results"]
            category_names = namespace["category_names"]

            if isinstance(data, dict):
                return data, category_names
            else:
                raise ValueError(f"❌ Unerwartetes Datenformat in {script_name}")
        else:
            raise ValueError(f"❌ Daten nicht gefunden in {script_name}")
    except Exception as e:
        print(f"⚠️ Fehler beim Verarbeiten von {script_name}: {e}")
        return None, None

def save_plot_data_to_csv(script_name):
    """Lädt die Daten aus `plotX.py` und speichert sie als CSV."""
    data, category_names = extract_data_from_plot(script_name)

    if data is None or category_names is None:
        print(f"❌ {script_name} konnte nicht konvertiert werden.")
        return

    # DataFrame erstellen
    df = pd.DataFrame(data, index=category_names)

    # CSV speichern (ersetze `.py` mit `.csv`)
    csv_filename = script_name.replace(".py", ".csv")
    csv_filename = csv_filename.replace("PlotCodes", "CSVData")  # Speichert CSV in einem separaten Ordner

    # Sicherstellen, dass der Ordner für CSV-Dateien existiert
    os.makedirs("CSVData", exist_ok=True)

    df.to_csv(csv_filename, encoding="utf-8")
    print(f"✅ {script_name} wurde erfolgreich in {csv_filename} umgewandelt!")

# Sicherstellen, dass der `PlotCodes`-Ordner existiert
if not os.path.exists(plot_folder):
    print(f"❌ Ordner nicht gefunden: {plot_folder}")
    exit()

print("📂 Aktuelles Verzeichnis:", os.getcwd())
print("📋 Vorhandene Dateien in PlotCodes:", os.listdir(plot_folder))

# Alle `plotX.py`-Dateien verarbeiten
for plot_file in plot_files:
    if os.path.exists(plot_file):
        print(f"🔄 Verarbeite Datei: {plot_file}")
        save_plot_data_to_csv(plot_file)
    else:
        print(f"⚠️ Datei fehlt: {plot_file}")

print("✅ Alle Plots wurden erfolgreich in CSV umgewandelt! 🎉")

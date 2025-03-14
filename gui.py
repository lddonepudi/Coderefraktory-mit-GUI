import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

def generate_plot(file, plot_type):
    """Lädt die CSV-Datei und erzeugt das gewünschte Diagramm."""
    try:
        df = pd.read_csv(file.name)

        # Sicherstellen, dass die Datei nicht leer ist
        if df.empty:
            raise ValueError("❌ Die CSV-Datei enthält keine Daten!")

        # Spalten extrahieren
        labels = df.iloc[:, 0].values
        values = df.iloc[:, 1:].sum(axis=1).values  # Falls mehrere Spalten existieren

        # Matplotlib-Figur erstellen
        fig, ax = plt.subplots()

        # Diagrammtyp auswählen
        if plot_type == "Balkendiagramm":
            ax.barh(labels, values, color="blue")
            ax.set_xlabel("Werte")
            ax.set_title("Balkendiagramm")
        elif plot_type == "Kreisdiagramm":
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title("Kreisdiagramm")
        elif plot_type == "Gestapeltes Balkendiagramm":
            ax.bar(labels, values, color="green")
            ax.set_xlabel("Kategorien")
            ax.set_title("Gestapeltes Balkendiagramm")
        else:
            raise ValueError("❌ Ungültiger Plot-Typ!")

        return fig  # 🔥 WICHTIG: Matplotlib-Figur zurückgeben!
    
    except Exception as e:
        # Falls ein Fehler auftritt, eine leere Figure zurückgeben
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"❌ Fehler: {e}", fontsize=12, ha="center", va="center")
        return fig

# Gradio-Interface
with gr.Blocks() as demo:
    gr.Markdown("## 📊 Datenvisualisierung mit CSV-Dateien")
    file_input = gr.File(label="📂 Lade eine CSV-Datei hoch")
    plot_type = gr.Radio(["Balkendiagramm", "Kreisdiagramm", "Gestapeltes Balkendiagramm"],
                          label="📈 Wähle den Diagrammtyp")
    output = gr.Plot()
    
    submit_button = gr.Button("🔍 Plot erzeugen")
    submit_button.click(generate_plot, inputs=[file_input, plot_type], outputs=output)

# App starten
if __name__ == "__main__":
    demo.launch()

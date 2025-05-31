from export.csv_export import export_csv
from export.json_export import export_json

def comparar_exportaciones():
    csv_resultado = export_csv()
    json_resultado = export_json()

    print("\n📊 RESULTADOS DE EXPORTACIÓN:")
    for resultado in [csv_resultado, json_resultado]:
        print(f"\nFormato: {resultado['formato']}")
        print(f"  ⏱ Tiempo: {resultado['tiempo']:.4f} segundos")
        print(f"  📦 Tamaño: {resultado['tamano_kb']:.2f} KB")

if __name__ == "__main__":
    comparar_exportaciones()

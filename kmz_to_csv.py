import zipfile
import xml.etree.ElementTree as ET
import csv
import os

def extract_points_from_kmz(kmz_file_path, output_csv_path):
    """
    Extrai pontos (type P) de um arquivo KMZ e salva em CSV
    
    Args:
        kmz_file_path: Caminho para o arquivo KMZ
        output_csv_path: Caminho para o arquivo CSV de saída
    """
    
    # Namespaces do KML
    namespaces = {
        'kml': 'http://www.opengis.net/kml/2.2',
        'gx': 'http://www.google.com/kml/ext/2.2'
    }
    
    try:
        # Extrair KML do KMZ
        with zipfile.ZipFile(kmz_file_path, 'r') as kmz:
            # Procurar pelo arquivo KML principal (geralmente doc.kml)
            kml_files = [f for f in kmz.namelist() if f.endswith('.kml')]
            
            if not kml_files:
                print("Nenhum arquivo KML encontrado no KMZ!")
                return
            
            # Usar o primeiro arquivo KML encontrado
            kml_file = kml_files[0]
            print(f"Processando arquivo: {kml_file}")
            
            kml_content = kmz.read(kml_file)
        
        # Parse do XML
        root = ET.fromstring(kml_content)
        
        # Lista para armazenar os pontos extraídos
        points_data = []
        
        # Dicionário para mapear elementos para suas pastas
        element_to_folder = {}
        
        # Processar cada folder e mapear elementos
        folders = root.findall('.//kml:Folder', namespaces)
        
        for folder in folders:
            folder_name_elem = folder.find('kml:name', namespaces)
            folder_name = folder_name_elem.text if folder_name_elem is not None else "Unknown"
            
            print(f"Processando pasta: {folder_name}")
            
            # Encontrar todos os placemarks diretamente dentro desta pasta (não recursivo)
            for child in folder:
                if child.tag.endswith('Placemark'):
                    element_to_folder[child] = folder_name
        
        # Processar todos os placemarks
        all_placemarks = root.findall('.//kml:Placemark', namespaces)
        
        
        for placemark in all_placemarks:
            # Verificar se tem um Point (não LineString)
            point = placemark.find('.//kml:Point', namespaces) # XXX porque nao pegamos o LineString se esse parece ser o ponto da ave?
            
            if point is not None:
                # Determinar pasta
                folder_name = element_to_folder.get(placemark, "Root")
                
                # Extrair nome do placemark
                name_elem = placemark.find('kml:name', namespaces)
                name = name_elem.text if name_elem is not None else "Unnamed"
                
                # Extrair coordenadas
                coords_elem = point.find('kml:coordinates', namespaces)
                if coords_elem is not None:
                    coords_text = coords_elem.text.strip()
                    
                    # Formato: longitude,latitude,altitude
                    coords_parts = coords_text.split(',')
                    
                    if len(coords_parts) >= 2:
                        longitude = float(coords_parts[0])
                        latitude = float(coords_parts[1])
                        altitude = float(coords_parts[2]) if len(coords_parts) > 2 else 0.0
                        
                        # Adicionar à lista
                        points_data.append({
                            'latitude': latitude,
                            'longitude': longitude,
                            'altitude_m': altitude,
                            'name': name,
                            'folder': folder_name
                        })
                        
                        print(f"  Ponto extraído: {name} ({latitude}, {longitude}, {altitude}m) - Pasta: {folder_name}")
        
        # Salvar em CSV
        if points_data:
            with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['latitude', 'longitude', 'altitude_m', 'name', 'folder']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escrever cabeçalho
                writer.writeheader()
                
                # Escrever dados
                for point in points_data:
                    writer.writerow(point)
            
            print(f"\n✅ Conversão concluída!")
            print(f"📊 {len(points_data)} pontos extraídos")
            print(f"📁 Arquivo salvo em: {output_csv_path}")
            
        else:
            print("⚠️  Nenhum ponto foi encontrado no arquivo KML!")
            
    except zipfile.BadZipFile:
        print("❌ Erro: O arquivo não é um KMZ válido!")
    except ET.ParseError as e:
        print(f"❌ Erro ao processar XML: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Configurar caminhos dos arquivos
    kmz_input = "data/exemplo.kmz"  # Substitua pelo caminho do seu arquivo KMZ
    csv_output = "data/pontos_extraidos.csv"  # Nome do arquivo CSV de saída
    
    # Verificar se o arquivo KMZ existe
    if os.path.exists(kmz_input):
        extract_points_from_kmz(kmz_input, csv_output)
    else:
        print(f"❌ Arquivo {kmz_input} não encontrado!")
        print("Por favor, verifique o caminho do arquivo.")

import zipfile
import xml.etree.ElementTree as ET
import csv
import os

def extract_bird_positions_from_kmz(kmz_file_path, output_csv_path):
    """
    Extrai apenas as posições das aves de um arquivo KMZ
    Considera apenas pontos com estilos que contenham "_polygon"
    
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
            kml_content = kmz.read(kml_file)
        
        # Parse do XML
        root = ET.fromstring(kml_content)
        
        # Lista para armazenar as posições das aves
        bird_positions = []
        
        # Dicionário para mapear elementos para suas pastas
        element_to_folder = {}
        
        # Processar cada folder e mapear elementos
        folders = root.findall('.//kml:Folder', namespaces)
        
        for folder in folders:
            folder_name_elem = folder.find('kml:name', namespaces)
            folder_name = folder_name_elem.text if folder_name_elem is not None else "Unknown"
            
            # Encontrar todos os placemarks diretamente dentro desta pasta (não recursivo)
            for child in folder:
                if child.tag.endswith('Placemark'):
                    element_to_folder[child] = folder_name
        
        # Processar todos os placemarks
        all_placemarks = root.findall('.//kml:Placemark', namespaces)
        
        for placemark in all_placemarks:
            # Verificar se tem um Point
            point = placemark.find('.//kml:Point', namespaces)
            
            if point is not None:
                # Verificar se tem styleUrl com "_polygon"
                style_url_elem = placemark.find('kml:styleUrl', namespaces)
                
                if style_url_elem is not None:
                    style_url = style_url_elem.text
                    
                    # Filtrar apenas estilos que contenham "_polygon"
                    if style_url and "_polygon" in style_url:
                        # Determinar pasta
                        folder_name = element_to_folder.get(placemark, "Root")
                        
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
                                bird_positions.append({
                                    'pasta': folder_name,
                                    'latitude': latitude,
                                    'longitude': longitude,
                                    'altitude': altitude
                                })
        
        # Salvar em CSV
        if bird_positions:
            with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['pasta', 'latitude', 'longitude', 'altitude']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escrever cabeçalho
                writer.writeheader()
                
                # Escrever dados
                for bird in bird_positions:
                    writer.writerow(bird)
            
            print(f"CSV gerado: {output_csv_path}")
            print(f"Total de registros: {len(bird_positions)}")
            
        else:
            print("Nenhuma posição de ave encontrada!")
            
    except zipfile.BadZipFile:
        print("Erro: O arquivo não é um KMZ válido!")
    except ET.ParseError as e:
        print(f"Erro ao processar XML: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Configurar caminhos dos arquivos
    kmz_input = "data/exemplo.kmz"  # Substitua pelo caminho do seu arquivo KMZ
    csv_output = "tmp/aves_posicoes.csv"  # Nome do arquivo CSV de saída
    
    # Verificar se o arquivo KMZ existe
    if os.path.exists(kmz_input):
        extract_bird_positions_from_kmz(kmz_input, csv_output)
    else:
        print(f"Arquivo {kmz_input} não encontrado!")
        print("Por favor, verifique o caminho do arquivo.")

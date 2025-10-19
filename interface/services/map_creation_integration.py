# services/map_creation_integration.py
"""
Serviço de integração para o módulo de criação de mapas.

Este módulo fornece funções para integrar o módulo modulo_criacao_mapas
com a interface Streamlit, incluindo conversão de mapas e gerenciamento
de arquivos gerados.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import streamlit as st

# Adicionar o módulo de criação de mapas ao path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
map_creation_module = project_root / "modulo_criacao_mapas"
sys.path.append(str(map_creation_module))

try:
    from map_converter_utils import converter_mapa, retornaPrctCombust
except ImportError as e:
    st.error(f"Erro ao importar módulo de criação de mapas: {e}")
    converter_mapa = None
    retornaPrctCombust = None

class MapCreationIntegration:
    """Classe para integração do módulo de criação de mapas com a interface."""
    
    def __init__(self):
        self.mapas_dir = Path("mapas")
        self.mapas_dir.mkdir(exist_ok=True)
        
        # Cores padrão do sistema
        self.colors = {
            'Parede': ((0, 0, 0), '#000000', '1'),
            'Espaço vazio': ((255, 255, 255), '#FFFFFF', '0'),
            'Tapete/Caminho': ((255, 165, 0), '#FFA500', '9'),
            'Porta/Saída': ((255, 0, 0), '#FF0000', '2'),
            'Janelas': ((0, 255, 0), '#00FF00', '7'),
            'Inocupável': ((192, 192, 192), '#C0C0C0', '8'),
        }
    
    def get_color_scheme(self) -> Dict[str, Tuple[Tuple[int, int, int], str, str]]:
        """Retorna o esquema de cores padrão."""
        return self.colors
    
    def validate_map_image(self, image_path: str) -> Tuple[bool, str]:
        """
        Valida se uma imagem PNG é compatível com o sistema de mapas.
        
        Args:
            image_path: Caminho para a imagem PNG
            
        Returns:
            Tuple[bool, str]: (é_válida, mensagem)
        """
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Verificar se tem dimensões válidas
            if img_array.shape[0] < 5 or img_array.shape[1] < 5:
                return False, "Imagem muito pequena (mínimo 5x5 pixels)"
            
            if img_array.shape[0] > 100 or img_array.shape[1] > 100:
                return False, "Imagem muito grande (máximo 100x100 pixels)"
            
            # Verificar se usa cores compatíveis
            unique_colors = set()
            for row in img_array:
                for pixel in row:
                    if len(pixel) >= 3:  # RGB ou RGBA
                        rgb = tuple(pixel[:3])
                        unique_colors.add(rgb)
            
            # Verificar se todas as cores são compatíveis
            compatible_colors = {color[0] for color in self.colors.values()}
            incompatible = unique_colors - compatible_colors
            
            if incompatible:
                return False, f"Cores incompatíveis encontradas: {incompatible}"
            
            return True, "Imagem válida"
            
        except Exception as e:
            return False, f"Erro ao validar imagem: {e}"
    
    def convert_image_to_maps(self, image_path: str, output_base_name: str) -> Dict[str, str]:
        """
        Converte uma imagem PNG em arquivos de mapa.
        
        Args:
            image_path: Caminho para a imagem PNG
            output_base_name: Nome base para os arquivos de saída
            
        Returns:
            Dict[str, str]: Dicionário com caminhos dos arquivos gerados
        """
        if converter_mapa is None:
            raise ImportError("Módulo de conversão não disponível")
        
        try:
            # Validar imagem primeiro
            is_valid, message = self.validate_map_image(image_path)
            if not is_valid:
                raise ValueError(f"Imagem inválida: {message}")
            
            # Converter usando o módulo original
            converter_mapa(image_path, output_base_name)
            
            # Verificar arquivos gerados
            generated_files = {}
            map_files = {
                "main": f"{output_base_name}.map",
                "fire": f"{output_base_name}_fogo.map",
                "wind": f"{output_base_name}_vento.map"
            }
            
            for key, filename in map_files.items():
                if os.path.exists(filename):
                    generated_files[key] = filename
            
            return generated_files
            
        except Exception as e:
            raise Exception(f"Erro na conversão: {e}")
    
    def save_map_to_directory(self, map_data: List[List[Tuple[int, int, int]]], 
                            filename: str) -> str:
        """
        Salva dados de mapa como PNG no diretório de mapas.
        
        Args:
            map_data: Dados do mapa (lista de listas de RGB)
            filename: Nome do arquivo (sem extensão)
            
        Returns:
            str: Caminho do arquivo salvo
        """
        try:
            from PIL import Image
            
            # Criar imagem
            rows = len(map_data)
            cols = len(map_data[0])
            img = Image.new('RGB', (cols, rows))
            
            for y in range(rows):
                for x in range(cols):
                    img.putpixel((x, y), map_data[y][x])
            
            # Salvar no diretório de mapas
            output_path = self.mapas_dir / f"{filename}.png"
            img.save(output_path)
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Erro ao salvar mapa: {e}")
    
    def get_map_files(self) -> List[Path]:
        """Retorna lista de arquivos de mapa disponíveis."""
        return list(self.mapas_dir.glob("*.png"))
    
    def delete_map(self, filename: str) -> bool:
        """
        Remove um mapa do diretório.
        
        Args:
            filename: Nome do arquivo (com ou sem extensão)
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            if not filename.endswith('.png'):
                filename += '.png'
            
            map_path = self.mapas_dir / filename
            if map_path.exists():
                map_path.unlink()
                return True
            return False
            
        except Exception as e:
            st.error(f"Erro ao remover mapa: {e}")
            return False
    
    def create_map_from_template(self, template_name: str, rows: int, cols: int) -> List[List[Tuple[int, int, int]]]:
        """
        Cria um mapa baseado em um template.
        
        Args:
            template_name: Nome do template ('empty', 'room', 'corridor')
            rows: Número de linhas
            cols: Número de colunas
            
        Returns:
            List[List[Tuple[int, int, int]]]: Dados do mapa
        """
        # Criar mapa vazio
        map_data = [[(255, 255, 255) for _ in range(cols)] for _ in range(rows)]
        
        if template_name == 'empty':
            # Mapa vazio (já criado)
            pass
            
        elif template_name == 'room':
            # Sala simples com paredes e uma porta
            wall_color = self.colors['Parede'][0]
            door_color = self.colors['Porta/Saída'][0]
            
            # Paredes externas
            for i in range(rows):
                map_data[i][0] = wall_color  # Parede esquerda
                map_data[i][cols-1] = wall_color  # Parede direita
            for j in range(cols):
                map_data[0][j] = wall_color  # Parede superior
                map_data[rows-1][j] = wall_color  # Parede inferior
            
            # Porta no meio da parede direita
            door_pos = rows // 2
            map_data[door_pos][cols-1] = door_color
            
        elif template_name == 'corridor':
            # Corredor com paredes laterais
            wall_color = self.colors['Parede'][0]
            door_color = self.colors['Porta/Saída'][0]
            
            # Paredes laterais
            for i in range(rows):
                map_data[i][0] = wall_color
                map_data[i][cols-1] = wall_color
            
            # Portas nas extremidades
            map_data[0][cols//2] = door_color  # Porta superior
            map_data[rows-1][cols//2] = door_color  # Porta inferior
        
        return map_data
    
    def get_map_statistics(self, map_data: List[List[Tuple[int, int, int]]]) -> Dict[str, int]:
        """
        Calcula estatísticas de um mapa.
        
        Args:
            map_data: Dados do mapa
            
        Returns:
            Dict[str, int]: Estatísticas do mapa
        """
        stats = {}
        total_pixels = len(map_data) * len(map_data[0])
        
        # Contar cada tipo de terreno
        for name, (rgb, _, code) in self.colors.items():
            count = 0
            for row in map_data:
                for pixel in row:
                    if pixel == rgb:
                        count += 1
            stats[name] = count
        
        # Calcular porcentagens
        for name in stats:
            stats[f"{name}_percent"] = round((stats[name] / total_pixels) * 100, 1)
        
        return stats

# Instância global do serviço
map_creation_service = MapCreationIntegration()


#!/usr/bin/env python3
"""
Script para criar GIF animado a partir dos frames de simulação.

Este script lê os frames PNG gerados durante uma simulação (quando draw mode está ativo)
e cria um GIF animado mostrando a evolução da evacuação.

Uso:
    python scripts/create_simulation_gif.py <nome_do_experimento> [--fps 10] [--output output.gif]
    
Exemplo:
    python scripts/create_simulation_gif.py minha_simulacao --fps 15 --output evacuacao.gif
"""

import argparse
from pathlib import Path
from PIL import Image
import sys

def create_gif_from_frames(experiment_name: str, fps: int = 10, output_path: str = None):
    """
    Cria um GIF animado a partir dos frames de uma simulação.
    
    Args:
        experiment_name: Nome do experimento/simulação
        fps: Frames por segundo (padrão: 10)
        output_path: Caminho de saída do GIF (padrão: <experiment_name>.gif)
    
    Returns:
        Path do GIF criado ou None se falhar
    """
    # Diretório de saída da simulação
    output_dir = Path("simulador_heuristica") / "output" / experiment_name
    
    if not output_dir.exists():
        print(f"❌ Erro: Diretório de saída não encontrado: {output_dir}")
        print(f"   Certifique-se de que a simulação '{experiment_name}' foi executada com draw mode ativo.")
        return None
    
    # Procura por frames dinâmicos (principal visualização)
    frame_files = sorted(output_dir.glob("dinamic_map_*.png"), key=lambda p: int(p.stem.split('_')[-1]))
    
    if not frame_files:
        print(f"❌ Erro: Nenhum frame encontrado em {output_dir}")
        print("   Certifique-se de que a simulação foi executada com draw mode ativo (-d flag)")
        return None
    
    print(f"✅ Encontrados {len(frame_files)} frames em {output_dir}")
    
    # Define caminho de saída
    if output_path is None:
        output_path = f"{experiment_name}.gif"
    
    output_file = Path(output_path)
    
    # Carrega todas as imagens
    print(f"📸 Carregando frames...")
    frames = []
    for i, frame_file in enumerate(frame_files):
        try:
            img = Image.open(frame_file)
            frames.append(img)
            if (i + 1) % 50 == 0:
                print(f"   Carregados {i + 1}/{len(frame_files)} frames...")
        except Exception as e:
            print(f"⚠️  Aviso: Erro ao carregar frame {frame_file}: {e}")
            continue
    
    if not frames:
        print(f"❌ Erro: Nenhum frame válido carregado")
        return None
    
    print(f"✅ {len(frames)} frames carregados com sucesso")
    
    # Calcula duração de cada frame em milissegundos
    duration = int(1000 / fps)
    
    # Salva como GIF
    print(f"🎬 Criando GIF com {fps} FPS (duração: {duration}ms por frame)...")
    try:
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,  # 0 = loop infinito
            optimize=True
        )
        
        # Mostra informações do arquivo gerado
        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"\n✅ GIF criado com sucesso!")
        print(f"   📁 Arquivo: {output_file.absolute()}")
        print(f"   📊 Tamanho: {file_size_mb:.2f} MB")
        print(f"   🎞️  Frames: {len(frames)}")
        print(f"   ⏱️  FPS: {fps}")
        print(f"   🔄 Loop: Infinito")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Erro ao criar GIF: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Cria GIF animado a partir dos frames de uma simulação",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s minha_simulacao
  %(prog)s minha_simulacao --fps 15
  %(prog)s minha_simulacao --fps 20 --output resultados/evacuacao.gif
        """
    )
    
    parser.add_argument(
        "experiment",
        help="Nome do experimento/simulação"
    )
    
    parser.add_argument(
        "--fps",
        type=int,
        default=10,
        help="Frames por segundo do GIF (padrão: 10)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Caminho de saída do GIF (padrão: <experiment>.gif)"
    )
    
    args = parser.parse_args()
    
    # Validação
    if args.fps <= 0 or args.fps > 60:
        print(f"❌ Erro: FPS deve estar entre 1 e 60 (fornecido: {args.fps})")
        sys.exit(1)
    
    # Cria GIF
    result = create_gif_from_frames(args.experiment, args.fps, args.output)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

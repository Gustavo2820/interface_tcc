import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image
import os
import sys
from pathlib import Path
from map_converter_utils import converter_mapa

# Configurações iniciais
default_rows = 20
default_cols = 20
default_cell_size = 25

# Cores e seus significados
COLORS = {
    'Parede': ((0, 0, 0), '#000000'),
    'Espaço vazio': ((255, 255, 255), '#FFFFFF'),
    'Tapete/Caminho': ((255, 165, 0), '#FFA500'),
    'Inocupável': ((128, 128, 128), '#808080'),
    'Porta/Saída': ((255, 0, 0), '#FF0000'),
}

class PixelMapEditor(tk.Tk):
    def __init__(self, rows=default_rows, cols=default_cols, cell_size=default_cell_size, 
                 auto_save_dir=None, web_integration=False):
        super().__init__()
        self.title('Editor de Mapas Pixel Art')
        self.resizable(False, False)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.selected_color_name = 'Parede'
        self.selected_rgb, self.selected_hex = COLORS[self.selected_color_name]
        self.map = [[(255, 255, 255) for _ in range(cols)] for _ in range(rows)]
        self.auto_save_dir = auto_save_dir
        self.web_integration = web_integration
        self._build_ui()
        self._draw_map()

    def _build_ui(self):
        # Legenda das cores (nome e cor visual)
        legenda_frame = tk.Frame(self)
        legenda_frame.pack(pady=(10, 0))
        tk.Label(legenda_frame, text='Legenda: ', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        for nome, (rgb, hex_color) in COLORS.items():
            tk.Label(legenda_frame, text=nome, fg=hex_color, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

        # Frame para seleção de cor
        color_frame = tk.Frame(self)
        color_frame.pack(pady=5)
        tk.Label(color_frame, text='Selecione a cor:').pack(side=tk.LEFT)
        self.color_buttons = {}
        for name, (rgb, hex_color) in COLORS.items():
            btn = tk.Button(color_frame, bg=hex_color, width=3, relief=tk.SUNKEN if name==self.selected_color_name else tk.RAISED,
                            command=lambda n=name: self._select_color(n))
            btn.pack(side=tk.LEFT, padx=2)
            self.color_buttons[name] = btn

        # Canvas para o mapa
        self.canvas = tk.Canvas(self, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg='white')
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.canvas.bind('<B1-Motion>', self._on_canvas_click)

        # Botões de ação
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)
        
        # Botão de salvar
        save_btn = tk.Button(button_frame, text='Salvar como PNG', command=self._save_as_png)
        save_btn.pack(side=tk.LEFT, padx=5)

        # Botão de salvar no diretório de mapas (se configurado)
        if self.auto_save_dir:
            auto_save_btn = tk.Button(button_frame, text='Salvar no Sistema', command=self._save_to_system)
            auto_save_btn.pack(side=tk.LEFT, padx=5)

        # Botão de converter imagem existente
        import_btn = tk.Button(button_frame, text='Converter imagem existente', command=self._importar_e_converter)
        import_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão de carregar mapa existente
        load_btn = tk.Button(button_frame, text='Carregar Mapa', command=self._load_map)
        load_btn.pack(side=tk.LEFT, padx=5)

    def _select_color(self, name):
        self.selected_color_name = name
        self.selected_rgb, self.selected_hex = COLORS[name]
        for n, btn in self.color_buttons.items():
            btn.config(relief=tk.SUNKEN if n==name else tk.RAISED)

    def _on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.map[row][col] = self.selected_rgb
            self._draw_cell(row, col)

    def _draw_map(self):
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                self._draw_cell(row, col)

    def _draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        color = '#%02x%02x%02x' % self.map[row][col]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def _save_as_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if not file_path:
            return
        img = Image.new('RGB', (self.cols, self.rows))
        for y in range(self.rows):
            for x in range(self.cols):
                img.putpixel((x, y), self.map[y][x])
        try:
            img.save(file_path)
            # Conversão automática após salvar
            base_path = file_path.rsplit('.', 1)[0]
            converter_mapa(file_path, base_path)
            messagebox.showinfo('Sucesso', f'Mapa salvo em {file_path}\nArquivos .map gerados no mesmo local.')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível salvar ou converter: {e}')

    def _save_to_system(self):
        """Salva o mapa no diretório de mapas do sistema"""
        if not self.auto_save_dir:
            messagebox.showerror('Erro', 'Diretório de salvamento não configurado')
            return
            
        # Pedir nome do arquivo
        filename = simpledialog.askstring("Nome do Mapa", "Digite o nome do mapa (sem extensão):")
        if not filename:
            return
            
        try:
            # Criar diretório se não existir
            os.makedirs(self.auto_save_dir, exist_ok=True)
            
            # Salvar PNG
            png_path = os.path.join(self.auto_save_dir, f"{filename}.png")
            img = Image.new('RGB', (self.cols, self.rows))
            for y in range(self.rows):
                for x in range(self.cols):
                    img.putpixel((x, y), self.map[y][x])
            img.save(png_path)
            
            # Converter para arquivos .map
            base_path = os.path.join(self.auto_save_dir, filename)
            converter_mapa(png_path, base_path)
            
            messagebox.showinfo('Sucesso', f'Mapa salvo no sistema:\n{png_path}\nArquivos .map gerados automaticamente.')
            
            # Se for integração web, notificar que o mapa foi salvo
            if self.web_integration:
                self._notify_web_integration(filename)
                
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar no sistema: {e}')
    
    def _load_map(self):
        """Carrega um mapa PNG existente"""
        img_path = filedialog.askopenfilename(title='Selecione um mapa PNG para carregar', 
                                           filetypes=[('PNG files', '*.png')])
        if not img_path:
            return
            
        try:
            img = Image.open(img_path)
            if img.size != (self.cols, self.rows):
                # Redimensionar se necessário
                img = img.resize((self.cols, self.rows), Image.NEAREST)
            
            # Carregar dados do mapa
            self.map = []
            for y in range(self.rows):
                row = []
                for x in range(self.cols):
                    pixel = img.getpixel((x, y))
                    if len(pixel) >= 3:  # RGB ou RGBA
                        row.append(pixel[:3])
                    else:
                        row.append((255, 255, 255))  # Default branco
                self.map.append(row)
            
            # Redesenhar o mapa
            self._draw_map()
            messagebox.showinfo('Sucesso', f'Mapa carregado: {img_path}')
            
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao carregar mapa: {e}')
    
    def _notify_web_integration(self, filename):
        """Notifica a integração web que um mapa foi salvo"""
        # Criar arquivo de notificação para a integração web
        notification_file = os.path.join(self.auto_save_dir, f".{filename}_saved")
        with open(notification_file, 'w') as f:
            f.write(f"Mapa {filename} salvo em {os.path.join(self.auto_save_dir, f'{filename}.png')}")
    
    def _importar_e_converter(self):
        img_path = filedialog.askopenfilename(title='Selecione a imagem para converter', filetypes=[('Imagens', '*.png;*.jpg;*.jpeg')])
        if not img_path:
            return
        try:
            base_path = img_path.rsplit('.', 1)[0]
            converter_mapa(img_path, base_path)
            messagebox.showinfo('Sucesso', f'Arquivos .map gerados no mesmo local de {img_path}')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao converter imagem: {e}')

def create_map_editor(rows=default_rows, cols=default_cols, cell_size=default_cell_size, 
                     auto_save_dir=None, web_integration=False):
    """
    Cria uma instância do editor de mapas com configurações específicas.
    
    Args:
        rows: Número de linhas do mapa
        cols: Número de colunas do mapa
        cell_size: Tamanho de cada célula em pixels
        auto_save_dir: Diretório para salvamento automático
        web_integration: Se True, configura para integração web
    
    Returns:
        PixelMapEditor: Instância do editor
    """
    return PixelMapEditor(rows, cols, cell_size, auto_save_dir, web_integration)

def launch_map_editor():
    """Lança o editor de mapas com janela de configuração"""
    def start_editor():
        try:
            width_px = int(width_var.get())
            height_px = int(height_var.get())
            cell_size = int(cell_size_var.get())
            # No editor, cols = largura (px) e rows = altura (px)
            cols = width_px
            rows = height_px
            config_win.destroy()
            app = PixelMapEditor(rows, cols, cell_size)
            app.mainloop()
        except Exception as e:
            messagebox.showerror('Erro', f'Valores inválidos: {e}')

    config_win = tk.Tk()
    config_win.title('Configuração do Mapa')
    tk.Label(config_win, text='Largura (px):').grid(row=0, column=0)
    tk.Label(config_win, text='Altura (px):').grid(row=1, column=0)
    tk.Label(config_win, text='Tamanho da célula (px):').grid(row=2, column=0)
    width_var = tk.StringVar(value=str(default_cols))
    height_var = tk.StringVar(value=str(default_rows))
    cell_size_var = tk.StringVar(value=str(default_cell_size))
    tk.Entry(config_win, textvariable=width_var, width=7).grid(row=0, column=1)
    tk.Entry(config_win, textvariable=height_var, width=7).grid(row=1, column=1)
    tk.Entry(config_win, textvariable=cell_size_var, width=7).grid(row=2, column=1)
    tk.Button(config_win, text='Iniciar Editor', command=start_editor).grid(row=3, column=0, columnspan=2, pady=5)
    config_win.mainloop()

if __name__ == '__main__':
    launch_map_editor() 
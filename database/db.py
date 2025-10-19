import sqlite3

# Conectar ao banco (cria o arquivo se não existir)
con = sqlite3.connect("simulador.db")
cur = con.cursor()

# Criar tabela Mapa
cur.execute("""
CREATE TABLE IF NOT EXISTS Mapa (
    id_mapa INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    arquivo_map TEXT NOT NULL
)
""")

# Criar tabela Simulacao com chave composta (id_simulacao + id_mapa)
cur.execute("""
CREATE TABLE IF NOT EXISTS Simulacao (
    id_simulacao INTEGER NOT NULL,
    id_mapa INTEGER NOT NULL,
    nome TEXT NOT NULL,
    algoritmo TEXT NOT NULL,
    config_pedestres_json TEXT NOT NULL,
    pos_pedestres_json TEXT,
    config_simulacao_json TEXT NOT NULL,
    cli_config_json TEXT NOT NULL,
    nsga_config_json TEXT,
    executada INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id_simulacao, id_mapa),
    FOREIGN KEY (id_mapa) REFERENCES Mapa(id_mapa) ON DELETE CASCADE
)
""")

# Criar tabela Resultado com chave composta (id_resultado + id_simulacao)
cur.execute("""
CREATE TABLE IF NOT EXISTS Resultado (
    id_resultado INTEGER NOT NULL,
    id_simulacao INTEGER NOT NULL,
    frente_pareto_json TEXT NOT NULL,
    PRIMARY KEY (id_resultado, id_simulacao),
    FOREIGN KEY (id_simulacao) REFERENCES Simulacao(id_simulacao) ON DELETE CASCADE
)
""")

# Criar tabela Preset
cur.execute("""
CREATE TABLE IF NOT EXISTS Preset (
    id_preset INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,       
    parametros_json TEXT NOT NULL
)
""")

# Salvar alterações e fechar
con.commit()
con.close()

print("Banco de dados criado com sucesso!")
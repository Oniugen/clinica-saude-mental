import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'clinica.db')
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado. Ele será criado na primeira execução.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Adicionar coluna consultorio_sala em agendamentos se não existir
    try:
        cursor.execute("ALTER TABLE agendamentos ADD COLUMN consultorio_sala TEXT")
        print("Coluna consultorio_sala adicionada à tabela agendamentos.")
    except sqlite3.OperationalError:
        print("Coluna consultorio_sala já existe na tabela agendamentos.")

    # Adicionar coluna consultorio_sala em consultas se não existir
    try:
        cursor.execute("ALTER TABLE consultas ADD COLUMN consultorio_sala TEXT")
        print("Coluna consultorio_sala adicionada à tabela consultas.")
    except sqlite3.OperationalError:
        print("Coluna consultorio_sala já existe na tabela consultas.")

    conn.commit()
    conn.close()
    print("Migração concluída com sucesso.")

if __name__ == "__main__":
    migrate()

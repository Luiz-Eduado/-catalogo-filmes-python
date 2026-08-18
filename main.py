import sqlite3

DB = "banco.db"

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    with conectar() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10)
        );
        """)

def cadastrar_filme():
    titulo = input("Título: ").strip()
    genero = input("Gênero: ").strip()
    ano = int(input("Ano: "))
    nota = float(input("Nota (0 a 10): "))

    with conectar() as conn:
        conn.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (titulo, genero, ano, nota)
        )
    print("Filme cadastrado com sucesso!")

def listar_filmes():
    with conectar() as conn:
        filmes = conn.execute(
            "SELECT id, titulo, genero, ano, nota FROM filmes ORDER BY titulo"
        ).fetchall()

    if not filmes:
        print("Nenhum filme cadastrado.")
        return

    print("\n--- FILMES ---")
    for filme in filmes:
        print(
            f"{filme['id']} | {filme['titulo']} | "
            f"{filme['genero']} | {filme['ano']} | Nota: {filme['nota']:.1f}"
        )

def buscar_por_genero():
    genero = input("Digite o gênero: ").strip()

    with conectar() as conn:
        filmes = conn.execute(
            "SELECT titulo, genero, ano, nota FROM filmes "
            "WHERE genero LIKE ? ORDER BY nota DESC",
            (f"%{genero}%",)
        ).fetchall()

    if not filmes:
        print("Nenhum resultado encontrado.")
        return

    for filme in filmes:
        print(
            f"{filme['titulo']} | {filme['genero']} | "
            f"{filme['ano']} | Nota: {filme['nota']:.1f}"
        )

def remover_filme():
    try:
        filme_id = int(input("ID do filme que deseja remover: "))
    except ValueError:
        print("ID inválido.")
        return

    with conectar() as conn:
        cursor = conn.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))

    if cursor.rowcount:
        print("Filme removido com sucesso!")
    else:
        print("Filme não encontrado.")

def menu():
    criar_banco()

    while True:
        print("""
========= CATÁLOGO DE FILMES =========
1 - Cadastrar filme
2 - Listar filmes
3 - Buscar por gênero
4 - Remover filme
0 - Sair
=======================================
""")
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_filme()
            elif opcao == "2":
                listar_filmes()
            elif opcao == "3":
                buscar_por_genero()
            elif opcao == "4":
                remover_filme()
            elif opcao == "0":
                print("Programa encerrado.")
                break
            else:
                print("Opção inválida.")
        except (ValueError, sqlite3.Error) as erro:
            print(f"Erro: {erro}")

if __name__ == "__main__":
    menu()

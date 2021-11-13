import sqlite3
from sqlite3.dbapi2 import Error
from tratamento_json import somente_pilotos


class Connect:
    def __init__(self, db_name: str):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            print(f"Banco de dados: {db_name}")
            self.cursor.execute("SELECT SQLITE_VERSION()")
            self.data = self.cursor.fetchone()
            print(f"SQLite version: {self.data}")
        except sqlite3.Error:
            print("Erro ao abrir o banco de dados")
            return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()


class Pilotos:
    db_name = 'all_f1_pilots'

    def __init__(self):
        self.db = Connect('all_f1_pilots.db')
        self.db_name

    def create_schema(self, schema_name='sql/pilotos_schema.sql'):
        print(f"Criando tabela {self.db_name}...")
        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error as err:
            print(f'A tabela {self.db_name} já existe', err)
            return False
        print("Tabela criada com sucesso")

    def inserir_todos_pilotos(self, file_name: str = 'pilotos/todos_pilotos.json'):
        pilotos = somente_pilotos()
        for piloto in pilotos['Drivers']:
            self.db.cursor.execute("""
                INSERT INTO pilotos (driverId, biografia, nome, sobrenome, dataDeNascimento, nacionalidade)
                VALUES (?,?,?,?,?,?)
                """, (piloto['driverId'], piloto['url'], piloto['givenName'], piloto['familyName'], piloto['dateOfBirth'], piloto['nationality']))

    def ler_todos_pilotos(self):
        sql = "SELECT * FROM pilotos ORDER BY nome"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def localizar_piloto(self, nome: str):
        piloto = self.db.cursor.execute(
            'SELECT * FROM pilotos WHERE nome = ?', (nome,)
        )
        return piloto.fetchone()

    def imprimir_piloto(self, nome: str):
        if self.localizar_piloto(nome) == None:
            print("Não existe piloto com o nome informado")
        else:
            print(self.localizar_piloto(nome))

    def contar_pilotos(self):
        numero_de_pilotos = self.db.cursor.execute(
            'SELECT COUNT(*) FROM pilotos'
        )
        print("Total de clientes: ", numero_de_pilotos.fetchone()[0])

    def contar_pilotos_por_nacionalidade(self, nacionalidade: str = 'Brazilian'):
        pilotos = self.db.cursor.execute(
            'SELECT * FROM pilotos WHERE nacionalidade = ?', (nacionalidade,)
        )
        print("Número de pilotos brasileiros que já passaram pela F1: ",
              pilotos.fetchone()[0])

    def atualizar_biografia(self, nome: str, link: str):
        try:
            clientes = self.localizar_piloto(nome)
            if clientes:
                self.db.cursor.execute("""
                UPDATE pilotos
                SET biografia = ?
                WHERE nome = ?
                """, link, nome,)
                self.db.commit_db()
                print("Dados atualizados com sucesso")
            else:
                print("Não existe piloto com o nome informado")
        except Error:
            raise Error

    def deletar_piloto(self, nome):
        try:
            piloto = self.localizar_piloto(nome)
            if piloto:
                self.db.cursor.execute("""
                DELETE FROM pilotos WHERE nome = ?
                """, (nome,))
                self.db.commit_db()
                print(f"piloto {piloto} excluído com sucesso")
            else:
                print("Não existe piloto com o nome informado")
        except Error:
            raise Error

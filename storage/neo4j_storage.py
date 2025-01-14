#from chatterbot.tagging import PosHypernymTagger
from chatterbot import languages
from chatterbot.storage import StorageAdapterCypher  # Importez StorageAdapterCypher au lieu de StorageAdapter
from neo4j import GraphDatabase
from chatterbot.conversation import Statement

class Neo4jStorageAdapter(StorageAdapterCypher):  # Héritez de StorageAdapterCypher
    def __init__(self, uri, user, password):
        try:
            self.tagger = PosHypernymTagger(language=languages.FRE)
        except ImportError as e:
            print(f"Erreur lors de l'import de PosHypernymTagger : {e}")
            self.tagger = None

        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")

    # ... (le reste du code reste inchangé)



    def create(self, statement):
        with self.driver.session() as session:
            session.write_transaction(self._create_statement, statement)

    @staticmethod
    def _create_statement(tx, statement):
        query = (
            "CREATE (s:Statement {text: $text, response: $response}) "
            "RETURN s"
        )
        result = tx.run(query, text=statement.text, response=getattr(statement, 'response', None))
        return result.single()[0]

    def create_many(self, statements):
        with self.driver.session() as session:
            for statement in statements:
                session.write_transaction(self._create_statement, statement)


    def retrieve(self, statement_text):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Statement {text: $text}) RETURN n", text=statement_text)
            return [Statement(text=record["n"]["text"], response=record["n"]["response"]) for record in result]

    def update(self, statement):
        with self.driver.session() as session:
            session.write_transaction(self._update_statement, statement)

    @staticmethod
    def _update_statement(tx, statement):
        query = (
            "MATCH (s:Statement {text: $text}) "
            "SET s.response = $response "
            "RETURN s"
        )
        result = tx.run(query, text=statement.text, response=getattr(statement, 'response', None))
        return result.single()[0]

    def delete(self, statement):
        with self.driver.session() as session:
            session.write_transaction(self._delete_statement, statement)

@staticmethod

@staticmethod
def _delete_statement(tx, statement):
    query = (
        "MATCH (s:Statement {text: $text}) "
        "DELETE s"
    )
    tx.run(query, text=statement.text)

def filter(self, **kwargs):
        with self.driver.session() as session:
            return session.read_transaction(self._filter_statements, **kwargs)

@staticmethod

@staticmethod
def _filter_statements(tx, **kwargs):
    query = "MATCH (s:Statement) WHERE "
    conditions = []
    for key, value in kwargs.items():
        if isinstance(value, str):
            conditions.append(f"s.{key} =~ '{value}'")
        else:
            conditions.append(f"s.{key} = {value}")
    query += " AND ".join(conditions) 
    query += " RETURN s"
    results = tx.run(query)
    statements = []
    for record in results:
        node = record[0]
        statement = Statement(text=node["text"], response=node["response"])
        statements.append(statement)
    return statements


    def count(self):
        with self.driver.session() as session:
            return session.read_transaction(self._count_statements)

    @staticmethod
    def _count_statements(tx):
        query = "MATCH (s:Statement) RETURN count(s)"
        result = tx.run(query)
        return result.single()[0]

    def get_random(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_random_statement)

    @staticmethod
    def _get_random_statement(tx):
        query = (
            "MATCH (s:Statement) "
            "RETURN s, rand() as r "
            "ORDER BY r "
            "LIMIT 1"
        )
        result = tx.run(query)
        node = result.single()[0]
        statement = Statement(text=node["text"], response=node["response"])
        return statement
def drop(self):
        with self.driver.session() as session:
            session.write_transaction(self._drop_database)

@staticmethod

def _drop_database(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)


    def get_response_statements(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_response_statements)

    @staticmethod
    def _get_response_statements(tx):
        query = "MATCH (s:Statement) WHERE s.response IS NOT NULL RETURN s"
        results = tx.run(query)
        statements = []
        for record in results:
            node = record[0]
            statement = Statement(text=node["text"], response=node["response"])
            statements.append(statement)
        return statements

    # Nouvelles fonctionnalitÃ©s ajoutÃ©es
    def advanced_search(self, pattern):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Statement) WHERE n.text =~ $pattern RETURN n", pattern=pattern)
            return [Statement(text=record["n"]["text"], response=record["n"]["response"]) for record in result]

    def create_relation(self, statement_text_1, statement_text_2, relation_type):
        with self.driver.session() as session:
            session.run("MATCH (n1:Statement {text: $text1}), (n2:Statement {text: $text2}) "
                        "CREATE (n1)-[:RELATION {type: $type}]->(n2)", text1=statement_text_1, text2=statement_text_2, type=relation_type)

    def associate_with_user(self, statement_text, username):
        with self.driver.session() as session:
            session.run("MATCH (u:User {name: $username}), (n:Statement {text: $text}) "
                        "MERGE (u)-[:ASSOCIATED_WITH]->(n)", username=username, text=statement_text)

    def get_user_statements(self, username):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User {name: $username})-[:ASSOCIATED_WITH]->(n:Statement) RETURN n", username=username)
            return [Statement(text=record["n"]["text"], response=record["n"]["response"]) for record in result]

    def collect_statistics(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Statement) RETURN n.text, n.response, size((n)<-[:USED_IN]-()) as usage_count")

import logging
from chatterbot import languages
from chatterbot.tagging import PosLemmaTagger
from neo4j import GraphDatabase

class StorageAdapterCypher(object):
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")

        self.tagger = PosLemmaTagger(language=languages.FRE)

    def count(self):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Statement) RETURN COUNT(s) AS count")
            return result.single()["count"]

    def remove(self, statement_text):
        with self.driver.session() as session:
            session.run("MATCH (s:Statement {text: $text}) DETACH DELETE s", text=statement_text)

    def filter(self, **kwargs):
        with self.driver.session() as session:
            return session.read_transaction(self._filter_statements, **kwargs)

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

    def create(self, **kwargs):
        with self.driver.session() as session:
            statement = kwargs.get('text', '')
            response = kwargs.get('response', None)
            session.write_transaction(self._create_statement, statement, response)

    @staticmethod
    def _create_statement(tx, statement, response):
        query = (
            "CREATE (s:Statement {text: $text, response: $response}) "
            "RETURN s"
        )
        tx.run(query, text=statement, response=response)

    def drop(self):
        with self.driver.session() as session:
            session.write_transaction(self._drop_database)

    @staticmethod
    def _drop_database(tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)



from chatterbot.storage.neo4j_storage import Neo4jStorageAdapter as ChatterbotNeo4jStorageAdapter
from chatterbot.storage import StorageAdapterCypher
from chatterbot.conversation import Statement
from neo4j import GraphDatabase

class Neo4jStorageAdapter(StorageAdapterCypher):
    def __init__(self, uri, user, password):
        super().__init__()
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

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

    # Implémentez d'autres méthodes comme retrieve, update, delete, filter, etc. en utilisant des requêtes Cypher

# Exemple d'utilisation
uri = "bolt://localhost:7687"  # Changez ceci avec votre URI Neo4j
user = "neo4j"  # Changez ceci avec votre nom d'utilisateur Neo4j
password = "powerslave666"  # Changez ceci avec votre mot de passe Neo4j

neo4j_adapter = Neo4jStorageAdapter(uri, user, password)

# Maintenant, vous pouvez utiliser ChatterBot avec votre adaptateur de stockage Neo4j
from chatterbot import ChatBot

chatbot = ChatBot('Neo4jBot', storage_adapter='Neo4jStorageAdapter')

# Entraînez le chatbot ou continuez avec d'autres opérations


from neo4j_storage import Neo4jStorageAdapter
from chatterbot.storage import StorageAdapterCypher
from chatterbot.conversation import Statement
from neo4j import GraphDatabase

class Neo4jStorageAdapter(StorageAdapterCypher):
    def __init__(self, uri, user, password):
        super().__init__(uri, user, password)  # Passer les arguments à la classe parente

# Example usage
uri = "bolt://localhost:7687"  # Change this to your Neo4j URI
user = "neo4j"  # Change this to your Neo4j username
password = "powerslave666"  # Change this to your Neo4j password

neo4j_adapter = Neo4jStorageAdapter(uri, user, password)

# Now you can use ChatterBot with your Neo4j storage adapter
from chatterbot import ChatBot

chatbot = ChatBot('Neo4jBot', storage_adapter='Neo4jStorageAdapter')

# Train the chatbot or continue with other operations


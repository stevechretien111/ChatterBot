# exemple.py

from chatterbot import ChatBot
from neo4j_adapter import Neo4jAdapter

chatbot = ChatBot(
    "My Bot", 
    storage_adapter=Neo4jAdapter()
)

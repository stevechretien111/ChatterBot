from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from neo4j_storage import Neo4jStorageAdapter

# Initialisation du ChatBot avec l'adaptateur Neo4j
chatbot = ChatBot('Neo4jBot')

# Ajoutez directement l'adaptateur de stockage à l'objet ChatBot
chatbot.storage = Neo4jStorageAdapter(
    uri = "bolt://localhost:7687/chatterbot"
user = "neo4j"
password = "powerslave666"
adapter = Neo4jStorageAdapter(uri, user, password)
)

# Initialisation du formateur du corpus français
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.french')

# Boucle de chat
while True:
    user_input = input("Vous: ")

    if user_input.lower() == 'exit':
        break

    response = chatbot.get_response(user_input)
    print("Neo4jBot:", response)


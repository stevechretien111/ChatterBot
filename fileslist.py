import os

def lister_fichiers_et_contenu(chemin, fichier_sortie):
    with open(fichier_sortie, 'w', encoding='utf-8') as output_file:
        for dossier_parent, sous_repertoires, fichiers in os.walk(chemin):
            output_file.write(f'Dossier : {dossier_parent}\n')

            for fichier in fichiers:
                chemin_fichier = os.path.join(dossier_parent, fichier)
                output_file.write(f'\tFichier : {fichier}\n')

                with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                    contenu = f.read()
                    output_file.write(f'\tContenu :\n{contenu}\n\n')

# Remplacez '/chemin/vers/le/repertoire' par le chemin absolu de votre répertoire cible
chemin_repertoire = '/home/steve/miniforge3/envs/chatterbot/lib/python3.8/site-packages/chatterbot'
fichier_sortie = 'fileslist.txt'
lister_fichiers_et_contenu(chemin_repertoire, fichier_sortie)

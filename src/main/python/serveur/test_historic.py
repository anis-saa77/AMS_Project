from pdf import create_pdf
messages = []

messages.append("Salut !")
messages.append("Salut ! Comment puis-je vous aider aujourd'hui ?")

messages.append("Comment vas tu ?")
messages.append("Je vais bien, merci ! Je suis un robot, donc je n'ai pas de sentiments ou d'émotions comme les humains, mais je suis prêt à discuter et à vous aider si vous avez besoin de quelque chose. Et vous, comment allez-vous ?")

messages.append("Raconte moi une histoire.")
messages.append("Bien sûr ! Voici une histoire que je vais vous raconter :\nIl était une fois, dans un petit village niché au cœur d'une forêt dense, un jeune garçon nommé  Léo. Léo était un enfant curieux et aventurier, qui aimait explorer les bois et découvrir leurs secrets.\nUn jour, tandis qu'il se promenait dans la forêt, Léo tomba sur un petit lac caché derrière un rideau de feuilles. Le lac était si calme et si clair que Léo put voir son propre reflet dans l'eau. Soudain, il aperçut une forme qui se déplaçait sous la surface de l'eau.\nLéo s'approcha du bord du lac et vit que c'était une petite sirène qui nageait vers lui. La sirène avait des cheveux verts et des yeux bleus, et elle souriait à Léo. Elle lui dit que son nom était Calypso et qu'elle était la gardienne du lac.\nCalypso expliqua à Léo que le lac était magique et que ses eaux avaient le pouvoir de guérir les blessures et de rendre les gens heureux. Mais elle ajouta que le lac était en danger, car un sorcier malveillant avait jeté un sort pour assécher les eaux.\nLéo, qui était un garçon courageux, décida de aider Calypso à briser le sort et à sauver le lac. Ensemble, ils entreprirent un voyage périlleux à travers la forêt, affrontant des créatures fantastiques et des obstacles sur leur chemin.\nFinalement, ils arrivèrent au château du sorcier et découvrirent que le sort était lié à un cristal magique. Léo et Calypso réussirent à détruire le cristal et à briser le sort, ce qui permit au lac de retrouver son eau et sa magie.\nLe village fut sauvé et les habitants furent reconnaissants envers Léo et Calypso. Le jeune garçon et la sirène devinrent les meilleurs amis et explorèrent ensemble es secrets de la forêt et du lac. Et ils vécurent heureux pour toujours.\nVoilà, j'espère que vous avez aimé l'histoire ")

messages.append("Salut je m'appelle Grégoire je suis en train de travailler sur un projet on a MS projet 1 et je suis en train de faire un test de longueur de texte")
messages.append("Bonjour Grégoire ! Comment puis-je vous aider aujourd'hui ? Vous avez besoin d'aide pour votre projet ou pour MS Project 1 ? Ou est-ce que vous voulez simplement discuter de votre test de longueur de texte ?")

print(messages)
create_pdf(messages)
print("Done !")
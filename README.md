Planning Advents - Ruben Pain
-

Lire les commentaires mi-anglais mi-français (oui j'ai eu la flemme à la fin).

Petit résumé parce que je suis sympa en attendant 
que je trouve une alternative plus jolie à la sortie csv.

Le fichier `Detection_Shape.py` sert à deux choses principales :
 - Trouver les lignes verticales et donc les colonnes du tableau
 - Trouver la position, le type et la couleur des formes (ceci reste à 
 optimiser un peu je pense, mais est fonctionnel)

Le fichier `API_azure.py` contient les fonctions de l'API d'Azure :
 - Il trouve les mots manuscrits présents dans l'image et leurs positions

Le fichier `main.py` est le corps du programme :
 - Il récupère les données des autres fichiers
 - Il nettoye les données afin de les préparer pour les traiter
 - Il traite ces données afin de les recouper pour trouver quelle forme va avec quel texte et à quelle date
 - Il écrit dans le csv les données souhaitées
 
 Le fichier `executable.py` contient la petite inteface graphique, une fenêtre, 4 champs :
  - Un label (uniquement à titre indicatif)
  - Un input pour récupérer le nom du fichier csv de sortie souhaité à transmettre au main.py
  - Un bouton pour upload qui ouvre un explorateur de fichier, afin de choisir l'image que l'on veut analyser pour la transmettre au main.py 
  - Un bouton pour quitter

La reconnaissance des caractères manuscrits n'est pas parfait, 81% sur ma photo test.
  
Instaurer des **règles d'or** pour le tableau sera quelque chose d'important :
 - Bien prendre la photo (cadrage, luminosité)
 - Bien placer les formes droites, éviter de les coller
 - ...

**PS :**
  _Wallah c'est moche et chiant à faire un README go faire des WATCHME (nouveau concept)_
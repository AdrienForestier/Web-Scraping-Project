Bonjour !
Ceci est le projet de Web Scraping d'Adrien Forestier & William Gainnier.

Concernant les fichiers, vous pouvez trouver les codes de scraping dans le dossier Scraper.
Il y a deux versions du projet. La première (streamlit_ski.py) est une version avec les données récoltées manuellement, qu'il faut donc téléchargere en local (attention à bien changer les path).
La deuxième version (streamlit_ski_with_cluster.py) est une version plus évoluée. Elle repose sur une instance AWS EC2. Cette dernière lance un script permettant de scrapper tous les jours les sites nécessaires au fonctionnement du streamlit. Ces données sont ensuite envoyées dans un cluster mongo, puis appellées dans le streamlit. Attention, ceci n'est valable que pour la deuxième partie, celle sur la météo.

Data :
Les fichiers des données scrappés sont trop volumineux nous avons donc mis en zip ces fichiers.
Si vous souhaitez exécuter le streamlit, veuillez télécharger les données ainsi que le code et changer le path du fichier dans le code localementpour avoir accès aux données.

Bon visionnage :)

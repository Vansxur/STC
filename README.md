Bienvenue, jeune développeur !

Tu as été assigné à cette mission car tu es le seul qualifié en "pentest"...
L'ancien développeur chargé de cette IHM a quitté son poste sans prévenir personne, et maintenant nous sommes bloqués car personne n'a le mot de passe pour l'application.
Plusieurs secrets sous la forme STC{UnExemple} sont cachés dans cette IHM, et ta tâche est de tous les retrouver.

Voici comment procéder :

Télécharge l'application : git clone https://github.com/Vansxur/STC
⚠️ Ne lis surtout pas le contenu des fichiers app.py, templates/ et database.db.
Vérifie également que ton port 5000 n'est pas en utilisation. 

Entre les commandes suivantes : 
chmod +x run.sh
./run.sh

Une fois la commande lancée, ne touche plus à ce terminal et ouvre en un autre. 
Ton IHM est prête à être attaquée à l'addresse 127.0.0.1:5000

Utilise Burp Suite : C'est ton outil favori pour analyser et intercepter les requêtes HTTP.
Outil utile : L'ancien développeur a laissé un script nommé md5crack.py, tu pourrai peut-être t'en servir...

Informations supplémentaires :
Nom d'utilisateur et mot de passe : On sait que les informations de connexion (nom d'utilisateur et mot de passe) se trouvent dans les fichiers Username et Password.

Important : Certaines fonctionnalités de l'application peuvent mettre un peu de temps à répondre, donc ne t'inquiète pas, c'est normal.

N'oublie pas de rapporter les 4 flags ! Nous comptons sur toi pour mener à bien cette mission.

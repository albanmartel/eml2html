# eml2html
Generateur de page html à partir d'un fichier courriel local 

Script python pour afficher dans le navigateur par défaut un email à partir d'un email sous forme de fichier

2 Paramètres sont nécessaires : 
  - i/--input le chemin absolu vers le fichier courriel
  - -d/--directory le chemin absolu vers le répertoire de travail où sera stocké la page html généré ainsi que les pièces jointes sauvegardées en local

0. Ouverture du fichier de courriel
1. Récupération des entêtes du courriel et décodage
2. Générer un code html pour les entêtes seules les plus importantes sont affichées
3. Analyse du corps du courriel et décodage de chaque partie sauf les pièces jointes
4. Généré un code html si aucune partie text/html à partir du code text/plain n'est pas présente dans le courriel
5. Ajouter l'information sur les pièces jointes dans le code html pour voir leurs noms et les voir.
6. Enregistrer temporairement les pièces jointes dans un dossier temporaire
7. Assembler les différentes pages html pour en faire une seule
8. afficher la page index.html dans le navigateur par défaut

Dépendances python : tous les modules utilisés font partie des librairies standards

ce script peut se coupler à mutt(logiciel linux messagerie terminal) via une macro dans muttrc

--------------------------------------------------

HTML page generator from a local email file

Python script to display an email from a file as an HTML page in the default browser

2 parameters are required:

i/--input the absolute path to the email file
-d/--directory the absolute path to the working directory where the generated HTML page and saved attachments will be stored
Open the email file
Retrieve and decode the email headers
Generate HTML code for the headers, only the most important ones are displayed
Analyze the email body and decode each part except the attachments
Generate HTML code if no text/html part is present in the email, using the text/plain part
Add information about attachments to the HTML code to display their names and allow viewing
Temporarily save attachments in a temporary folder
Assemble the different HTML pages into a single one
Display the index.html page in the default browser
Python dependencies: all modules used are part of the standard library

This script can be coupled with mutt (Linux terminal email client) via a macro in muttrc"

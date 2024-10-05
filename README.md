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

# Installation sous GNU/Linux

$ git clone https://github.com/albanmartel/eml2html.git

$ cd eml2html

eml2html$ sudo make install

# Désinstaller sous GNU/Linux

$ cd eml2html
eml2html$ sudo make uninstall

# Modifier le code existant puis déployer 

$ cd eml2html

eml2html$ sudo make uninstall

eml2html$ vim email2html.py

eml2html$ sudo make install

# Coupler email2html avec mutt

Ajouter la ligne suivante dans .muttrc (le fichier de configuration de mutt)

macro index,pager <F12> "<pipe-message>cat > $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml<enter><shell-escape>email2html.sh -i $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml -d $HOME/Courriel/Mutt/mutt.tmp/<enter>" "Voir l'email dans votre navigateur web"

La touche F12 peut aussi bien être remplacée par une autre touche où combinaison de touche

La logique de la macro est la suivante enregistre l'email courant quand j'appuie sur la touche F12 dans $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml Appuyer sur la touche enter puis exécuter le script <shell-escape>email2html.sh -i $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml -d $HOME/Courriel/Mutt/mutt.tmp/ si tout est bien configurer le navigateur par défaut s'ouvre et affiche l'email courant sous forme d'une page index.html locale.


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

This script can be coupled with mutt (Linux terminal email client) via a macro in muttrc


# Installation under GNU/Linux

$ git clone https://github.com/albanmartel/eml2html.git

$ cd eml2html

eml2html$ sudo make install

# Uninstallation under GNU/Linux

$ cd eml2html

eml2html$ sudo make uninstall

# Modify existing code and deploy

$ cd eml2html

eml2html$ sudo make uninstall

eml2html$ vim email2html.py

eml2html$ sudo make install

# Coupling email2html with Mutt

Add the following line to your .muttrc (Mutt configuration file)

macro index,pager <F12> "<pipe-message>cat > $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml<enter><shell-escape>email2html.sh -i $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml -d $HOME/Courriel/Mutt/mutt.tmp/<enter>" "View email in web browser"

The F12 key can be replaced with any other key or key combination.

The logic of the macro is as follows: when you press F12, the current email is saved to $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml. Then, the script <shell-escape>email2html.sh -i $HOME/Courriel/Mutt/mutt.tmp/saved_email.eml -d $HOME/Courriel/Mutt/mutt.tmp/ is executed, which generates an HTML version of the email. If everything is configured correctly, your default web browser will open and display the email as a local index.html page.





import os
import sys
import shutil
import time
import argparse
import quopri
import base64
import binascii
from bs4 import BeautifulSoup
import email
import email.message
import email.parser
from email.parser import HeaderParser
from email.header import decode_header
import webbrowser


def lireContenuMail(email_file):
    """Lit le contenu d'un courriel à partir d'un fichier courriel.

    Args:
        email_file (str): Chemin vers le fichier courriel.

    Returns:
        str: Une chaine de caractères contenant les données brut du courriel,
               ou None si le fichier n'existe pas.

    Raises:
        OSError: Si une erreur survient lors de l'ouverture du fichier.
    """
    if not os.path.exists(email_file):
        print(f"Erreur : Le fichier courriel '{email_file}' n'existe pas.")
        return None
    with open(email_file, "r") as file:
        data = file.read()
    return data


def recupererEntetesMail(data):
    """Parse le contenu du courriel à partir d'une chaine de caractère
    imprime des clefs récupérées

    Args:
        data(str): Une chaine de caractères contenant les données brut du courriel

    Returns:
        headers(dict) : retourne un dictionnaire contenant tous les entêtes de mail
    """
    parser = HeaderParser()
    courrielparse = parser.parsestr(data)
    info_entetes = []

    headers = {}
    for key, value in courrielparse.items():
        decoded_value = ""
        for part, encoding in decode_header(value):
            if isinstance(part, bytes):
                part = part.decode(encoding or "utf-8", errors="replace")
            decoded_value += part
        headers[key] = decoded_value
        info_entetes.append(f"clef : {key} , valeur : {decoded_value}")

    traces = "\n+---------Entêtes courriel----Début---------+\n"
    traces += "\n".join(info_entetes)
    traces += "\n+---------Entêtes courriel----Fin----------+\n"

    print(traces)

    return headers


def entetes_en_html(data):
    """La fonction entetes_en_html est conçue pour extraire les en-têtes d'un email 
    et les convertir en code HTML afin de les afficher de manière structurée et lisible.

    Args:
        data: Une chaîne de caractères représentant le contenu brut de l'email.
    
    returns:
        (str)html_content: code html contenant les informations sur les entêtes 
    """
    headers = recupererEntetesMail(data)
    # Extraction des headers avec gestion des valeurs manquantes
    from_ = headers['From'] if 'From' in headers else 'N/A'
    to = headers['To'] if 'To' in headers else 'N/A'
    cc = headers['Cc'] if 'Cc' in headers else 'N/A'
    bcc = headers['Bcc'] if 'Bcc' in headers else 'N/A'
    subject = headers['Subject'] if 'Subject' in headers else 'N/A'
    date = headers['Date'] if 'Date' in headers else 'N/A'
    reply_to = headers['Reply-To'] if 'Reply-To' in headers else 'N/A'
    message_id = headers['Message-ID'] if 'Message-ID' in headers else 'N/A'
    # Générer code HTML des entêtes de mail
    html_content = f"""
        <p><strong>From:</strong> {from_}</p>\n
        <p><strong>To:</strong> {to}</p>\n
        <p><strong>Cc:</strong> {cc}</p>\n
        <p><strong>Bcc:</strong> {bcc}</p>\n
        <p><strong>Subject:</strong> {subject}</p>\n
        <p><strong>Date:</strong> {date}</p>\n
        <p><strong>Reply-To:</strong> {reply_to}</p>\n
        <p><strong>Message-ID:</strong> {message_id}</p>\n
    """

    return html_content


def generer_html_entete(data):
    """cette fonction fournit une base solide pour générer du code HTML 
    à partir des en-têtes d'un email. 
    Elle peut être personnalisée et améliorée en fonction des besoins spécifiques de l'application.

    Args:
        data: Une chaîne de caractères représentant le contenu brut de l'email.
    
    returns:
        (str)html_content: page html contenant les informations sur les entêtes 


    """
    # Générer le code HTML
    html_content = """
    <!DOCTYPE html>\n
    <html lang="fr">\n
    <head>\n
        <meta charset="UTF-8">\n
        <title>Courriel</title>\n
    </head>\n
    <body>\n
    """
    html_content += entetes_en_html(data)
    html_content += """
    </body>\n
    </html>\n
    """
    
    print("Génération entêtes html terminée !")
    return html_content


def fusion_pages_html(html_content_first, html_content_second):
    """
    La fonction fusion_pages_html est conçue pour combiner 
    le contenu de deux pages HTML en une seule page. 
    Elle effectue une fusion en ajoutant le contenu de la deuxième page 
    à la fin de la première page.

    Args:
        (str)html_content_first: Une chaine de caractères des données html de la première page
        (str)html_content_second: Une chaine de caractères des données html de la seconde page

    returns:
        (str)html: La page HTML fusionnée est formatée et retournée 
    """
    html = ""
    first_soup = BeautifulSoup(html_content_first, 'html.parser')
    if first_soup is None:
        print(f"first_soup est {first_soup}")
    second_soup = BeautifulSoup(html_content_second, 'html.parser')
    if second_soup is None:
        print(f"second_soup est {second_soup}")
    if first_soup.body is None:
        new_body = first_soup.new_tag('body')
        new_body.extend(first_soup)
        first_soup = BeautifulSoup(new_body.prettify(), 'html.parser')
    if second_soup.body is None:
        new_body = second_soup.new_tag('body')
        new_body.extend(second_soup)
        second_soup = BeautifulSoup(new_body.prettify(), 'html.parser')

    body_first = first_soup.body
    body_second = second_soup.body
    body_second_content = body_second.contents

    # Remplacer la balise <body> par une balise <div>
    print("Remplacer la balise <body> par une balise <div>")
    new_div = second_soup.new_tag('div')
    new_div.attrs = second_soup.body.attrs  # Copier les attributs du body
    new_div.extend(body_second_content)

    # Remplacer le body par le nouveau div
    body_second.replace_with(new_div)
    style_first = first_soup.find_all('style')
    style_second = first_soup.find_all('style')
    body_first.append(new_div)
    style_first.append(style_second)

    html = first_soup.prettify()
    print("Fusion des pages html terminée !")

    return html


def extrait_courriel(data):
    """Extraire et décoder le contenu texte, HTML et les pièces jointes d'un email.
    Gérer les formats d'emails simples et multiples.
    Fournir des messages de trace détaillés pour le débogage et l'analyse.

    Args:
        data: Une chaîne de caractères représentant le contenu brut de l'email.

    Returns:
        dict: Un dictionnaire contenant les éléments extraits de l'email :
            text_content: Le contenu texte brut de l'email.
            html_content: Le contenu HTML de l'email.
            attachments: Une liste de dictionnaires, chacun représentant une pièce jointe avec son nom et son contenu.
    """

    text_content = ""
    html_content = ""
    attachments = []
    corps_mail = {
        "text_content": text_content,
        "html_content": html_content,
        "attachments": attachments,
    }
    compteur_txt_plain_part = 0
    compteur_html_part = 0
    compteur_attachements_part = 0
    msg = email.message_from_string(data)
    if email.message.Message.is_multipart(msg):
        # Traitement spécifique pour les messages multipart
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                text_content += part.get_payload(decode=False)
                compteur_txt_plain_part += 1
            if content_type == "text/html":
                html_content += part.get_payload(decode=False)
                compteur_html_part += 1
            else:
                # if content_disposition and 'attachment' in content_disposition.lower():
                attachment_content = part.get_payload(decode=False)
                if attachment_content is not None:
                    attachment_name = part.get_filename()
                    if attachment_name is not None:
                        attachment = {}
                        attachment[attachment_name] = attachment_content
                        attachments.append(attachment)
                        compteur_attachements_part += 1
    else:
        # Traitement spécifique pour les messages simples
        content_type = msg.get_content_type()
        content = msg.get_payload(decode=True)
        # Extraire et décoder le corps txt
        if content_type == "text/plain":
            if type(content) is bytes:
                try:
                    text_content += content.decode("utf-8")
                except Exception as e:
                    print(f"Erreur décodage utf-8 text/plain")
                    try:
                        text_content += content.decode("latin-1")
                    except Exception as e:
                        print(f"Erreur décodage latin-1 text/plain")
            else:
                text_content += content
            compteur_txt_plain_part += 1
        # Extraire et décoder le corps html
        if content_type == "text/html":
            print(f"text/html not multipart : {content}")
            if type(content) is bytes:
                try:
                    html_content += content.decode("utf-8")
                except Exception as e:
                    print(f"Erreur décodage text/html")
                    try:
                        html_content += content.decode("latin-1")
                    except Exception as e:
                        print(f"Erreur décodage latin-1 text/html ")
            else:
                html_content += content
            compteur_html_part += 1

    corps_mail["text_content"] = text_content
    corps_mail["html_content"] = html_content
    corps_mail["attachments"] = attachments

    testMultipart = (
        "Le message est multipart"
        if email.message.Message.is_multipart(msg)
        else "Le message n'est pas multipart "
    )

    traces = "\n+---------Analyse courriel----Début--+\n"
    traces += testMultipart + "\n"
    traces += f"{compteur_txt_plain_part} partie(s) text/plain\n"
    traces += f"{compteur_html_part} partie(s) text/html\n"
    traces += f"{compteur_attachements_part} partie(s) pièce(s)-jointe(s)\n"
    traces += "+---------Analyse courriel----Fin---+\n"

    print(traces)

    return corps_mail


def decode_email_content(encoded_string, nom_contenu):
    """La fonction decode_email_content est conçue pour décoder le contenu d'un email 
    qui peut être encodé dans différents formats couramment utilisés dans les emails. 
    Elle vise à identifier le format d'encodage et à appliquer le décodage approprié 
    afin d'obtenir le contenu texte brut de l'email.

    Args:
        encoded_string: Une chaîne à décoder
        nom_contenu: permet de voir c'est un text/plain ou text/html que l'on décode

    Return:
        str: retourne la chaîne décodée, qui correspond au contenu texte brut de l'email.

    debug traces:
        La fonction imprime des messages de traces pour indiquer le succès ou l'échec de 
        chaque tentative de décodage. 
        Ces traces peuvent être utiles pour le débogage et l'analyse.
    """
    decoded_content = None
    echec64 = True
    echecQp = True
    echecBin = True
    echecLatin1 = True
    echecUTF8 = True
    echecAucunDecodage = True

    try:
        # Essayer de décoder en base64
        octets = base64.b64decode(encoded_string)
        decoded_content = octets.decode("utf-8")
        echec64 = False
    except Exception as e:
        print(f"Erreur décodage Base64 {nom_contenu}")

    if not decoded_content:
        try:
            # Essayer de décoder en Quoted-Printable
            octets = quopri.decodestring(encoded_string)
            decoded_content = octets.decode("utf-8")
            echecQp = False
        except Exception as e:
            print(f"Erreur décodage Quoted-Printable {nom_contenu}")

    if decoded_content is None:
        try: 
            # Essayer de décoder en binaire (supposant que c'est une chaîne d'octets)
            decoded_content = binascii.hexlify(encoded_string).decode('ascii')
            echecBin = False
        except Exception as e:
            print(f"Erreur décodage binaire {nom_contenu}")        
        if type(encoded_string) is bytes:
            try:
                decoded_content = encoded_string.decode("utf-8")
                echecUTF8 = False
            except Exception as e:
                print(f"Erreur décodage utf-8 {nom_contenu}")
                try:
                    decoded_content += encoded_string.decode("latin-1")
                    echecLatin1 = False
                except Exception as e:
                    print(f"Erreur décodage latin-1 {nom_contenu}")
        else:
            #Si les deux décodages précédents ont échoué
            # cela veut dire que c'est déjà de l'utf-8
            decoded_content = encoded_string
            echecAucunDecodage = False
        

    resultat_base64 = "Échec " if echec64 else "Réussi"
    resultat_QP = "Échec " if echecQp else "Réussi"
    resultat_UTF8 = "Échec " if echecUTF8 else "Réussi"
    resultat_Bin = "Échec " if echecBin else "Réussi"
    resultat_latin1 = "Échec " if echecLatin1 else "Réussi"
    resultat_aucunDecodage = "Échec " if echecAucunDecodage else "Réussi"

    traces = f"+--Décodage--{nom_contenu}-Début--+\n"
    traces += "|          Base 64 : " + resultat_base64 + "      |\n"
    traces += "+--------------------------------+\n"
    traces += "| Quoted-Printable : " + resultat_QP + "      |\n"
    traces += "+--------------------------------+\n"
    traces += "|          Binaire : " + resultat_Bin + "      |\n"
    traces += "+--------------------------------+\n"
    traces += "|          Latin-1 : " + resultat_latin1 + "      |\n"
    traces += "+--------------------------------+\n"
    traces += "|            utf-8 : " + resultat_UTF8 + "      |\n"
    traces += "+--------------------------------+\n"    
    traces += "|   Aucun decodage : " + resultat_aucunDecodage + "      |\n"
    traces += f"+--Décodage--{nom_contenu}-Fin----+\n"

    print(traces)

    return decoded_content


def decode_enleve_entitesnumerique(corps_courriel):
    """La fonction decode_enleve_entitesnumerique est conçue pour traiter un email 
    en décodant son contenu, en supprimant les entités numériques et 
    en restructurant le contenu pour une meilleure visualisation du code par un humain
    et un traitement ultérieur.

    args: 
        corps_courriel(dict) : dictionnaire du corps de mail (text/plain, text/html et pièces-jointes)

    Returns:
        dict: un dictionnaire contenant le contenu texte, le contenu HTML 
                    et la liste des pièces jointes, tous traités et formatés.
    
    Les étapes :
        1. Décodage du contenu
        2. Analyse du contenu html
        3. Traitement des pièces jointes
        4. Fusion du code texte avec l'info sur les pièces jointes
        5. Fusion du code de la page html avec les donnees des pièces jointes

    Notes :
        * Les entités numériques sont actuellement définies comme des séquences de chiffres.
        * La suppression des entités se fait en remplaçant les entités par des espaces.
        * La fonction suppose que le contenu HTML est bien formé.
    """
    
    text_content = ""
    html_content = ""
    attachments = []
    pieces_jointes = ""
    traces = ""
    corps_courriel_decode = {
        "text_content": text_content,
        "html_content": html_content,
        "attachments": attachments,
    }
    if corps_courriel["text_content"] != "":
        text_entites_numeriques = decode_email_content(
            corps_courriel["text_content"], "text_content"
        )
        corps_courriel_decode["text_content"] = BeautifulSoup(text_entites_numeriques, "html.parser").get_text()
        traces += "\n+----Texte Courriel---Début---------+\n"
        traces += corps_courriel_decode["text_content"]
        traces += "\n+----Texte Courriel---Fin-----------+\n"
    else:
        print("Le contenu text/plain du courriel est vide")
    if corps_courriel["html_content"] != "":
        html_entites_numeriques = decode_email_content(
            corps_courriel["html_content"], "html_content"
        )
        corps_courriel_decode['html_content'] = BeautifulSoup(html_entites_numeriques, 'html.parser').prettify()
        traces += "\n+----html Courriel---Début---------+\n"
        traces += corps_courriel_decode["html_content"]
        traces += "\n+----html Courriel---Fin-----------+\n"
    else:
        print("Le contenu text/html du courriel est vide")
    if corps_courriel["attachments"] != []:
        for colonne in corps_courriel["attachments"]:
            for nom_fichier_joint, contenuBase64_joint in colonne.items():
                attachments.append(nom_fichier_joint)
        pieces_jointes_txt = "\n\nPièces-jointes : \n-" + "\n-".join(attachments)
        liens_attachements = ""
        for lien in attachments:
            liens_attachements += f"<a href=\"attachments/{lien}\"> - {lien}</a><br/>\n"
        pieces_jointes_html = "<body>\n<p><a href=\"attachments\">Pièces-jointes:</a><br/>\n" + liens_attachements + "</p>\n</body>"
        corps_courriel_decode["text_content"] +=  pieces_jointes_txt
        html = fusion_pages_html(corps_courriel_decode['html_content'], pieces_jointes_html)
        corps_courriel_decode['html_content'] = html 
        corps_courriel_decode["attachments"] = corps_courriel["attachments"]
        traces += "\n+----Pièces-jointes---Début---------+\n"
        traces += pieces_jointes
        traces += "\n+----Pièces-jointes---Fin-----------+\n"

    print(traces)

    return corps_courriel_decode


def rassembler_contenu(email_file):
    """ la fonction rassembler_contenu est une fonction de haut niveau 
    qui orchestre le traitement d'un email. Elle offre une interface simple
    pour accéder aux différentes parties d'un email 
    et peut être utilisée comme point de départ pour 
    de nombreuses applications de traitement d'email.

    args: 
        email_file(str) : chemin absolu du fichier email à traiter

    Returns:
        dict: Un dictionnaire contenant les éléments extraits de l'email :
            headers(dict) : retourne un dictionnaire contenant tous les entêtes de mail
            text_content: Le contenu texte brut de l'email.
            html_content: Le contenu HTML de l'email.
            attachments: Une liste de dictionnaires, chacun représentant une pièce jointe avec son nom et son contenu.
    """
    data = lireContenuMail(email_file)
    print("Données courriel lues !")
    courriel = {}
    if data:
        headers = recupererEntetesMail(data)
        print("Entêtes courriel récupérées !")
        corps_courriel = extrait_courriel(data)
        print("Extraction parties courriel faite !")
        corps_courriel_decode = decode_enleve_entitesnumerique(corps_courriel)
        print("Courriel décodé !")
        courriel['headers'] = headers
        courriel['text_content'] = corps_courriel_decode['text_content']
        courriel['html_content'] = corps_courriel_decode['html_content']
        courriel['attachments'] = corps_courriel_decode["attachments"]
        
    return courriel


def local_attachements(email_file, dossier_sauvegarde):
    """La fonction local_attachements a pour objectif de télécharger
    et d'enregistrer localement les pièces jointes d'un email. 
    Elle prend en entrée le chemin vers un fichier email
    et le chemin d'un dossier de destination,
    et enregistre chaque pièce jointe dans un fichier distinct à l'intérieur de ce dossier.

    args: 
        email_file(str) : chemin absolu du fichier email à traiter
        dossier_sauvegarde(str) :  chemin absolu du dossier des pièces-jointes
    """
    #effacer le dernier dossiers des pièces jointes
    dossier_sauvegarde = os.path.join(dossier_sauvegarde, "attachments")
    try:
        shutil.rmtree(dossier_sauvegarde)
        print(f"Le répertoire {dossier_sauvegarde} a été supprimé.")
    except OSError as e:
        print(f"Erreur lors de la suppression du répertoire : {e}")
    
    try:
        os.makedirs(dossier_sauvegarde, exist_ok=True)
        print(f"Le répertoire {dossier_sauvegarde} a été créé avec succès.")
    except FileExistsError:
        print(f"Le répertoire {dossier_sauvegarde} existe déjà.")
    except PermissionError:
        print(f"Vous n'avez pas les permissions suffisantes pour créer le répertoire {dossier_sauvegarde}.")
    except OSError as e:
        print(f"Une erreur s'est produite lors de la création du répertoire : {e}")
    courriel = rassembler_contenu(email_file)
    if courriel["attachments"] != []:
        for colonne in courriel["attachments"]:
            for nom_fichier_joint, contenuBase64_joint in colonne.items():
                fichier_sauvegarde = os.path.join(dossier_sauvegarde, nom_fichier_joint)
                try:
                    with open (fichier_sauvegarde, 'wb') as file :
                        file.write(base64.b64decode(contenuBase64_joint))
                except FileNotFoundError:
                    print("Impossible de créer le fichier.")
                except PermissionError:
                    print("Vous n'avez pas les permissions suffisantes pour écrire dans ce fichier.")
                except Exception as e:
                    print(f"Une erreur inattendue s'est produite : {e}")


def preparer_html_final(email_file):
    """La fonction preparer_html_final a pour objectif
    de générer le code HTML complet d'un email à partir
    de ses différentes composantes (en-têtes, contenu texte, contenu HTML).
    Elle sert de point d'entrée pour obtenir 
    une représentation HTML complète et structurée d'un email,
    qui pourra ensuite être utilisée pour l'affichage,
    l'impression ou d'autres traitements.

    args: 
        email_file(str) : chemin absolu du fichier email à traiter

    returns:
        courriel(dict) : Dictionnaire où le code html est mis-à-jour
    """
    data = lireContenuMail(email_file)
    courriel = rassembler_contenu(email_file)
    html_entetes = generer_html_entete(data)

    if courriel['html_content'] == "":
        html_content = "<p>\n" + courriel['text_content'].replace("\n", "<br/>\n") + "</p>\n"
        courriel['html_content'] = fusion_pages_html(html_entetes, html_content)
    else:
        courriel['html_content'] = fusion_pages_html(html_entetes, courriel['html_content'])
    print(f"preparer_html_final : \n{courriel['html_content']}")

    return courriel


def sauvegarder_html(email_file, dossier_sauvegarde):
    """la fonction sauvegarder_html offre une solution complète
    pour transformer un email en une page HTML et l'ouvrir
    dans un navigateur. Elle peut être utilisée dans de nombreux scénarios
    où il est nécessaire d'avoir une représentation visuelle et interactive des emails.

    Utilise le navigateur par défaut du système pour afficher l'email sous forme html
    """
    local_attachements(email_file, dossier_sauvegarde)
    courriel = preparer_html_final(email_file)
    fichier_sauvegarde = os.path.join(dossier_sauvegarde, "index.html")
    #supprimer l'ancien fichier index.html
    try:
        os.remove(fichier_sauvegarde)
        print(f"Le fichier {fichier_sauvegarde} a été supprimé.")
    except FileNotFoundError:
        print(f"Le fichier {fichier_sauvegarde} n'a pas été trouvé.")
    except PermissionError:
        print(f"Vous n'avez pas les permissions suffisantes pour supprimer {fichier_sauvegarde}.")

    try:
        with open (fichier_sauvegarde, 'w') as file :
            file.write(courriel['html_content'])
        #Affiche la page html dans le navigateur par défaut dans un nouvel onglet
        webbrowser.open(fichier_sauvegarde,new=0)
    except FileNotFoundError:
        print("Impossible de créer le fichier.")
    except PermissionError:
        print("Vous n'avez pas les permissions suffisantes pour écrire dans ce fichier.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")


def main():
    """La fonction main() sert de point d'entrée principal de l'application. Elle a pour objectif de :
    - Parser les arguments en ligne de commande: 
        Elle utilise le module argparse pour analyser 
        les arguments fournis par l'utilisateur lors de l'exécution du script.
    - Vérifier la validité des arguments: 
        Elle vérifie si les fichiers et les répertoires spécifiés par l'utilisateur existent.
    - Appeler les fonctions de traitement: 
        Elle appelle les fonctions rassembler_contenu et sauvegarder_html
        pour traiter le fichier email et générer la page HTML.
    - Mesurer le temps d'exécution: 
        Elle calcule le temps d'exécution du script.
    """
    start_time = time.time()
    parser = argparse.ArgumentParser(
        description="Afficher les headers récupérés à partir d'un fichier courriel avec du python."
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        help="fichier de configuration courriel à Analyser",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        required=False,
        help="dossier de travail où index.html sera généré et les pièces jointes sauvegardées",
    )
    args = parser.parse_args()

    if args.input:
        # Vérification de l'existence du fichier courriel
        if not os.path.exists(args.input):
            print(f"Erreur : Le fichier courriel/email '{args.input}' n'existe pas.")
            sys.exit(1)
    else:
        print(
            "Veuillez spécifier un fichier courriel/email en entrée avec l'option -i ou --input."
        )
    if args.directory:
        # Vérification de l'existence du dossier de travail
        if not os.path.exists(args.directory):
            print(f"Erreur : Le repertoire de travail '{args.directory}' n'existe pas.")
            sys.exit(1)
    else:
        print(
            "Veuillez spécifier un dossier de travail avec l'option -d ou --directory."
        )
    # Message sur les données
    print(f" Fichier courriel/mail : {args.input}")
    print(f"    Dossier de travail : {args.directory}")
    #rassembler_contenu(args.input)
    sauvegarder_html(args.input, args.directory)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Le script s'est exécuté en : {execution_time:.5f} secondes")

if __name__ == "__main__":
    main()

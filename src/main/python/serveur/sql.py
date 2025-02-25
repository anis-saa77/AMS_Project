import sqlite3

def getAidKeywords(cur, aid_name):
    # Vérifier si l'aide sociale existe
    check_query = "SELECT id FROM SocialAid WHERE name = ?;"
    cur.execute(check_query, (aid_name,))
    aid_exists = cur.fetchone()  # Récupère la première ligne correspondante

    if not aid_exists:
        # Fermer la connexion et lever une exception si l'aide sociale n'existe pas
        raise ValueError(f"L'aide sociale '{aid_name}' n'existe pas dans la base de données.")

    # Requête SQL pour récupérer les mots-clés associés à l'aide sociale
    query = '''
    SELECT Keyword.word
    FROM SocialAid
    JOIN SocialAid_Keyword ON SocialAid.id = SocialAid_Keyword.social_aid_id
    JOIN Keyword ON SocialAid_Keyword.keyword_id = Keyword.id
    WHERE SocialAid.name = ?;
    '''

    cur.execute(query, (aid_name,))
    keywords = [row[0] for row in cur.fetchall()]

    # Fermeture de la connexion
    #connection.close()
    return keywords

def getAids(cur):
    query = '''
        SELECT SocialAid.name
        FROM SocialAid
        ORDER BY SocialAid.id ASC;
        '''

    cur.execute(query)
    aids = [row[0] for row in cur.fetchall()]
    return aids

def getAidInfo(cur, aid_name):
    # Vérifier si l'aide sociale existe
    check_query = "SELECT id FROM SocialAid WHERE name = ?;"
    cur.execute(check_query, (aid_name,))
    aid_exists = cur.fetchone()  # Récupère la première ligne correspondante

    if not aid_exists:
        raise ValueError(f"L'aide sociale '{aid_name}' n'existe pas dans la base de données.")

    query = '''
       SELECT SocialAid.description
       FROM SocialAid
       WHERE SocialAid.name = ?;
       '''
    cur.execute(query, (aid_name,))
    info = cur.fetchone()
    return info

def getAidImage(cur, aid_name):
    # Vérifier si l'aide sociale existe
    check_query = "SELECT id FROM SocialAid WHERE name = ?;"
    cur.execute(check_query, (aid_name,))
    aid_exists = cur.fetchone()  # Récupère la première ligne correspondante

    if not aid_exists:
        raise ValueError(f"L'aide sociale '{aid_name}' n'existe pas dans la base de données.")

    query = '''
       SELECT SocialAid.image
       FROM SocialAid
       WHERE SocialAid.name = ?;
       '''
    cur.execute(query, (aid_name,))
    info = cur.fetchone()
    return info







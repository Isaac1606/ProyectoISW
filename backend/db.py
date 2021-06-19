from uuid import uuid4
from random import randint
import psycopg2
import yagmail

# host = "localhost"
# user = "postgres"
# password = "hola123"

database = "test_isw"
host = "localhost"
user = "postgres"
password = "admin"
port = 5432


def connect():
    try:
        connection = psycopg2.connect( database= database, host = host, user = user, password = password )
        return connection
    except :
        return None

def validateToken(token):
    connection = connect()
    if connection is None:
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM tokens WHERE token='{token}'")
        ans = cur.fetchone()
        return ans
    except :
        return None

def createUser(userRequest):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM usuarios WHERE correo='{userRequest['email']}'")
        user = cur.fetchone()
        if user is not None :
            cur.close()
            connection.close()
            return None
        correo = userRequest['email']
        password = userRequest['password']
        nombre = userRequest['name'].encode()
        nombre = nombre.decode()
        fecha_nac = userRequest['birthday']
        sexo = userRequest['sex']
        peso = userRequest['weight']
        estatura = userRequest['height']
        id_ts = getBloodID(userRequest['blood'])
        id_tp = getSkinID(userRequest['skin'])
        cur.execute(f"INSERT INTO usuarios (correo,password,nombre,fecha_nac,sexo,peso,estatura,id_tiposangre,id_tipopiel) VALUES ('{correo}','{password}','{nombre}','{fecha_nac}','{sexo}','{peso}','{estatura}','{id_ts}','{id_tp}')")
        connection.commit()
        new_token = False
        while new_token is False :
            print("while")
            token = str(uuid4())
            cur.execute(f"SELECT * FROM tokens WHERE token='{token}'")
            ans = cur.fetchone()
            if ans is None :
                new_token = True
        print("after while")
        cur.execute(f"SELECT * FROM usuarios WHERE correo='{correo}'")
        ans = cur.fetchone()
        id_usuario = ans[0]
        cur.execute(f"INSERT INTO tokens (token,id_usuario) VALUES ('{token}','{id_usuario}')")
        connection.commit()
        cur.close()
        connection.close()
        return token
    except :
        return None

def getSkinID(skin):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM tipo_piel WHERE desc_tipopiel='{skin}'")
        ans = cur.fetchone()
        return ans[0]
    except :
        return None

def getBloodID(blood):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM tipo_sangre WHERE desc_tiposangre='{blood}'")
        ans = cur.fetchone()
        return ans[0]
    except :
        return None

def getAllergyID(allergy):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM alergias WHERE desc_alergia='{allergy}'")
        ans = cur.fetchone()
        return ans[0]
    except :
        return None

def updateUser(userRequest):
    connection = connect()
    if connection is None :
        return False
    try :
        cur = connection.cursor()
        token = validateToken(userRequest["token"])
        if token is None :
            cur.close()
            connection.close()
            return False
        user = token[1]
        nombre = userRequest['name'].encode()
        nombre = nombre.decode()
        fecha_nac = userRequest['birthday']
        sexo = userRequest['sex']
        peso = userRequest['weight']
        estatura = userRequest['height']
        id_ts = getBloodID(userRequest['blood'])
        id_tp = getSkinID(userRequest['skin'])
        cur.execute(f"UPDATE usuarios SET nombre='{nombre}', fecha_nac='{fecha_nac}', sexo='{sexo}', peso='{peso}', estatura='{estatura}', id_tiposangre='{id_ts}', id_tipopiel='{id_tp}' WHERE id_usuario='{user}'")
        connection.commit()
        cur.close()
        connection.close()
        return True
    except :
        return False

def getUser(id_user):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM usuarios WHERE id_usuario='{id_user}'")
        user = cur.fetchone()
        if user is None :
            return None
        userResponse = {
            "name" : user[3],
            "email" : user[1],
            "birthday" : user[4],
            "sex" : user[5],
            "height" : user[7],
            "weight" : user[6],
            "skin" : "1",
            "blood" : "1"
        }
        return userResponse
    except :
        return None

def getUserAllergies(id_user):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM usuario_alergia WHERE id_usuario='{id_user}' ORDER BY fecha_descubrimiento")
        ans = cur.fetchall()
        id_allergies = []
        for a in ans :
            id_allergies.append([a[1],a[2]])
        allergies = []
        num = 0 
        for id_allergy in id_allergies :
            cur.execute(f"SELECT * FROM alergias WHERE id_alergia='{id_allergy[0]}'")
            allergy = cur.fetchone()
            num += 1
            a_dict = {
                "id_alergia" : num,
                "fecha" : str(id_allergy[1]),
                "descripcion" : allergy[1]
            }
            allergies.append(a_dict)
        return allergies
    except :
        return None

def insertUserAllergy(userRequest):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        token = validateToken(userRequest["token"])
        if token is None :
            cur.close()
            connection.close()
            return None
        user = token[1]
        date = userRequest["date"]
        allergy = getAllergyID(userRequest["allergy"])
        cur.execute(f"INSERT INTO usuario_alergia (id_usuario,id_alergia,fecha_descubrimiento) VALUES ('{user}','{allergy}','{date}')")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def deleteUserAllergy(userRequest):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        token = validateToken(userRequest["token"])
        if token is None :
            cur.close()
            connection.close()
            return False
        user = token[1]
        allergy = getAllergyID(userRequest["allergy"])
        cur.execute(f"DELETE FROM usuario_alergia WHERE id_usuario='{user}' AND id_alergia='{allergy}'")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def getUserConsults(id_user):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM consultas WHERE id_usuario='{id_user}' ORDER BY fecha_consulta")
        ans = cur.fetchall()
        consults = []
        num = 0
        for a in ans :
            num += 1
            a_dict = {
                "id_consulta" : num,
                "id_db" : a[0],
                "fecha" : a[1],
                "descripcion" : a[2]
            }
            consults.append(a_dict)
        return consults
    except :
        return None

def insertUserConsult(userRequest):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        token = validateToken(userRequest["token"])
        if token is None :
            cur.close()
            connection.close()
            return None
        id_user = token[1]
        date = userRequest["date"]
        desc = userRequest["desc"]
        cur.execute(f"INSERT INTO consultas (fecha_consulta,desc_consulta,id_usuario) VALUES ('{date}','{desc}','{id_user}')")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def deleteUserConsult(userRequest):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        token = validateToken(userRequest["token"])
        if token is None :
            cur.close()
            connection.close()
            return False
        consulta = userRequest["id_consulta"]
        cur.execute(f"DELETE FROM consultas WHERE id_consulta='{consulta}'")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def checkCredentials(mail,password):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM usuarios WHERE correo='{mail}'")
        user = cur.fetchone()
        u_mail, u_password = user[1], user[2]
        if u_mail == mail and u_password == password :
            new_token = False
            while new_token is False :
                print("while")
                token = str(uuid4())
                cur.execute(f"SELECT * FROM tokens WHERE token='{token}'")
                ans = cur.fetchone()
                if ans is None :
                    new_token = True
            print("after while")
            id_usuario = user[0]
            print(f"INSERT INTO tokens (token,id_usuario) VALUES ('{token}','{id_usuario}')")
            cur.execute(f"INSERT INTO tokens (token,id_usuario) VALUES ('{token}','{id_usuario}')")
            print(234)
            connection.commit()
            cur.close()
            connection.close()
            return token
        cur.close()
        connection.close()
        return None
    except :
        return None

def deleteUserToken(token):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"DELETE FROM tokens WHERE token='{token}'")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def sendMail(email):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM usuarios WHERE correo='{email}'")
        user = cur.fetchone()
        if user is None :
            return None
        while True :
            token = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])
            cur.execute(f"SELECT * FROM mail_tokens WHERE token='{token}'")
            ans = cur.fetchone()
            if ans is None :
                break
        to = email
        subject = "Recuperación contraseña"
        contents = [
            f"Hola, {user[3]}, favor de ingresar el siguiente código para recuperar tu contraseña:",
            f"{token}",
            f"¿No has sido tú quien ha solicitado la contraseña? Haz caso omiso."
        ]
        sender_email = ""
        sender_password = ""
        yag = yagmail.SMTP(sender_email,sender_password)
        yag.send(to,subject, contents)

        id_user = user[0]
        cur.execute(f"INSERT INTO mail_tokens (token,id_usuario) VALUES ('{token}','{id_user}')")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def changePassword(token,password):
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM mail_tokens WHERE token='{token}'")
        ans = cur.fetchone()
        if ans is None :
            return None
        id_user = ans[1]
        cur.execute(f"UPDATE usuarios SET password='{password}' WHERE id_usuario='{id_user}'")
        cur.execute(f"DELETE FROM mail_tokens WHERE token='{token}'")
        connection.commit()
        cur.close()
        connection.close()
    except :
        return None

def getBloods():
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM tipo_sangre")
        bloods = cur.fetchall()
        if bloods is None :
            return None
        ans = []
        for blood in bloods :
            ans.append(blood[1])
        return ans
    except :
        return None

def getSkins():
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM tipo_piel")
        skins = cur.fetchall()
        if skins is None :
            return None
        ans = []
        for skin in skins :
            ans.append(skin[1])
        return ans
    except :
        return None

def getAllergies():
    connection = connect()
    if connection is None :
        return None
    try :
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM alergias")
        allergies = cur.fetchall()
        if allergies is None :
            return None
        ans = []
        for allergy in allergies :
            ans.append(allergy[1])
        return ans
    except :
        return None

def loadSkins():
    connection = connect()
    cur = connection.cursor()
    skins = [
        "I Piel blanca pálida",
        "II Piel clara",
        "III Piel blanca más oscura",
        "IV Piel de color marrón claro",
        "V Piel marrón",
        "VI Piel morena o negra"
    ]
    for skin in skins :
        skin = skin.encode()
        skin = skin.decode()
        cur.execute(f"INSERT INTO tipo_piel (desc_tipopiel) VALUES ('{skin}')")
    connection.commit()
    cur.close()
    connection.close()

def loadAllergies():
    connection = connect()
    cur = connection.cursor()
    allergies = [
        "Alergia a medicamentos",
        "Alergia a comidas",
        "Alergia a insectos",
        "Alergia a latex",
        "Alergia a mascotas",
        "Alergia a polen"
    ]
    for allergy in allergies :
        allergy = allergy.encode()
        allergy = allergy.decode()
        cur.execute(f"INSERT INTO alergias (desc_alergia) VALUES ('{allergy}')")
    connection.commit()
    cur.close()
    connection.close()
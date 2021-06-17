from uuid import uuid4
import psycopg2

host = "localhost"
user = "postgres"
password = "hola123"

def connect():
    try:
        connection = psycopg2.connect( host = host, user = user, password = password )
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
        print(1)
        cur = connection.cursor()
        print(userRequest['email'])
        cur.execute(f"SELECT * FROM usuarios WHERE correo='{userRequest['email']}'")
        user = cur.fetchone()
        print(1.5)
        if user is not None :
            cur.close()
            connection.close()
            return None
        print(2)
        correo = userRequest['email']
        password = userRequest['password']
        nombre = userRequest['name'].encode()
        nombre = nombre.decode()
        fecha_nac = userRequest['birthday']
        sexo = userRequest['sex']
        peso = userRequest['weight']
        estatura = userRequest['height']
        id_ts = userRequest['blood']
        id_tp = userRequest['skin']
        print(3)
        print(userRequest)
        print(nombre)
        cur.execute(f"INSERT INTO usuarios (correo,password,nombre,fecha_nac,sexo,peso,estatura,id_tiposangre,id_tipopiel) VALUES ('{correo}','{password}','{nombre}','{fecha_nac}','{sexo}','{peso}','{estatura}','{id_ts}','{id_tp}')")
        connection.commit()
        print(4)
        cur.execute(f"SELECT * FROM usuarios WHERE correo='{correo}'")
        print(5)
        token = str(uuid4())
        print(5.5)
        ans = cur.fetchone()
        id_usuario = ans[0]
        print(5.6)
        cur.execute(f"INSERT INTO tokens (token,id_usuario) VALUES ('{token}','{id_usuario}')")
        print(6)
        connection.commit()
        print(7)
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
            token = str(uuid4())
            id_usuario = user[0]
            cur.execute(f"INSERT INTO tokens (token,id_usuario) VALUES ('{token}','{id_usuario}')")
            connection.commit()
            cur.close()
            connection.close()
            return token
        cur.close()
        connection.close()
        return None
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

def loadskins():
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
        print(skin)
        skin = skin.encode()
        skin = skin.decode()
        cur.execute(f"INSERT INTO tipo_piel (desc_tipopiel) VALUES ('{skin}')")
    connection.commit()
    cur.close()
    connection.close()
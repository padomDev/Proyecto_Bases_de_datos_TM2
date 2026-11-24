from domines.security import *
from repositories.usuarios_repo import *
from repositories.preguntas_repo import *
from repositories.logs_repo import *

#   Acumulador de mensajes de error para retornar al usuario.
mensaje_error = []

#   Funcion que sirve para validar las credenciales ingresadas por el usuario para su registro.
def registro_service(
    usuario, 
    contraseña,
    confirm_contraseña,
    pregunta, 
    respuesta
    ):

    existe_usuario = buscar_usuario(usuario)

    #   Valida que el nombre de usuario no se encuentre ya registrado.
    if existe_usuario is not None:
        mensaje_error.append("Este nombnre de usuario ya esta registrado")

    #   Valida que el nombre de usuario tenga entre 6 y 50 caracteres.
    if len(usuario) < 6 or len(usuario) > 50:
        mensaje_error.append("      El nombre de usuario debe tener entre 6 caracteres y 50")

    #   Valida que el nomnre del usuario tenga al menos una letra mayuscula.
    if not any(letra.isupper() for letra in usuario):
        mensaje_error.append("El nomnre de usuairo debe contener al menos una letra mayuscula")

    #   Valida que el nombre del ususario tenga al menos un numero.
    if not any(letra.isdigit() for letra in usuario):
        mensaje_error.append("El nombre de usuario debe contener al menos un número")

    #   Valida que la contraseña tenga entre 6 y 50 caracteres.
    if len(contraseña) < 6 or len(contraseña) > 50:
        mensaje_error.append("La contraseña debe tener entre 6 caracteres y 50")
    
    #   Valida que las contraseñas coincidan.
    if contraseña != confirm_contraseña:
        mensaje_error.append("Las contraseñas no coinciden")
    
    #   Valida que la contraseña tenga al menos una letra mayuscula.
    if not any(letra.isupper() for letra in contraseña):
        mensaje_error.append("La contraseña debe contener al menos una letra mayuscula")

    #   Valida que la contraseña tenga al menos un numero.
    if not any(letra.isdigit() for letra in contraseña):
        mensaje_error.append("La contraseña debe contener al menos un número")

    #   Valida que la respuesta a la pregunta de ingreso sea correcta.
    if not verificar_respuesta_repo(pregunta["id"], respuesta):
        mensaje_error.append("Respuesta ingresada incorrecta")
    
    #   Evalua si existen menmsajes de error. Si existen, los retorna y limpia el registro de errores.
    if mensaje_error:
        errores = mensaje_error.copy()
        mensaje_error.clear()
        return errores
    #   Si no hay errores, registra el usuario. Guarda su contraseña hasheada con salt, el salt lo guarda para poder validar ingresos futuros.
    else:
        contraseña_hasheada = hash_casero_16_bytes(contraseña)
        id_usuario = registrar_usuario_repo(usuario, contraseña_hasheada[0], contraseña_hasheada[1])
        log_registro_repo(id_usuario)
        return True

#   Funcion para validar ingreso.
def login_service(
    usuario,
    contraseña,
    pregunta, 
    respuesta
    ):

    respuesta_verificada = verificar_respuesta_repo(pregunta["id"], respuesta)

    #   Evalua que la respuesta del captcha sea correcta
    if respuesta_verificada == 1:

    #   Busca el usuario en la lista de usuarios.
        usuario_db = buscar_usuario(usuario)

        #   Evalua si el usuario ingresado existe.
        if usuario_db is not None:

            #   Si existe, trae su contrasena hasheada de la base de datos
            hasheo_generado = hash_casero_16_bytes_login(contraseña, usuario_db['salt'])

            #   Evalua que ambas contraseñas sean iguales.
            if usuario_db["password_hash"] == hasheo_generado[0]:

                #   Si lo son, la funcion retorna "True".
                log_login_repo(usuario_db["id"])
                return True

            #   Si no son iguales carga mensaje de error en la lista de errores.
            else:
                mensaje_error.append("La contraseña ingresada no coincide, pruebe nuevamente")
        #   Si el nombre de usuario no conidie lo carga en la lista de errores.
        else:
            mensaje_error.append("El nombre de usuario es incorrecto")
    #   Si la respuesta es incorrecta la carga en la lista de errores.        
    else:
        mensaje_error.append("Respuesta ingresada incorrecta")

    #   Retorna la lista de errores.
    errores = mensaje_error.copy()
    mensaje_error.clear()
    return errores


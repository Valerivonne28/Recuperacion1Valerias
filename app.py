# Valeria Ivonne Gutierrez Martinez
# Recuperacion 1
# Importar los módulos Flask,jsonify,request,session,redirect y url,pymysql,bcrypt
 
from flask import Flask, jsonify, request, session, redirect, url_for,Blueprint
import pymysql
import bcrypt

# Crear la aplicacion con flask
app = Flask(__name__)

# Configuracion de una clave secreta y la base de datos en MySQL
app.secret_key = 'Valeria'
app.config['MYSQL_DATABASE_HOST'] = 'host.docker.internal' 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Valeria'
app.config['MYSQL_DATABASE_DB'] = 'valerecuperacion'


                        ###################### Microservicio de login y usuarios #########################

# Ruta para registrar un usuario usando el metodo POST
@app.route('/register', methods=['POST'])
def register():
     # Extrae los diferentes campos del objeto JSON que se envía en la solicitud HTTP
    datos = request.get_json()
    usuario = datos.get('usuario')
    password = datos.get('password')
    email = datos.get('email')  #Obtiene el valor
    nombre = datos.get('nombre')
    telefono = datos.get('telefono')
    municipio = datos.get('municipio')
    sexo = datos.get('sexo')
    edad = datos.get('edad')

    # Hash de la contraseña usando la biblioteca bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Conexión a la base de datos MySQL
    mysql = pymysql.connect(
        host=app.config['MYSQL_DATABASE_HOST'],
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        db=app.config['MYSQL_DATABASE_DB']
        )
    #crear un cursor para interactuar con una base de datos utilizando MySQL en Python
    cursor = mysql.cursor()

    #Para registrar
    #Ejecutar consulta SQL para registrar un nuevo usuario en la tabla
    cursor.execute(
        'INSERT INTO usuarios (usuario, password, email, nombre, telefono, municipio, sexo, edad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        (usuario, hashed_password, email, nombre, telefono, municipio, sexo, edad)
    )
    mysql.commit()   # Confirmar los cambios en la base de datos
    cursor.close()   # Cerrar el cursor
    mysql.close()    # Cerrar la conexión a la base de datos
    
    #Devuelve una respuesta JSON indicando que el usuario se registró correctamente
    return jsonify({'message': 'Usuario registrado correctamente'})

#########
#Para hacer el inicio de sesion con el metodo POST
@app.route('/login', methods=['POST'])
def login():
    # Obtener datos del JSON
    datos = request.get_json()
    email = datos.get('email')
    password = datos.get('password')

    # Conexión a la base de datos
    mysql = pymysql.connect(
        host=app.config['MYSQL_DATABASE_HOST'],
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        db=app.config['MYSQL_DATABASE_DB']
    )
    #Cursor para interactuar con una base de datos 
    cursor = mysql.cursor(pymysql.cursors.DictCursor)
    
    # Ejecutar una consulta para obtener los datos del usuario por su email
    cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
    usuario_data = cursor.fetchone()

    if usuario_data:
        # Obtener la contraseña almacenada del usuario
        stored_password = usuario_data['password']
        # Comparar la contraseña proporcionada con la contraseña almacenada en forma segura
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            session['logged_in'] = True
            return jsonify({'message': 'Inicio de sesión exitoso'})
        else:
            return jsonify({'error': 'La contraseña no coincide, intentalo nuevamente'}), 401
    else:
        return jsonify({'error': 'El email no está registrado en la base de datos'}), 404
    
##########  
## Actualizar la info de un usuario con el metodo PUT
@app.route('/update_user', methods=['PUT'])
def update_user():
    print("Se ha alcanzado la ruta /update_user")  # Mensaje de depuración
    datos = request.get_json() # Obtener los datos del JSON recibido
    print("Datos recibidos:", datos)  # Mensaje de depuración

   # Obtener los valores de los atributos del usuario desde el JSON
    email = datos.get('email')
    nombre = datos.get('nombre')
    telefono = datos.get('telefono')
    municipio = datos.get('municipio')
    sexo = datos.get('sexo')
    edad = datos.get('edad')

    # Establecer la conexión a la base de datos MySQL
    mysql = pymysql.connect(
        host=app.config['MYSQL_DATABASE_HOST'],
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        db=app.config['MYSQL_DATABASE_DB']
    )
    # Crear un cursor para interactuar con la base de datos
    cursor = mysql.cursor()
     # Ejecutar la consulta SQL para actualizar la información del usuario
    cursor.execute(
        'UPDATE usuarios SET nombre = %s, telefono = %s, municipio = %s, sexo = %s, edad = %s WHERE email = %s',
        (nombre, telefono, municipio, sexo, edad, email)
    )
    mysql.commit()  # Confirmar los cambios en la base de datos
    cursor.close()  # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    # Devolver una respuesta JSON indicando que la información del usuario se ha actualizado correctamente
    return jsonify({'message': 'Información de usuario actualizada correctamente'})

##########
## Eliminar usuario con metodo DELETE
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
     # Obtener los datos del JSON recibido
    datos = request.get_json()
    email = datos.get('email')

    # Establecer la conexión a la base de datos MySQL
    mysql = pymysql.connect(
        host=app.config['MYSQL_DATABASE_HOST'],
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        db=app.config['MYSQL_DATABASE_DB']
    )

    # Crear un cursor para interactuar con la base de datos
    cursor = mysql.cursor()
    # Ejecutar la consulta SQL para eliminar el usuario con el email proporcionado
    cursor.execute('DELETE FROM usuarios WHERE email = %s', (email,))
    mysql.commit()  # Confirmar los cambios en la base de datos
    cursor.close()  # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    # Devolver una respuesta JSON indicando que el usuario ha sido eliminado correctamente
    return jsonify({'message': 'Usuario eliminado correctamente'})


############
#Aqui se obtienen todos los usuarios desde la base de datos, usando el metodo GET
@app.route('/database', methods=['GET'])
def database():
    # Verificar si el usuario ha iniciado sesión
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))  # Redirigir al inicio de sesión si no se ha iniciado sesión

    # Configurar la conexión a la base de datos
    mysql = pymysql.connect(
        host=app.config['MYSQL_DATABASE_HOST'],
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        db=app.config['MYSQL_DATABASE_DB']
    )

    cursor = mysql.cursor(pymysql.cursors.DictCursor)  # Crear un cursor para interactuar con la base de datos
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()  # Obtener todos los registros de usuarios

   # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    mysql.close()

    # Devolver los registros de usuarios en formato JSON
    return jsonify(usuarios)  



#########MIcroservicio de productos#########
##Aqui se verifica si el usuario ha iniciado la sesion 
def check_login():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'No has iniciado sesión'}), 401
    
##Obtiene una conexion a la base de datos MySQL 
def get_mysql_connection():
    return pymysql.connect(
        host=app.config['MYSQL_DATABASE_HOST'],
        user=app.config['MYSQL_DATABASE_USER'],
        password=app.config['MYSQL_DATABASE_PASSWORD'],
        db=app.config['MYSQL_DATABASE_DB']
    )

#Crear un nuevo registro de producto usando el método POST
@app.route('/create_product', methods=['POST'])
def create_product():
    #Verifica si el usuario ha iniciado sesion
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))  # Redirigir al inicio de sesión si no se ha iniciado sesión
    datos = request.get_json()
    #Se obtienen los datos del producto desde JSON
    nombre = datos.get('nombre')
    precio_compra = datos.get('precio_compra')
    precio_venta = datos.get('precio_venta')
    descripcion = datos.get('descripcion')
    stock = datos.get('stock')
    valoracion = datos.get('valoracion')

    # Validar campos
    if not nombre or not precio_compra or not precio_venta or not descripcion or not stock or not valoracion:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

   #Conexion a la base de datos
    mysql = get_mysql_connection()
    cursor = mysql.cursor()

# Ejecutar una consulta para insertar el nuevo producto en la base de datos
    cursor.execute(
        'INSERT INTO productos (nombre, precio_compra, precio_venta, descripcion, stock, valoracion) VALUES (%s, %s, %s, %s, %s, %s)',
        (nombre, precio_compra, precio_venta, descripcion, stock, valoracion)
    )
    mysql.commit()  # Confirmar los cambios en la base de datos
    cursor.close()  # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    return jsonify({'message': 'Producto creado correctamente'})

#Actualizar los productos utilizando el metodo PUT 
@app.route('/update_product', methods=['PUT'])
def update_product():
    # Verifica si el usuario ha iniciado sesión
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))  # Redirigir al inicio de sesión si no se ha iniciado sesión

    data = request.get_json()
    # Obtener datos actualizados del producto desde la solicitud JSON
    product_id = data.get('id')
    new_name = data.get('nombre')
    new_precio_compra = data.get('precio_compra')
    new_precio_venta = data.get('precio_venta')
    new_descripcion = data.get('descripcion')
    new_stock = data.get('stock')
    new_valoracion = data.get('valoracion')

    # Obtener una conexión a la base de datos
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Ejecutar una consulta para actualizar el producto en la base de datos
    update_query = (
        "UPDATE productos "
        "SET nombre = %s, precio_compra = %s, precio_venta = %s, "
        "descripcion = %s, stock = %s, valoracion = %s "
        "WHERE id = %s"
    )
    cursor.execute(update_query, (new_name, new_precio_compra, new_precio_venta,
                                  new_descripcion, new_stock, new_valoracion, product_id))

    connection.commit()   # Confirmar los cambios en la base de datos
    cursor.close()        # Cerrar el cursor y la conexión a la base de datos
    connection.close()

    return jsonify({'message': 'Producto actualizado correctamente'})


#Eliminar producto que esta en la base de datos usando el metodo DELETE
@app.route('/delete_product', methods=['DELETE'])
def delete_product():
    # Verifica si el usuario ha iniciado sesión
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))  # Redirigir al inicio de sesión si no se ha iniciado sesión

    data = request.get_json()
   # Obtener el ID del producto a eliminar desde JSON
    product_id = data.get('id')

    # Obtener una conexión a la base de datos
    connection = get_mysql_connection()
    cursor = connection.cursor()

   # Ejecutar una consulta para eliminar el producto de la base de datos
    delete_query = "DELETE FROM productos WHERE id = %s"
    cursor.execute(delete_query, (product_id,))

    connection.commit()  # Confirmar los cambios en la base de datos
    cursor.close()       # Cerrar el cursor y la conexión a la base de datos
    connection.close()

    return jsonify({'message': 'Producto eliminado correctamente'})

#Ver todos los productos si solo el usuario inicia sesion, usando el metodo GET
@app.route('/get_all_products', methods=['GET'])
def get_all_products():
     # Verifica si el usuario ha iniciado sesión
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    # Obtener una conexión a la base de datos
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Ejecutar una consulta para obtener todos los productos de la base de datos
    select_query = "SELECT * FROM productos"
    cursor.execute(select_query)
    products = cursor.fetchall()

    cursor.close()       # Cerrar el cursor y la conexión a la base de datos
    connection.close()

    return jsonify(products)

                                           ####Microservicio de ventas####

###Crear venta usando metodo post 

@app.route('/create_sale', methods=['POST'])
def create_sale():
    datos = request.get_json()
     # Obtener los datos de la venta desde la solicitud JSON
    fecha_venta = datos.get('fecha_venta')
    cantidad = datos.get('cantidad')
    total = datos.get('total')
    producto_id = datos.get('producto_id')
    cliente_nombre = datos.get('cliente_nombre')
    cliente_email = datos.get('cliente_email')
    forma_pago = datos.get('forma_pago')
    direccion_entrega = datos.get('direccion_entrega')
    ciudad_entrega = datos.get('ciudad_entrega')
    estado_entrega = datos.get('estado_entrega')
    codigo_postal = datos.get('codigo_postal')

    # Obtener una conexión a la base de datos
    mysql = get_mysql_connection()
    cursor = mysql.cursor()

   # Ejecutar una consulta para insertar la nueva venta en la base de datos
    cursor.execute(
        'INSERT INTO ventas (fecha_venta, cantidad, total, producto_id, cliente_nombre, cliente_email, forma_pago, direccion_entrega, ciudad_entrega, estado_entrega, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (fecha_venta, cantidad, total, producto_id, cliente_nombre, cliente_email, forma_pago, direccion_entrega, ciudad_entrega, estado_entrega, codigo_postal)
    )
    mysql.commit()   # Confirmar los cambios en la base de datos
    cursor.close()   # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    return jsonify({'message': 'Venta creada correctamente'})

#Actualizar venta usando el metodo PUT 

@app.route('/update_sale', methods=['PUT'])
def update_sale():
    datos = request.get_json()
    venta_id = datos.get('venta_id')  # ID de la venta que deseas actualizar

    # Obtener los demás datos de la venta desde el JSON
    fecha_venta = datos.get('fecha_venta')
    cantidad = datos.get('cantidad')
    total = datos.get('total')
    producto_id = datos.get('producto_id')
    cliente_nombre = datos.get('cliente_nombre')
    cliente_email = datos.get('cliente_email')
    forma_pago = datos.get('forma_pago')
    direccion_entrega = datos.get('direccion_entrega')
    ciudad_entrega = datos.get('ciudad_entrega')
    estado_entrega = datos.get('estado_entrega')
    codigo_postal = datos.get('codigo_postal')

   # Obtener una conexión a la base de datos
    mysql = get_mysql_connection()
    cursor = mysql.cursor()

   # Ejecutar una consulta para actualizar la venta en la base de datos
    cursor.execute(
        'UPDATE ventas SET fecha_venta = %s, cantidad = %s, total = %s, producto_id = %s, cliente_nombre = %s, cliente_email = %s, forma_pago = %s, direccion_entrega = %s, ciudad_entrega = %s, estado_entrega = %s, codigo_postal = %s WHERE id = %s',
        (fecha_venta, cantidad, total, producto_id, cliente_nombre, cliente_email, forma_pago, direccion_entrega, ciudad_entrega, estado_entrega, codigo_postal, venta_id)
    )
    mysql.commit()  # Confirmar los cambios en la base de datos
    cursor.close()  # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    return jsonify({'message': 'Venta actualizada correctamente'})


#Borrar venta usando el metodo DELETE
@app.route('/delete_sale', methods=['DELETE'])
def delete_sale():
    producto_id = request.args.get('producto_id')

   # Obtener una conexión a la base de datos
    mysql = get_mysql_connection()
    cursor = mysql.cursor()

 # Ejecutar una consulta para eliminar la venta de la base de datos
    cursor.execute('DELETE FROM ventas WHERE producto_id = %s', (producto_id,))
    mysql.commit()   # Confirmar los cambios en la base de datos

    cursor.close()    # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    return jsonify({'message': 'Venta eliminada correctamente'})

#Conseguir todas las ventas usando el metodo GET 

@app.route('/get_all_sales', methods=['GET'])
def get_all_sales():
    mysql = get_mysql_connection()
    cursor = mysql.cursor()

 # Ejecutar una consulta para obtener todas las ventas de la base de datos
    cursor.execute('SELECT * FROM ventas')
    ventas = cursor.fetchall()

    cursor.close()   # Cerrar el cursor y la conexión a la base de datos
    mysql.close()

    return jsonify(ventas)


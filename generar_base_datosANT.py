import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
           host='GabrielCes.mysql.pythonanywhere-services.com',
           user='GabrielCes',
           password='LAGABONETA'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe un error en el nombre de usuario o en la clave')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `GabrielCes$PedidoEntrega`;")

cursor.execute("CREATE DATABASE `GabrielCes$PedidoEntrega`;")

cursor.execute("USE `GabrielCes$PedidoEntrega`;")

# creando las tablas
TABLES = {}

TABLES['productos'] = ('''
      CREATE TABLE `productos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `articulo` varchar(50) NOT NULL,
      `descripcion` varchar(100) NOT NULL,
      `precio_venta` decimal(9,2) NOT NULL,
      `stock_minimo` int(4) NOT NULL,
      `existencia` int(4) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nombre` varchar(40) NOT NULL,
      `usuario` varchar(20) NOT NULL,
      `clave` varchar(20) NOT NULL,
       `role` varchar(20) NOT NULL,
      `correo` varchar(80) NOT NULL,
      PRIMARY KEY (`usuario`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['clientes'] = ('''
      CREATE TABLE `clientes` (
      `codigo` varchar(20) NOT NULL,
      `nombre` varchar(100) NOT NULL,
      `fecha` date NOT NULL,
      `direccion` varchar(200) NOT NULL,
      `telefono` varchar(20) NOT NULL,
      `ciudad` varchar(50) NOT NULL,
      PRIMARY KEY (`codigo`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['pedidos'] = ('''
      CREATE TABLE `pedidos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `codigo_cliente` varchar(20) NOT NULL,
      `fecha` date NOT NULL,
      `total` decimal(10,2) NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (`codigo_cliente`) REFERENCES `clientes` (`codigo`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabla_nombre in TABLES:
      tabla_sql = TABLES[tabla_nombre]
      try:
            print('Creando tabla {}:'.format(tabla_nombre), end=' ')
            cursor.execute(tabla_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Ya existe la tabla')
            else:
                  print(err.msg)
      else:
            print('OK')


# insertando usuarios
usuario_sql = 'INSERT INTO usuarios (nombre, usuario, clave, role, correo) VALUES (%s, %s, %s, %s, %s)'

usuarios = [
      ("Jair Sampaio", "driver1", "driver1pass","driver","jair@gmail.com"),
      ("Rosa Flores", "driver2", "driver2pass","driver","rosa@gmail.com"),
      ("Yami Moto Nokamina", "driver3", "driver3pass","driver","yamimoto@gmail.com"),
      ("Mustafá ALi Babá", "seller1", "seller1pass","seller","mustafa@gmail.com"),
      ("Armando Meza", "seller2", "seller2pass","seller","ameza@gmail.com"),
      ("Teodoro Luque", "seller3", "seller3pass","seller","tluque@gmail.com"),
      ("Jacobo Zimermann", "manager1", "manager1pass","admin","jzimermann@gmail.com"),
      ("Lucrecio Pérez", "manager2", "manager2pass","admin","lperez@gmail.com")
]
cursor.executemany(usuario_sql, usuarios)


cursor.execute('select * from GabrielCes$PedidoEntrega.usuarios')
print(' -------------  Usuarios:  -------------')
for user in cursor.fetchall():
    print(user[0],user[1],user[2],user[3],user[4])



# insertando productos
productos_sql = 'INSERT INTO productos (articulo, descripcion, precio_venta, stock_minimo, existencia) VALUES (%s, %s, %s, %s, %s)'

productos = [
      ('mantequilla paquete grande', 'mantequilla paquete envase de 350 grs.', 20.00, 200, 1000),
      ('aceite de girasol', 'aceite girasol envase 1000 ml.', 15.0, 300, 1500),
      ('detergente ropa Suzzio', 'detergente ropa Suzzio 800 gr.',30.00, 24, 100),
      ('lava vajilla líquido Muggre 250 ml.', 'detergente ropa Suzzio 800 gr.',10.00, 24, 100),
      ('leche Vaka Loka', 'leche líquida Vaka Loka 800 ml.',8.00, 24, 100)
      ]
cursor.executemany(productos_sql, productos)

cursor.execute('select * from GabrielCes$PedidoEntrega.productos')
print(' -------------  Productoss:  -------------')
for producto in cursor.fetchall():
    print(producto[0],' ',producto[1],' ',producto[2] )

clientes = [
    # Datos de app.py y los nuevos que solicitaste
    ("CLI001", "Juan Pérez", "2024-06-01", "Av. Los Sauces # 345", "7777 7777", "Cochabamba"),
    ("CLID002", "María García", "2024-06-02", "Av. Los Sauces # 345", "7777 7777", "Cochabamba"),
    ("CLI003", "Carlos López", "2024-06-03", "Av. Los Sauces # 345", "7777 7777", "Cochabamba")
]
cursor.executemany(clientes_sql, clientes)

cursor.execute('select * from GabrielCes$PedidoEntrega.clientes')
print(' -------------  Clientes:  -------------')
for cli in cursor.fetchall():
    print(cli[0], cli[1], cli[2])

# commitando si no hay nada que tenga efecto
conn.commit()

cursor.close()
conn.close()
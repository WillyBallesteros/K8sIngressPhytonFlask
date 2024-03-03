# User Management

Microservicio para la gestión de usuarios y de acceso.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Estructura

La estructura del proyecto es la siguiente:
```
├── src # Esta carpeta con el código de la aplicación.
│   └── blueprints # Esta carpeta contiene la capa de aplicación del microservicio.
│   └── commands # Esta carpeta contiene los caso de uso implementados en el microservicio.
│   └── errors # Esta carpeta contiene las excepciones personalizadas del servicio.
│   └── models # Esta carpeta contiene la capa de persistencia.
│   └── utils # Esta carpeta contiene funciones auxiliares requeridas por los comandos.
├── tests # Esta carpeta contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`
├── `Pipfile`: Este archivo declara todas las dependencias que serán utilizadas por el microservicio. 
├── `.env.template`: Archivo de plantilla Env utilizado para definir variables de entorno. 
├── `.env.test`: Archivo utilizado para definir variables de entorno para las pruebas unitarias.
├── Dockerfile: Definición para construir la imagen Docker del microservicio.

```
## Ejecución
### Ejecución del servicio
Para correr dierectamente el servicio, se deben ejecutar los siguientes comandos:
```bash
$> pip install pipenv
$> pipenv install --dev
$> FLASK_APP=src/main.py pipenv run flask run -h 0.0.0.0 -p 3000
```
Para salir del entorno virtual, utiliza el siguiente comando:
```bash
$> deactivate
```
Para que la ejecución directa sea efectiva, debe tener declaradas las correspondientes variables de entorno en el archivo .env.development:
- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres

### Ejecución con Docker
Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:
```bash
$> docker build . -t <NOMBRE_DE_LA_IMAGEN>
```
Y para ejecutar esta imagen construida, utiliza el siguiente comando:
```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Uso
El microservicio debe consumirse como una api rest. Se recomienda utilizar postman para la prueba de la funcionalidad implementada. Las funciones disponibles son las siguientes:
- [Creación de usuarios](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Usuarios#1-creaci%C3%B3n-de-usuarios)
- [Actualización de usuarios](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Usuarios#2-actualizaci%C3%B3n-de-usuarios)
- [Generación de token](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Usuarios#3-generaci%C3%B3n-de-token)
- [Consultar información del usuario](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Usuarios#4-consultar-informaci%C3%B3n-del-usuario)
- [Consulta de salud del servicio](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Usuarios#5-consulta-de-salud-del-servicio)
- [Restablecer base de datos](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Usuarios#6-restablecer-base-de-datos)

## Pruebas

Las pruebas unitarias puede ejecutarse con los siguientes comandos:
```bash
$> pip install pipenv
$> pip install pipenv
$> pipenv install --dev
$> pipenv run pytest --cov=src -v -s --cov-fail-under=70 
```
Para salir del entorno virtual, utiliza el siguiente comando:
```bash
$> deactivate
```
También se puede ejecutar una batería de pruebas declaradas en postman en el archivo: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json en la carpeta Users


## Autor

Ricardo Nicolás Hüg


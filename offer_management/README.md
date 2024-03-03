# Offer Management

Microservicio para la de gestión de ofertas dentro de un entorno de desarrollo de aplicaciones en la nube.
Permite a los usuarios crear, buscar, eliminar y consultar ofertas.
Los usuarios pueden interactuar con el sistema utilizando tokens de autorización para realizar operaciones específicas, asegurando así la seguridad y la integridad de la información.
El sistema ofrece funcionalidades como la creación de ofertas, la posibilidad de filtrar ofertas con diferentes criterios.

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
$> FLASK_APP=src/main.py pipenv run flask run -h 0.0.0.0 -p 3003
```
Para salir del entorno virtual, utiliza el siguiente comando:
```bash
$> deactivate
```
Para que la ejecución directa funcione correctamente, es necesario que las variables de entorno pertinentes estén definidas en el archivo .env.development:
- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres

### Ejecución con Docker
Para crear la imagen desde el Dockerfile ubicado en la carpeta, utilice el siguiente comando:
```bash
$> docker build -t <NOMBRE_DE_LA_IMAGEN> .
```
Y para iniciar la imagen que se ha creado, emplee el siguiente comando:
```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Uso
El microservicio debe ser utilizado como una API REST. Se sugiere el uso de Postman para verificar la funcionalidad desarrollada. Las funciones disponibles se enumeran a continuación:
- [Creación de ofertas](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#1-creaci%C3%B3n-de-ofertas)
- [Ver y filtrar ofertas](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#2-ver-y-filtrar-ofertas)
- [Consultar una oferta](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#3-consultar-una-oferta)
- [Eliminar oferta](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#4-eliminar-oferta)
- [Consulta de salud del servicio](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#5-consulta-de-salud-del-servicio)
- [Restablecer base de datos](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#6-restablecer-base-de-datos)

## Pruebas

Las pruebas unitarias pueden llevarse a cabo mediante los siguientes comandos:
```bash
$> pip install pipenv
$> pip install pipenv
$> pipenv install --dev
$> pipenv run pytest --cov=src -v -s --cov-fail-under=70
```
Para salir del entorno virtual, ejecute el siguiente comando:
```bash
$> deactivate
```
Asimismo, es posible ejecutar un conjunto de pruebas definidas en Postman mediante el archivo: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json en la carpeta Offer


## Autor

Oscar Evelio Ramirez Blanco

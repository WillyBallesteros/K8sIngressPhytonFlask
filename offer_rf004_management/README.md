# Offer 004 Management

  

Microservicio para la de administración de creación de ofertas.
Valida que la publicación a la cual se desea realiar la oferta exista y que este vigente.
Valida que el usuario que desea realizar la oferta este registrado en el sistema y que sea un usuario diferente al que realizó el la publicación.
Valida que la ruta exista
Y crea el score en el sistema.

Implementa el patron Saga para la consistencia entre las transacciones y se apoya en una base de datos que tiene la tabla offercompensations.

Proporciona manejo de errores para asegurar que la información al finalizar sea consistente y para comunicar cualquier problema al usuario.

Los usuarios pueden interactuar con el sistema utilizando tokens de autorización para realizar operaciones específicas, asegurando así la seguridad y la integridad de la información.

  
  

## Índice

  

1. [Estructura](#estructura)

2. [Ejecución](#ejecución)

3. [Uso](#uso)

4. [Pruebas](#pruebas)

5. [Autor](#autor)

6. [Diseño Solución](#diseño_solución)

  
  

## Estructura

  

La estructura del proyecto es la siguiente:

```

├── src # Esta carpeta con el código de la aplicación.

│ └── blueprints # Esta carpeta contiene la capa de aplicación del microservicio.

│ └── commands # Esta carpeta contiene los caso de uso implementados en el microservicio.

│ └── errors # Esta carpeta contiene las excepciones personalizadas del servicio.

│ └── models # Esta carpeta contiene la capa de persistencia.

│ └── utils # Esta carpeta contiene funciones auxiliares requeridas por los comandos.

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

$>  pip  install  pipenv

$>  pipenv  install  --dev

$>  FLASK_APP=src/main.py  pipenv  run  flask  run  -h  0.0.0.0  -p  3013

```

Para salir del entorno virtual, utiliza el siguiente comando:

```bash

$>  deactivate

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

$>  docker  build  -t <NOMBRE_DE_LA_IMAGEN> .

```

Y para iniciar la imagen que se ha creado, emplee el siguiente comando:

```bash

$>  docker  run <NOMBRE_DE_LA_IMAGEN>

```

  

## Uso

El microservicio debe ser utilizado como una API REST. Se sugiere el uso de Postman para verificar la funcionalidad desarrollada. Las funciones disponibles se enumeran a continuación:

- [Creación de ofertas](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Creaci%C3%B3n-de-ofertas)

- [Consulta de salud del servicio](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202411/wiki/Gesti%C3%B3n-de-Ofertas#5-consulta-de-salud-del-servicio)

  

## Pruebas

  

Las pruebas unitarias pueden llevarse a cabo mediante los siguientes comandos:

```bash

$>  pip  install  pipenv

$>  pip  install  pipenv

$>  pipenv  install  --dev

$>  pipenv  run  pytest  --cov=src  -v  -s  --cov-fail-under=70

```

Para salir del entorno virtual, ejecute el siguiente comando:

```bash

$>  deactivate

```

  
  

## Autor

  

Oscar Evelio Ramírez Blanco

  

# Diseño de Solución para RF-004

  

## Modelo de Componentes

-  **User Service**: Gestiona la autenticación y la información de los usuarios.

-  **Post Service**: Administra las publicaciones existentes y sus detalles.

-  **Route Service**: Responsable de la gestión de trayectos.

-  **Score Service**: Responsable del calculo y almacenamiento de score.

-  **Offer_rf004 Service**: Encargado de la lógica de negocio para la creación de ofertas según el RF-004, interactuando con los servicios de Post, User, Score y Route para validar y crear los datos necesarios.

  

## Modelo de Despliegue

La solución está desplegada en un clúster de Kubernetes dentro de Google Cloud Platform, utilizando los siguientes elementos:

-  **Ingress**: Balanceador de carga que enruta las solicitudes a los microservicios correspondientes.

-  **Microservicios**: Conjunto de servicios desplegados como contenedores en el clúster, cada uno con su responsabilidad definida.

-  **SharedDB**: Base de datos centralizada utilizada por todos los servicios para operaciones CRUD.

  

## Patrones Utilizados

  

### Patrón Saga

El Patrón Saga es un mecanismo de diseño implementado en el servicio `Offer_rf004` para administrar transacciones que abarcan múltiples servicios y recursos, el Patrón Saga asegura que las operaciones distribuidas se ejecuten de manera consistente, a pesar de la naturaleza descentralizada y distribuida de los microservicios.

  

-  **Orquestación de Transacciones**: El `Offer_rf004` actúa como un coordinador que dirige el proceso de creación de publicaciones, orquestando llamadas a otros servicios y gestionando el flujo de transacciones.

-  **Compensaciones y Rollbacks**: En caso de fallas o errores durante la creación de una publicación o la asociación de rutas, el servicio `Offer_rf004` es responsable de ejecutar las acciones compensatorias necesarias para revertir los cambios y mantener la integridad del sistema.

-  **Estado de Transacciones**: Se mantiene un registro detallado del estado de cada transacción. Si una operación falla en cualquier punto, el sistema puede consultar este registro para determinar la acción compensatoria adecuada.

-  **Resiliencia**: El diseño proporcionado por el Patrón Saga permite al sistema tolerar fallos y seguir funcionando correctamente, garantizando que no se comprometa la consistencia de los datos.

  

Mediante la implementación de este patrón, el servicio `Offer_rf004` garantiza que todos los pasos involucrados en la creación de una publicación, desde la autenticación del usuario hasta la validación y creación de rutas, se manejen de forma atómica, ofreciendo una correcta experiencia de usuario y una base de datos siempre consistente.

  
  

## Flujo de Operaciones

1. El usuario inicia sesión y proporciona los datos de la publicación y la Oferta.

2. El servicio Offer_rf004 valida si la publicación existe.
3. Si la publicación existe, y se cumplen las reglas de negocio, se crea la oferta.
4. Con los datos recopilados se calcula el score.
5. La oferta se asocia al usuario de la sesión.

6. Se persisten los cambios en la base de datos.

  

## Validaciones

-  **Trayecto**: Existencia y unicidad.

-  **Fechas**: Verificación de que la fecha de inicio está en el futuro y la fecha de expiración es adecuada.

-  **Usuario**: Autenticación y autorización para la creación de publicaciones.
-  **Publicación**: Autenticación y autorización para la creación de publicaciones.

  

## Gestión de Errores

-  **Errores de Validación**: Mensajes claros y acciones de compensación si las validaciones fallan.

-  **Consistencia de Datos**: Uso del patrón Saga para garantizar que no haya estados inconsistentes a pesar de los errores que puedan ocurrir.

  

## Cumplimiento con Necesidades y Restricciones

- La solución cumple con las restricciones de autenticación de usuarios, validación de datos, y manejo de errores.

- La arquitectura permite la escalabilidad y fácil mantenimiento de los servicios.

  

## Diagramas Incluidos

-  **Diagrama de Componentes**: Visualiza la interacción entre los microservicios y la base de datos.
![ComponentModel](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo17/assets/124172912/74559d07-3c9e-4065-b7a2-e758807ed3a4)

-  **Diagrama de Despliegue**: Muestra cómo se despliegan los componentes en GCP y Kubernetes.
![DeploymentModel](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo17/assets/124172912/f3a00ae1-431c-4018-ab96-6bcf1d244f2b)


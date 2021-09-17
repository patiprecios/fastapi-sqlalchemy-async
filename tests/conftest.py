import pytest

DOCKER_DATABASES = {
    'postgres': {
        'image': 'postgres:13',
        'ports': {'3306': 3306},
        'environment': [
            'POSTGRES_USER=user',
            'POSTGRES_PASSWORD=password',
            'POSTGRES_DB=test'
        ],
    },
    'mysql': {
        'image': 'mysql:8',
        'ports': {'5432': 5432},
        'environment': [
            'MYSQL_USER=user',
            'MYSQL_ROOT_PASSWORD=password'
        ],
        'dsn': [

        ]
    }
}


def wait_for_startup(host, port):
    import socket
    import time

    # configure a socket to connect to db
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            st.connect((host, port))
            st.close()

            print('Database Ready')

            break
        except socket.error:
            time.sleep(0.5)


@pytest.fixture(scope='session')
def docker_client():
    ''' TODO '''
    import docker

    docker_client = docker.from_env()

    yield docker_client


@pytest.fixture(
    scope='session',
    ids=['postgres', 'mysql'],
    params=[
        {
            'database': 'postgres',
            'dsn': 'postgresql+asyncpg://user:password@localhost:5432/test'
        }, {
            'database': 'postgres',
            'dsn': 'postgresql+aiopg://user:password@localhost:5432/test'
        }
    ]
)
def docker_database(docker_client, request):
    ''' TODO '''
    database_config = DOCKER_DATABASES.get(request.param.get('database'))

    image = database_config.get('image')
    environment_vars = database_config.get('environment')

    ports = database_config.get('ports')
    main_port = next(iter(ports.values()))

    container = docker_client.containers.run(
        image,
        environment=environment_vars,
        ports=ports,
        detach=True
    )

    # use the first port
    wait_for_startup('localhost', main_port)

    # update status
    container.reload()

    yield container

    container.reload()

    if container.status in ('created', 'running'):
        container.stop()
        container.wait()


@pytest.fixture
def database_dsn(docker_database, request):
    print(request)

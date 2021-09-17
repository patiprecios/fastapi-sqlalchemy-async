
class TestDatabase():
    def test_connection(self, database_dsn):
        from fastapi_sqlalchemy_async.engine_repository import default

        default.create_engine(url=database_dsn)

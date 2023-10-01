class DatabaseConfig:
    def __init__(self, Host: str, Port: int, Password: str, User: str, DatabaseName='streamlist'):
        self.Host: str = Host
        self.Port: int = Port
        self.Password: str = Password
        self.User: str = User
        self.DatabaseName = DatabaseName


class Foo:
    def __init__(self, age=3):
        self.age = age


class Bar:
    def __init__(self, foo: Foo, name='Huy'):
        self.Foo = foo
        self.name = name


class Bar2:
    def __init__(self, foo: Foo, class_name='A6'):
        self.Foo = foo
        self.class_name = class_name


def with_config(config):
    def decorator(cls):
        def create_instance(*args, **kwargs):
            return cls(config, *args, **kwargs)
        return create_instance

    return decorator





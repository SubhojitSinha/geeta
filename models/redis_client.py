import redis
import pickle
from os import environ
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

env_verb     = "LOCAL" if environ['FLASK_ENV'] == 'development' else "PROD"
redis_config = app.config['REDIS'][env_verb]

class RedisClient:

    ENCODING   = 'utf-8'
    REDIS_HOST = redis_config['HOST']
    REDIS_PORT = redis_config['PORT']
    REDIS_SSL  = redis_config['SSL']

    # print(redis_config) if app.config['DEBUG'] else None

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, ssl=REDIS_SSL, db=0):
        """
        Initializes the RedisClient class.

        Args:
            host (str): The host address of the Redis server.
                Defaults to the class constant REDIS_HOST.
            port (int): The port number of the Redis server.
                Defaults to the class constant REDIS_PORT.
            db (int): The Redis database to connect to.
                Defaults to 0.

            PARAMS FOR REDIS CONNECTION
            ssl = True, ssl_cert_reqs = None, socket_connect_timeout = 50
        """
        self.host = host
        self.port = port
        self.db   = db
        self.ssl  = ssl
        # self.redis_client = redis.StrictRedis(
        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            ssl=self.ssl,
            ssl_cert_reqs=None,
            socket_connect_timeout=60
        )

    def check_connection(self):
        try:
            redis_check = self.redis_client.ping()
            if redis_check:
                return {
                    'status': True,
                    'message': 'Redis connection successful'
                }
            else:
                return {
                    'status': False,
                    'message': 'Redis connection failed'
                }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set(self, key, value, expire_seconds=None):
        """
        Stores the given value in the Redis database at the given key.

        Args:
            key (str): The key to store the value under
            value: The value to store
            expire_seconds (int, optional): The number of seconds after which the
                key should expire. If not given, the key will persist indefinitely.

        Returns:
            None
        """
        serialized_data = pickle.dumps(value)
        self.redis_client.set(key, serialized_data)
        if expire_seconds is not None:
            self.redis_client.expire(key, expire_seconds)

    def get(self, key):
        """
        Retrieves the value stored at the given key.

        Args:
            key (str): The key to retrieve the value from

        Returns:
            The value stored at the given key, or None if the key does not
            exist.
        """
        if self.redis_client.exists(key):
            value = self.redis_client.get(key)
            deserialized_data = pickle.loads(value)
        else:
            deserialized_data =  None
        return deserialized_data

    def delete(self, key):
        """
        Deletes the key from the Redis database.

        Args:
            key (str): The key to delete

        Returns:
            None
        """
        self.redis_client.delete(key)

    def exists(self, key):
        return True if self.redis_client.exists(key) == 1 else False

    def keys(self, pattern='*'):
        """
        Retrieves all keys matching the given pattern
        from the Redis database.

        Args:
            pattern (str): The pattern to match the keys against.
            Defaults to '*' which matches all keys.

        Returns:
            list[str]: A list of keys matching the given pattern.
        """
        keys = self.redis_client.scan_iter(pattern)
        return [key.decode(self.ENCODING) for key in keys]

    def get_all(self):
        """
        Retrieves all key-value pairs from the Redis database
        and returns them as a dictionary.

        Returns:
            dict: A dictionary containing all the key-value
            pairs from the Redis database.
        """
        redis_dict = {}
        for key in self.redis_client.scan_iter("*"):
            value = self.redis_client.get(key)
            redis_dict[key.decode(self.ENCODING)] = pickle.loads(value)

        return redis_dict

    def flushdb(self):
        """
        Flushes the Redis database.

        Returns:
            None
        """
        self.redis_client.flushdb()
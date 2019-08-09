import psycopg2
import psycopg2.extras

class ConnectionWrapper():
    def __init__(self, pw, user, port, host, db):
        self.__pw = pw
        self.__user = user
        self.__port = port
        self.__host = host
        self.__db = db
        self.conn = psycopg2.connect(host=self.__host, port=self.__port,
                                     database=self.__db, user=self.__user,
                                     password=self.__pw)


    def cursor(self, **kwargs):
        return self.conn.cursor(**kwargs)


    def reconnect(self, **kwargs):
        self.conn = psycopg2.connect(host=self.__host, port=self.__port,
                                database=self.__db, user=self.__user,
                                password=self.__pw)
        return self.conn


    def close(self):
        return self.conn.close()


class RequestsSession():
    retries = 15
    backoff_factor = 0.5
    status_forcelist = (429, 500, 502, 503, 504)
    headers = {'User-Agent': 'subscriber_completion_script / 1.0.0',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self):
        retry = urllib3.Retry(
            status=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist)

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)

        self.session = requests.Session()
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.headers.update(self.headers)




LOGGER = logging.getLogger()
LOG_LEVEL = logging.INFO
LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'f': {
            'format': '%(asctime)s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        }
    },
    'handlers': {
        'h': {
            'class': 'logging.FileHandler',
            'mode': 'w',
            'formatter': 'f',
            'filename': 'migration_logs.log',
        }
    },
    'root': {'handlers': ['h'], 'level': LOG_LEVEL}
}

@contextlib.contextmanager
def time_it(func):
    start = time.time()
    try:
        yield
    finally:
        LOGGER.debug('%s TOTAL COMPLETION TIME: %s', func, time.time() - start)

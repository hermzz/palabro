import os

config = {
    'db': {
        'dbn': 'mysql',
        'host': os.getenv('DB_HOST', 'db'),
        'user': os.getenv('DB_USER', 'root'),
        'pw': os.getenv('DB_PASS', 'example'),
        'db': 'palabro',
    }
}

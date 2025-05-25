import multiprocessing

bind = "127.0.0.1:8001"
workers = 2

# gunicorn askme.wsgi --config askme/gunicorn_cfg.py - команда для запуска gunicorn

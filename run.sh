uwsgi --http-socket 127.0.0.1:5000 --wsgi-file wsgi.py --master --processes 4 --threads 2 2> log.txt


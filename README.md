# django-showcase
Showcase is a comprehensive Django project designed to demonstrate my skills and knowledge in web development using Django

# Monitoring Django Project with Prometheus and Grafana

https://medium.com/@tommyraspati/monitoring-your-django-project-with-prometheus-and-grafana-b06a5ca78744


https://hodovi.cc/blog/django-monitoring-with-prometheus-and-grafana/



To start and stop grafana server

sudo systemctl start grafana-server

sudo systemctl stop grafana-server



To restart prometheus

./prometheus --config.file=prometheus.yml


To Add prometheus in Grafna 

in connection you need to give http://server-ip:9090


To check issue run docker-compose logs showcase 

To run celery
celery -A showcase worker --loglevel=info

remove all unused resources (images, containers, volumes, and networks)
docker system prune -a -f
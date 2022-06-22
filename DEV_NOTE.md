
systemctl status mosquitto

mosquitto_sub -h 127.0.0.1 -t topic
mosquitto_pub -h 127.0.0.1 -t topic -m "Hello"

alembic revision --autogenerate -m "add user table"

[Heroku-deploy](https://devcenter.heroku.com/articles/container-registry-and-runtime)

sudo heroku container:push web -a hidden-woodland-82190
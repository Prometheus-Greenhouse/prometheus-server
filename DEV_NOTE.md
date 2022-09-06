## MQTT Broker

```bash
systemctl status mosquitto
mosquitto_sub -h 127.0.0.1 -t topic
mosquitto_pub -h 127.0.0.1 -t topic -m "Hello"
```

## Setup database

```bash
sudo docker-compose -f stack.up -p prometheus -d
```

## Migrate database

```bash
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```

## Deploy heroku

[Heroku-deploy](https://devcenter.heroku.com/articles/container-registry-and-runtime)

```bash
sudo heroku container:push web -a hidden-woodland-82190
```

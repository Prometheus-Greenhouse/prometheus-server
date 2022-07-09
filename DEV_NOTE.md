
systemctl status mosquitto

mosquitto_sub -h 127.0.0.1 -t topic
mosquitto_pub -h 127.0.0.1 -t topic -m "Hello"

alembic revision --autogenerate -m "add user table"

[Heroku-deploy](https://devcenter.heroku.com/articles/container-registry-and-runtime)

sudo heroku container:push web -a hidden-woodland-82190

uvicorn --env-file .example.env main:app --port 8000 --reload

op.execute("""
CREATE SEQUENCE actuator_seq START WITH 1;
CREATE SEQUENCE farm_information_seq START WITH 1;
CREATE SEQUENCE sensor_seq START WITH 1;
CREATE SEQUENCE greenhouse_information_seq START WITH 1;
CREATE SEQUENCE nutrient_irrigator_seq START WITH 1;
CREATE SEQUENCE greenhouse_information_seq START WITH 1;
""")

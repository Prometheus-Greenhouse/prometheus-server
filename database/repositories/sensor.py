from project.core import repos


@repos
class SensorRepos:
    def __init__(self, session):
        self.session = session

    def insert(self, entity):
        self.session.add(entity)

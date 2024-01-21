from abc import ABC


class AbstractRepository(ABC):
    def create_model(self):
        raise NotImplemented()

    def retrieve_model(self):
        raise NotImplemented()

    def update_model(self):
        raise NotImplemented()

    def delete_model(self):
        raise NotImplemented()

    def get_user_by_email(self, email):
        raise NotImplemented()

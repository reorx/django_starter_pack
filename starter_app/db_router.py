class ModelNames(object):
    model_class_a = 'modelclassa'  # class ModelClassA(models.Model)
    model_class_b = 'modelclassb'  # class ModelClassB(models.Model)


db1_model_names = [
    ModelNames.model_class_a,
]

db2_model_names = [
    ModelNames.model_class_b,
]


def use_db1(model_name):
    return model_name in master_model_names


def use_db2(model_name):
    return model_name in clearing_model_names


def get_db_name(model_name):
    if use_db1(model_name):
        return DefaultRouter.db_db1
    elif use_db2(model_name):
        return DefaultRouter.db_db2
    else:
        return DefaultRouter.db_default


class DefaultRouter(object):
    db_default = 'default'
    db_db1 = 'foo'
    db_db2 = 'bar'

    def db_for_read(self, model, **hints):
        return get_db_name(model._meta.model_name)

    def db_for_write(self, model, **hints):
        return get_db_name(model._meta.model_name)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # ignore all models migration on db2
        if db == self.db_db2:
            return False

        # only migrate specified models on db1
        if use_db1(model_name):
            if db == self.db_db1:
                return True
            else:
                return False
        if db == self.db_db1:
            return False

        return None

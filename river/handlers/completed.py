from river.handlers.handler import Handler
from river.signals import workflow_is_completed

__author__ = 'ahmetdal'


class CompletedHandler(Handler):
    handlers = []

    @classmethod
    def dispatch(cls, sender, workflow_object, field, *args, **kwargs):
        suitable_handlers = filter(
            lambda h:
            h.get('workflow_object_pk', workflow_object.pk) == workflow_object.pk and
            h.get('field', field) == field, CompletedHandler.handlers
        )

        for handler in suitable_handlers:
            handler.get('handler')(object=workflow_object, field=field)

    @classmethod
    def register(cls, *args, **kwargs):
        d = super(CompletedHandler, cls).register(*args, **kwargs)
        CompletedHandler.handlers.append(d)


workflow_is_completed.connect(CompletedHandler.dispatch)
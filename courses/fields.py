from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields = None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                query = self.model.objects.all()
                if self.for_fields:
                    # qs = {}
                    # for field in self.for_fields:
                    #     qs[field] = getattr(model_instance, field)
                    # query = query.filter(**qs)
                    qs = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    query = query.filter(**qs)
                    last_item = query.latest(self.attname)
                    value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                    value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
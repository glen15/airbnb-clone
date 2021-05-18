from django.db import models

# objects.get 같이 object.어쩌고 하는 애들이 다 manager이고 밑에 클레스에서 이걸 확장시키는 것


class CustomReservationwManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
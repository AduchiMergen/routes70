from django.db import models
from django.urls import reverse


class Route(models.Model):

    # Relationships
    stops = models.ManyToManyField("routes.Stop", through="routes.RouteStop", blank=True)
    # type

    # Fields
    name = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("routes_Route_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("routes_Route_update", args=(self.pk,))


class Stop(models.Model):
    name = models.CharField(max_length=40)

    # Fields
    custom_id = models.CharField(max_length=40, blank=True)
    address = models.TextField(max_length=100)
    lon = models.DecimalField(max_digits=10, decimal_places=6)
    lat = models.DecimalField(max_digits=10, decimal_places=6)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return f'{self.name}, {self.address}'


class RouteStop(models.Model):
    order = models.IntegerField(default=0)

    # Relationships
    route = models.ForeignKey("routes.Route", on_delete=models.PROTECT)
    stop = models.ForeignKey("routes.Stop", on_delete=models.PROTECT)
    next_stop = models.OneToOneField(
        "routes.RouteStop",
        on_delete=models.PROTECT,
        related_name='previous_stop',
        blank=True,
        null=True,
    )

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

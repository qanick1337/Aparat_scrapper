from django.db import models

class Apartment(models.Model):
    sreality_id = models.CharField(max_length=100, unique=True)

    price = models.IntegerField()
    area_m2 = models.IntegerField()
    district = models.IntegerField()

    distance_to_local_hub = models.FloatField()

    # One hot features
    furnished = models.BooleanField(default=False)
    partly_furnished = models.BooleanField(default=False)
    not_furnished = models.BooleanField(default=False)
    metro = models.BooleanField(default=False)
    tram = models.BooleanField(default=False)
    new_building = models.BooleanField(default=False)
    after_reconstruction = models.BooleanField(default=False)
    brick = models.BooleanField(default=False)
    panel = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    cellar = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    parking_lots = models.BooleanField(default=False)

    # ML results
    predicted_price = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Apartment locality 
    seo_locality = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Apt: {self.area_m2}m2 in Prague {self.district} - {self.price} CZK"

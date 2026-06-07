from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Actor)
admin.site.register(Platform)
admin.site.register(Movie)
admin.site.register(Character)
admin.site.register(MovieCast)
admin.site.register(Crew)
admin.site.register(MovieCrew)
admin.site.register(Review)
admin.site.register(Language)


admin.site.register(WebSeries)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(SeriesCast)
admin.site.register(SeriesCrew)
admin.site.register(SeriesReview)

admin.site.register(Watchlist)
admin.site.register(ContactForm)


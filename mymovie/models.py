from django.db import models
from django.conf import settings

# Create your models here.
class Actor(models.Model):
    act_name = models.CharField(max_length=200)
    act_image = models.ImageField(upload_to="actors/")
    act_birth_date = models.DateField(null=True, blank=True)
    act_bio = models.TextField(blank=True)

    def __str__(self):
        return self.act_name
    

class Platform(models.Model):
    plat_name = models.CharField(max_length=100)
    plat_logo = models.ImageField(upload_to="platforms/")

    def __str__(self):
        return self.plat_name
    
class Language(models.Model):
    lang_name = models.CharField(max_length=100)

    def __str__(self):
        return self.lang_name
    

class Movie(models.Model):
    mov_name = models.CharField(max_length=200)
    mov_genre = models.CharField(max_length=100)
    mov_year = models.IntegerField()
    mov_duration = models.CharField(max_length=20)
    mov_description = models.TextField()
    mov_banner = models.ImageField(upload_to="movies/")
    mov_rating = models.FloatField()

    mov_platforms = models.ManyToManyField(Platform, blank=True)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.mov_name
    

class Character(models.Model):
    cat_name = models.CharField(max_length=200)

    def __str__(self):
        return self.cat_name
    

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="casts")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    cast_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["cast_order"]
    

class Crew(models.Model):
    crew_name = models.CharField(max_length=200)
    crew_role = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.crew_name} ({self.crew_role})"
    

class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="crews")
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    review_name = models.CharField(max_length=100)
    review_rating = models.FloatField()
    review_msg = models.TextField()
    review_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review_name
    




class WebSeries(models.Model):
    series_name = models.CharField(max_length=200)
    series_genre = models.CharField(max_length=100)
    series_start_year = models.IntegerField()
    series_end_year = models.IntegerField(null=True, blank=True)
    series_description = models.TextField()
    series_banner = models.ImageField(upload_to="series/")
    series_rating = models.FloatField()

    platforms = models.ManyToManyField(Platform, blank=True)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.series_name
    
class Season(models.Model):
    webseries = models.ForeignKey(WebSeries, on_delete=models.CASCADE, related_name="seasons")
    season_number = models.IntegerField()

    def __str__(self):
        return f"{self.webseries.series_name} - Season {self.season_number}"
    
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    episode_number = models.IntegerField()
    episode_title = models.CharField(max_length=200)
    episode_duration = models.CharField(max_length=20)
    episode_description = models.TextField()

    def __str__(self):
        return f"{self.episode_title} (Ep {self.episode_number})"
    
class SeriesCast(models.Model):
    webseries = models.ForeignKey(WebSeries, on_delete=models.CASCADE, related_name="casts")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    cast_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["cast_order"]

class SeriesCrew(models.Model):
    webseries = models.ForeignKey(WebSeries, on_delete=models.CASCADE, related_name="crews")
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)

class SeriesReview(models.Model):
    webseries = models.ForeignKey(WebSeries, on_delete=models.CASCADE, related_name="reviews")
    review_name = models.CharField(max_length=100)
    review_rating = models.FloatField()
    review_msg = models.TextField()
    review_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review_name
    


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    webseries = models.ForeignKey(WebSeries, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'movie'),
            ('user', 'webseries')
        ]



class ContactForm(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_msg = models.TextField()
    message_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact_name
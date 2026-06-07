from rest_framework import serializers
from .models import Movie, MovieCast, MovieCrew, Platform, Actor, Character, Language, Review, WebSeries, Season, Episode, SeriesCast, SeriesCrew, SeriesReview, ContactForm, Crew
from mypayment.serializers import RentalSerializer
import json


class PlatformSerializer(serializers.ModelSerializer):
    plat_logo = serializers.SerializerMethodField()

    class Meta:
        model = Platform
        fields = ["id", "plat_name", "plat_logo"]

    def get_plat_logo(self, obj):
        return obj.plat_logo.url if obj.plat_logo else None


class ActorSerializer(serializers.ModelSerializer):
    act_image = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ["id", "act_name", "act_image"]

    def get_act_image(self, obj):
        if obj.act_image:
            return obj.act_image.url
        return None


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "cat_name"]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class MovieCastSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    character = CharacterSerializer()

    class Meta:
        model = MovieCast
        fields = ["id", "actor", "character", "cast_order"]


class MovieCrewSerializer(serializers.ModelSerializer):
    crew = serializers.StringRelatedField()

    class Meta:
        model = MovieCrew
        fields = "__all__"


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    platforms = PlatformSerializer(source="mov_platforms", many=True)
    languages = LanguageSerializer(many=True)
    casts = MovieCastSerializer(many=True)
    crews = MovieCrewSerializer(many=True)
    reviews = ReviewSerializers(many=True)
    rentals = serializers.SerializerMethodField()
    mov_banner = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_mov_banner(self, obj):
        return obj.mov_banner.url if obj.mov_banner else None

    def get_rentals(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return []
        rentals = obj.rentals.filter(user=request.user, status="success")
        return RentalSerializer(rentals, many=True).data




class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"

class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Season
        fields = ["id", "season_number", "episodes"]

class SeriesCastSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    character = CharacterSerializer()

    class Meta:
        model = SeriesCast
        fields = ["id", "actor", "character", "cast_order"]

class SeriesCrewSerializer(serializers.ModelSerializer):
    crew = serializers.StringRelatedField()

    class Meta:
        model = SeriesCrew
        fields = "__all__"

class SeriesReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesReview
        fields = "__all__"

class WebSeriesSerializer(serializers.ModelSerializer):
    platforms = PlatformSerializer(many=True)
    languages = LanguageSerializer(many=True)
    seasons = SeasonSerializer(many=True)
    casts = SeriesCastSerializer(many=True)
    crews = SeriesCrewSerializer(many=True)
    reviews = SeriesReviewSerializer(many=True)
    rentals = serializers.SerializerMethodField()
    series_banner = serializers.SerializerMethodField()

    class Meta:
        model = WebSeries
        fields = "__all__"

    def get_series_banner(self, obj):
        return obj.series_banner.url if obj.series_banner else None

    def get_rentals(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return []
        rentals = obj.rentals.filter(user=request.user, status="success")
        return RentalSerializer(rentals, many=True).data
    


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"




class AdminActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class AdminMovieSerializer(serializers.ModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    mov_platforms = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    casts = serializers.CharField(write_only=True, required=False)
    crews = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Movie
        fields = "__all__"



    def create(self, validated_data):
        request = self.context.get("request")

        # ✅ REMOVE EVERYTHING BEFORE CREATE
        validated_data.pop("casts", None)
        validated_data.pop("crews", None)
        validated_data.pop("mov_platforms", None)
        validated_data.pop("languages", None)

        # Parse JSON
        casts_data = json.loads(request.data.get("casts", "[]"))
        crews_data = json.loads(request.data.get("crews", "[]"))

        # Create movie
        movie = Movie.objects.create(**validated_data)

        # ✅ Set ManyToMany
        movie.mov_platforms.set(request.data.getlist("mov_platforms"))
        movie.languages.set(request.data.getlist("languages"))

        # ✅ Create Casts manually
        for cast in casts_data:
            if not cast.get("actor") or not cast.get("character"):
                continue  # ✅ skip invalid rows

            MovieCast.objects.create(
                movie=movie,
                actor_id=cast["actor"],
                character_id=cast["character"],
                cast_order=cast.get("cast_order", 0)
            )

        # ✅ Create Crews manually
        for crew in crews_data:
            if not crew.get("crew"):
                continue

            MovieCrew.objects.create(
                movie=movie,
                crew_id=crew["crew"]
            )

        return movie

    def update(self, instance, validated_data):
        request = self.context.get("request")

        validated_data.pop("casts", None)
        validated_data.pop("crews", None)
        validated_data.pop("mov_platforms", None)
        validated_data.pop("languages", None)

        casts_data = json.loads(request.data.get("casts", "[]"))
        crews_data = json.loads(request.data.get("crews", "[]"))

        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # M2M
        platforms = request.data.getlist("mov_platforms")
        platforms = [int(i) for i in platforms if str(i).isdigit()]

        if platforms:
            instance.mov_platforms.set(platforms)
        languages = request.data.getlist("languages")
        languages = [int(i) for i in languages if str(i).isdigit()]

        if languages:
            instance.languages.set(languages)

        # Clear old
        instance.casts.all().delete()
        instance.crews.all().delete()

        # Recreate
        for cast in casts_data:
            MovieCast.objects.create(
                movie=instance,
                actor_id=cast["actor"],
                character_id=cast["character"],
                cast_order=cast.get("cast_order", 0)
            )

        for crew in crews_data:
            MovieCrew.objects.create(
                movie=instance,
                crew_id=crew["crew"]
            )

        return instance


class AdminMovieCastSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    character = CharacterSerializer()

    class Meta:
        model = MovieCast
        fields = ["id", "movie", "actor", "character", "cast_order"]


class AdminMovieCastWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCast
        fields = ["movie", "actor", "character", "cast_order"]


class AdminMovieCrewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCrew
        fields = ["movie", "crew"]



class WebSeriesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSeries
        fields = [
            "series_name",
            "series_genre",
            "series_start_year",
            "series_end_year",
            "series_description",
            "series_banner",
            "series_rating",
            "platforms",
            "languages"
        ]


class SeasonReadSerializer(serializers.ModelSerializer):
    webseries = serializers.CharField(source="webseries.series_name")
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ["id", "webseries", "season_number", "episodes"]

class SeasonWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ["id", "webseries", "season_number"]



class SeriesReadCastSerializer(serializers.ModelSerializer):
    webseries = serializers.CharField(source="webseries.series_name")
    actor = ActorSerializer()
    character = CharacterSerializer()
    class Meta:
        model = SeriesCast
        fields = ["id", "webseries", "actor", "character", "cast_order"]
        
class SeriesCastWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesCast
        fields = ["id", "webseries", "actor", "character", "cast_order"]



class SeriesCrewReadSerializer(serializers.ModelSerializer):
    webseries = serializers.CharField(source="webseries.series_name")
    crew = serializers.StringRelatedField()
    class Meta:
        model = SeriesCrew
        fields = ["id", "webseries", "crew"]

        
class SeriesCrewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesCrew
        fields = ["id", "webseries", "crew"]


class AdminSeriesReviewReadSerializer(serializers.ModelSerializer):
    webseries = serializers.CharField(source="webseries.series_name", read_only=True)
    webseries_id = serializers.IntegerField(source="webseries.id", read_only=True)

    class Meta:
        model = SeriesReview
        fields = "__all__"


class AdminSeriesReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesReview
        fields = ["id", "webseries", "review_name", "review_rating", "review_msg"]







class WebSeriesFullCreateSerializer(serializers.ModelSerializer):
    casts = serializers.ListField(write_only=True)
    crews = serializers.ListField(write_only=True)

    class Meta:
        model = WebSeries
        fields = [
            "series_name",
            "series_genre",
            "series_start_year",
            "series_end_year",
            "series_description",
            "series_banner",
            "series_rating",
            "platforms",
            "languages",
            "casts",
            "crews"
        ]



    def create(self, validated_data):
        request = self.context.get("request")

        # ✅ REMOVE EVERYTHING FIRST
        validated_data.pop("casts", None)
        validated_data.pop("crews", None)
        validated_data.pop("platforms", None)
        validated_data.pop("languages", None)

        # ✅ Parse JSON
        casts_data = json.loads(request.data.get("casts", "[]"))
        crews_data = json.loads(request.data.get("crews", "[]"))

        # ✅ Create main object
        webseries = WebSeries.objects.create(**validated_data)

        # ✅ M2M
        webseries.platforms.set(request.data.getlist("platforms"))
        webseries.languages.set(request.data.getlist("languages"))

        # ✅ Create Cast
        for cast in casts_data:
            if not cast.get("actor") or not cast.get("character"):
                continue

            SeriesCast.objects.create(
                webseries=webseries,
                actor_id=cast["actor"],
                character_id=cast["character"],
                cast_order=cast.get("cast_order", 0)
            )

        # ✅ Create Crew
        for crew in crews_data:
            if not crew.get("crew"):
                continue

            SeriesCrew.objects.create(
                webseries=webseries,
                crew_id=crew["crew"]
            )

        return webseries
    
    def update(self, instance, validated_data):
        request = self.context.get("request")
        import json

        # ❌ remove nested & m2m
        validated_data.pop("casts", None)
        validated_data.pop("crews", None)
        validated_data.pop("platforms", None)
        validated_data.pop("languages", None)

        casts_data = json.loads(request.data.get("casts", "[]"))
        crews_data = json.loads(request.data.get("crews", "[]"))

        # ✅ update main fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # ✅ M2M
        instance.platforms.set(request.data.getlist("platforms"))
        instance.languages.set(request.data.getlist("languages"))

        # ❌ clear old
        instance.casts.all().delete()
        instance.crews.all().delete()

        # ✅ recreate cast
        for cast in casts_data:
            if not cast.get("actor") or not cast.get("character"):
                continue

            SeriesCast.objects.create(
                webseries=instance,
                actor_id=cast["actor"],
                character_id=cast["character"],
                cast_order=cast.get("cast_order", 0)
            )

        # ✅ recreate crew
        for crew in crews_data:
            if not crew.get("crew"):
                continue

            SeriesCrew.objects.create(
                webseries=instance,
                crew_id=crew["crew"]
            )

        return instance
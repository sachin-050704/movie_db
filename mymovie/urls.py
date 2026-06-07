from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("actors", AdminActorViewSet)
router.register("platforms", AdminPlatformViewSet)
router.register("languages", AdminLanguageViewSet)
router.register("movies", AdminMovieViewSet)
router.register("characters", AdminCharacterViewSet)
router.register("crews", AdminCrewViewSet)
router.register("moviecast", AdminMovieCastViewSet)
router.register("moviecrew", AdminMovieCrewViewSet)
router.register("reviews", AdminReviewViewSet)
router.register("webseries", AdminWebSeriesViewSet)
router.register("season", AdminSeasonViewSet)
router.register("episodes", AdminEpisodeViewSet)
router.register("seriescast", AdminSeriesCastViewSet)
router.register("seriescrew", AdminSeriesCrewViewSet)
router.register("seriesreview", AdminSeriesReviewViewSet)
router.register("contact", AdminContactViewSet)



urlpatterns = [
    path("", movie_list),
    path("wevList/", web_list),
    path("<int:id>/", movie_detail),
    path("add_review/", add_review),
    path("add_web_review/", add_web_review),
    path("toggle/", toggle_watchlist),
    path("watchlist/", get_watchlist),
    path("removewatch/<int:movie_id>/", remove_watchlist),
    path("contactForm/", contact_form),
    path("admin1/", include(router.urls)),
]


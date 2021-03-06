from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from . import views
from images import views as image_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("s3Upload/", csrf_exempt(views.sign_s3)),
    path("cron/expireStories", image_views.expire_stories)
]

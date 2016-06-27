from django.conf.urls import url
from .views import PeopleCreate, PeopleUpdate, \
    PeopleDelete, PeopleList, PeopleDetail, AutoComplete

app_name = 'core'

urlpatterns = [
    url(r'^$', PeopleList.as_view(), name='people-list'),
    url(r'people/add/$',
        PeopleCreate.as_view(), name='people-add'),
    url(r'people/(?P<pk>[0-9]+)/$',
        PeopleUpdate.as_view(), name='people-update'),
    url(r'people/(?P<pk>[0-9]+)/detail$',
        PeopleDetail.as_view(), name='people-detail'),
    url(r'people/(?P<pk>[0-9]+)/delete/$',
        PeopleDelete.as_view(), name='people-delete'),
    url(r'autocomplete/$',
        AutoComplete.as_view(), name='people-auto'),
    ]

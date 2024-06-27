from django.urls import path
from .views import PersonCreate, PersonList, PersonDetail, PersonUpdate, DeleteView

urlpatterns = [
    path('', PersonList.as_view(), name='persons'),
    path('person/<int:pk>/', PersonDetail.as_view(), name='person'),
    path('person-create/', PersonCreate.as_view(), name='person-create'),
    path('person-update/<int:pk>/', PersonUpdate.as_view(), name='person-update'),
    path('person-delete/<int:pk>/', DeleteView.as_view(), name='person-delete'),
]

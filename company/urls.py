from django.urls import path
from company.views import CreateUpdateCompanyView

urlpatterns = [
    # path('', CreateCompanyView.as_view(), name='create-company'),
    path('', CreateUpdateCompanyView.as_view(), name='update-company'),
]

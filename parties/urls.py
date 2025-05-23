from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartyViewSet, TransactionViewSet

router=DefaultRouter()
router.register('party',PartyViewSet)
router.register('transaction',TransactionViewSet)

urlpatterns = [
    path('',include(router.urls)),
]


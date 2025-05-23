from core.models import Party, Transaction
from rest_framework import generics, permissions, viewsets
from .serializers import PartySerializer, TransactionSerializer
from rest_framework.authentication import TokenAuthentication
from parties import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Case, When, F, DecimalField, Value as V




class PartyViewSet(viewsets.ModelViewSet):
  serializer_class=PartySerializer
  authentication_classes=[TokenAuthentication]
  permission_classes=[permissions.IsAuthenticated]
  queryset=Party.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user).order_by('-id')

  def get_serializer_class(self):
    if self.action=='list':
      return serializers.PartySerializer

    return self.serializer_class

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
  serializer_class=TransactionSerializer
  authentication_classes=[TokenAuthentication]
  permission_classes=[permissions.IsAuthenticated]
  queryset=Transaction.objects.all()

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user).order_by('-timestamp')

  def get_serializer_class(self):
    if self.action=='list':
      return serializers.TransactionSerializer
    return self.serializer_class

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  @action(detail=False,methods=['get'])
  def summary(self,request):
    user=request.user

    overall_total= Transaction.objects.filter(user=user).aggregate(
      total_given=Sum(
        Case(
          When(transaction_type='given', then=F('amount')),
          default=V(0),
          output_field=DecimalField()
        )
      ),
      total_taken=Sum(
        Case(
          When(transaction_type='taken', then=F('amount')),
          default=V(0),
          output_field=DecimalField()
        )
      )

    )
    overall_given=overall_total['total_given'] or 0
    overall_taken=overall_total['total_taken'] or 0

    parties=Party.objects.filter(user=user)
    per_party_data=[]

    for party in parties:
      party_totals = party.transactions.aggregate(
        total_given=Sum(
          Case(
            When(transaction_type='given', then=F('amount')),
            default=V(0),
            output_field=DecimalField()
          )
        ),
        total_taken=Sum(
          Case(
            When(transaction_type='taken', then=F('amount')),
            default=V(0),
            output_field=DecimalField()
          )
        )
      )
      per_party_data.append({
        'party': party.name,
        'total_given': party_totals['total_given'] or 0,
        'total_taken': party_totals['total_taken'] or 0,
        'net_balance': (party_totals['total_given'] or 0) - (party_totals['total_taken'] or 0)})

    return Response({

        'total_given': overall_given,
        'total_taken': overall_taken,
        'net_balance': overall_given - overall_taken,
      'per_party': per_party_data})



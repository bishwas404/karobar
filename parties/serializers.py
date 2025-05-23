from core.models import Party, Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model=Transaction
    fields=['id','party','amount','transaction_type','note','timestamp']
    read_only_fields=['id','timestamp']

class PartySerializer(serializers.ModelSerializer):
  total_given=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
  total_taken=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
  class Meta:
    model=Party
    fields=['id','name','total_given','total_taken']


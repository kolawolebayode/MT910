from rest_framework import serializers
from .models import Ref, Acct



class REFSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ref
        fields = '__all__'


class ACCTSerializer(serializers.ModelSerializer):
    #refe = REFSerializer()
    class Meta:
        model = Acct
        fields = '__all__'




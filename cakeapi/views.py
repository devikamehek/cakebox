from django.shortcuts import render
from myapp.models import Cake

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

# Create your views here.

class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cake
        exclude=("id",)

class CakesView(ViewSet):
    # localhost:8000/api/cakes/
    # method-GET
    def list(self,request,*args,**kwargs):
        qs=Cake.objects.all()
        # qs-->py native -- deserialization
        serializer=CakeSerializer(qs,many=True)
        return Response(data=serializer.data)

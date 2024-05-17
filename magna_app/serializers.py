
from datetime import date

from rest_framework import serializers

from .models import *


class UsuarioSerializer(serializers.ModelSerializer):

    days_to_vencimiento = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ('nombre', 'activo', 'sexo', 'vencimiento', 'days_to_vencimiento',)
        
        
    def to_representation(self, instance):
        data = super(UsuarioSerializer, self).to_representation(instance)
        # Format the "vencimiento" field
        data['vencimiento'] = instance.vencimiento.strftime('%d/%m/%Y')
        return data
        
    def get_days_to_vencimiento(self, obj):
        today = date.today()
        delta = obj.vencimiento - today
        return delta.days

        



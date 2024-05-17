# Create your views here.
from io import BytesIO
from pathlib import Path
import pandas
from django.contrib import messages
from django.http import (HttpResponse,HttpResponseRedirect)
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from rest_framework.decorators import api_view
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .utils import GraphicsDataGenerator




@api_view(["GET", "POST"])
def admin_usuario(request, dni):
    if request.method == "GET":
        try:
            usuario = Usuario.objects.get(DNI=dni)
            serializer = UsuarioSerializer(usuario, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(
                {"not_found": f"Usuario with DNI {dni} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "POST":
        try:
            user = Usuario.objects.get(DNI=dni)
            Asistencia.objects.create(usuario=user)
            return Response({"message": "asistencia tomada"}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(
                {"not found": f"Usuario with DNI {dni} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )





def upload_excel(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_upload"]

        if not excel_file.name.endswith(".xlsx"):
            messages.warning(request, "The wrong file type was uploaded")
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        # Load the Excel file into a Pandas DataFrame
        data_frame = pandas.read_excel(excel_file)

        # Iterate over the rows of the DataFrame and create or update instances of the Usuario model
        for index, row in data_frame.iterrows():
            Usuario.objects.update_or_create(
                nombre=row["nombre"],
                apellido=row["apellido"],
                sexo=row["sexo"],
                DNI=row["DNI"],
                pago=row["pago"],
                vencimiento=row["vencimiento"],
                celular=int(row["celular"]) if pandas.notna(row["celular"]) else None,
            )

        return HttpResponseRedirect(reverse("admin:index"))

def graphics(request):
    data_generator = GraphicsDataGenerator()
    data = data_generator.generate_graphics_data()
    return render(request, "graphics.html", {"data": data})


    
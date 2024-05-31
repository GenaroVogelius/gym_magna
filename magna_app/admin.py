from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.forms.widgets import TextInput
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

from .models import *
from .views import *




class MagnaAdminArea(admin.AdminSite):
    site_header = "Magna Administración"
    site_url = "/entrada"
    index_title = "Administración de Magna Gym"
    site_header = 'Magna gym administración'


magna_site = MagnaAdminArea(name="magnaAdmin")

# ? hasta ahi lo que hiciste fue crear una administración personalizada


# ? aca lo que haces es customize el formulario de django
class UsuarioModelForm(forms.ModelForm):
    DNI = forms.IntegerField(widget=forms.TextInput(attrs={"size": 10}))
    celular = forms.IntegerField(
        widget=forms.TextInput(attrs={"size": 10}), required=False
    )


    class Meta:
        model = Usuario
        fields = "__all__"


class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "sexo",
        "DNI",
        "celular",
        "fecha_de_pago",
        "vencimiento",
        "tipo_de_plan",
        "activo",
    )
    ordering = ("-date_modified",)
    list_filter = ("activo",)
    # te hace la paginación:
    list_per_page = 10
    search_fields = (
        "nombre",
        "apellido",
        "DNI",
    )
    search_help_text = "Buscar por nombre, apelido o DNI"
    actions = ["mark_as_published", "mark_as_unpublished"]
    change_list_template = "change_list_usuarios.html"



    form = UsuarioModelForm

    def update_activo(self, obj):
        if obj.vencimiento < timezone.now().date():
            obj.activo = False
        else:
            obj.activo = True
        obj.save()

    update_activo.short_description = "Update Activo"

    # the changelist_view method checks the last execution date stored in the cache (update_activo_last_execution_date). If it is different from the current date, the update_activo function is called for each object in the queryset, and the activo field is updated accordingly. After the execution, the current date is stored in the cache as the last execution date.
    def changelist_view(self, request, extra_context=None):
        cache_key = "update_activo_last_execution_date"
        

        last_execution_date = cache.get(cache_key)
        current_date = timezone.now().date()

        print(current_date)
        print(last_execution_date)

        if last_execution_date is None or last_execution_date != current_date:
            cache_timeout = 60 * 60 * 24  # 24 horas
            print("entra")
            queryset = self.get_queryset(request)
            for obj in queryset:
                self.update_activo(obj)

            cache.set(cache_key, current_date, cache_timeout)

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        # lo que haces aca es crear este path y que cuando se lo llame se ejecute la función upload
        new_urls = [path("upload-excel/", upload_excel), path("graphics/", graphics)]
        return new_urls + urls


class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "dia", "hora", "activo")
    list_filter = ("dia", "activo")
    search_fields = ("usuario",)
    search_help_text = "Buscar por nombre"
    list_per_page = 10
    ordering = ("-dia",)



class TipoPlanAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "vigencia")
    ordering = ("-precio",)
class PreciosHistoricoAdmin(admin.ModelAdmin):
    pass



magna_site.register(Usuario, UsuarioAdmin)
magna_site.register(Asistencia, AsistenciaAdmin)
magna_site.register(TipoPlan, TipoPlanAdmin)
magna_site.register(PreciosHistorico, PreciosHistoricoAdmin)

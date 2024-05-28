from django.db import models
from dateutil.relativedelta import relativedelta
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now
from django.db.models.functions import TruncMonth


class PreciosHistorico(models.Model):
    # solo es creado cuando se modifica en usuario la fecha de pago, y cuando se modifica en tipoPlan el precio
    # usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    usuario_nombre = models.CharField(max_length=50)
    nombre_plan = models.CharField(max_length=50)
    precio_plan = models.PositiveIntegerField()
    fecha_de_pago = models.DateField(default=timezone.now, null=False, blank=False)


    class Meta:
        verbose_name = "Abono" 
        verbose_name_plural = "Abonos realizados"


    def __str__(self) -> str:
        return f"{self.usuario_nombre} pagó ${self.precio_plan} el {self.fecha_de_pago}"



class TipoPlan(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    vigencia = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.nombre
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.title()

        # # Means that it's a modification
        # if self.pk:
        #     previous_plan = TipoPlan.objects.get(pk=self.pk)
        #     # Means that there is a modification on the price
        #     if previous_plan.precio != self.precio:
        #         self.save_tipo_plan_history()
        super().save(*args, **kwargs)


    def save_tipo_plan_history(self):

        this_month= now().date()
        this_month = this_month.replace(day=1)

        queryset_users = Usuario.objects.annotate(
                month=TruncMonth('fecha_de_pago')
            ).filter(
                month=this_month,
                tipo_de_plan = self
            )
        
        precios_historico_list = []
        for previous_user in queryset_users:
            precios_historico_list.append(
                PreciosHistorico(
                    usuario=previous_user,
                    nombre_plan=previous_user.tipo_de_plan.nombre,
                    precio_plan=previous_user.tipo_de_plan.precio,
                    fecha_de_pago=previous_user.fecha_de_pago,
                )
            )

        # Use bulk_create to insert all records in one go, is more efficient
        PreciosHistorico.objects.bulk_create(precios_historico_list)



    class Meta:
        verbose_name = "Tipo de plan" 
        verbose_name_plural = "Tipos de Planes"


class Usuario(models.Model):
    SEX_CHOICES = [
        ("F", "Femenino"),
        ("M", "Masculino"),
    ]
    tipos_de_pagos = [
        ("E", "Efectivo"),
        ("T", "Transferencia"),
    ]
    

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10, choices=SEX_CHOICES)
    date_modified = models.DateTimeField(default=timezone.now, editable=False)
    DNI = models.BigIntegerField(unique=True, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    tipo_de_pago=models.CharField(max_length=20, choices=tipos_de_pagos)
    tipo_de_plan = models.ForeignKey(
        'TipoPlan', on_delete=models.PROTECT,
    )
    fecha_de_pago = models.DateField(default=timezone.now, null=False, blank=False)
    vencimiento = models.DateField(
        null=True, blank=True, help_text="Si no es especificado será al mes siguiente a la fecha de pago"
    )
    activo = models.BooleanField(default=True, editable=False)
    id = models.AutoField(primary_key=True)
    observaciones=models.CharField(max_length=200, blank=True, null=True)


    @receiver(pre_save, sender="magna_app.Usuario")
    def update_activo(sender, instance, **kwargs):
        try:
            if instance.vencimiento.date() < timezone.now().date():
                instance.activo = False
            else:
                instance.activo = True
        except:
            if instance.vencimiento < timezone.now().date():
                instance.activo = False
            else:
                instance.activo = True

    @staticmethod
    @receiver(post_save, sender="magna_app.Usuario")
    def post_save(instance, created, **kwargs):
        if created:
            instance.save_tipo_plan_history()



    def save(self, *args, **kwargs):
        #? para cuando se crea un nuevo usuario.
        if self.vencimiento == None:
            self.vencimiento = self.fecha_de_pago + relativedelta(months=1)

            # print(self.vencimiento)
            # if self.vencimiento.day != self.pago.day:
            #     self.vencimiento = self.vencimiento.replace(day=self.pago.day)
        else:
            # esto significa que solo modifico el dia del pago.
            # ! para testear podes sacar esto
            if self.fecha_de_pago > self.vencimiento:
                self.vencimiento = self.fecha_de_pago + relativedelta(months=1)
                if self.vencimiento.day != self.fecha_de_pago.day:
                    self.vencimiento = self.vencimiento.replace(day=self.fecha_de_pago.day)

        self.nombre = self.nombre.title()
        self.apellido = self.apellido.title()
        self.date_modified = timezone.now()

        # # Means that there is a modification of the user
        if self.pk:
            previous_user = Usuario.objects.get(pk=self.pk)
            # Means that there is a modification of the fecha de pago date
            if previous_user.fecha_de_pago != self.fecha_de_pago:
                self.save_tipo_plan_history()
        super().save(*args, **kwargs)


    def save_tipo_plan_history(self):
        PreciosHistorico.objects.create(
            usuario_nombre=self.nombre,
            nombre_plan=self.tipo_de_plan.nombre,
            precio_plan = self.tipo_de_plan.precio,
            fecha_de_pago = self.fecha_de_pago,
        )
        # ? Al poner super() lo que hace es buscar de las clases padres (en este caso models.Model) el metodo que vos le indicas (.save()). al ponerlo asi agregas las lineas de codigo que escribiste y después el resto será igual a lo que indica la clase padre, sirve para mantener la inheritance de la clase padre y no sobreescribir cosas que no queres.
        # ? if you remove the super().save(*args, **kwargs) call, the custom behavior you have defined in your save method will still be executed, but the model instance will not be saved to the database.

    def __str__(self):
        return f"{self.nombre} DNI: {self.DNI}"


class Asistencia(models.Model):

    usuario = models.ForeignKey(
        'Usuario', on_delete=models.CASCADE,
    )
    dia = models.DateField(auto_now=True)
    hora = models.TimeField(auto_now=True)
    activo = models.BooleanField(default=True, editable=False)
    
    
    def save(self, *args, **kwargs):
        # ?This will set self.activo to True if self.usuario.activo is True, and False 
        self.activo = bool(self.usuario.activo)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario} vino {self.dia} a las {self.hora}"
    










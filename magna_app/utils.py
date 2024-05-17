import json
from datetime import time, timedelta

import pandas
from django.db.models import Q
from django.utils import timezone

from .models import Asistencia, Usuario


def delete_old_asistencias():
    # Calculate the date 13 months ago from the current date
    thirteen_months_ago = timezone.now() - timedelta(days=390)

    # Use the QuerySet filter to get Asistencia objects older than 13 months
    old_asistencias = Asistencia.objects.filter(dia__lt=thirteen_months_ago)

    # Delete the old Asistencia objects
    old_asistencias.delete()

def delete_old_users():

    # Calculate the date 13 months ago from the current date
    thirteen_months_ago = timezone.now() - timedelta(days=390)

    # Use the QuerySet filter to get Asistencia objects older than 13 months
    old_users = Usuario.objects.filter(vencimiento__lt=thirteen_months_ago)

    # Delete the old Asistencia objects
    old_users.delete()


class GraphicsDataGenerator:
    def __init__(self):
        self.SLICES = [time(hour, minute) for hour in range(7, 22) for minute in (0, 30)]

    def get_asistencias_per_week_dataframe(self):
        """
        Obtiene la asistencia 7 dias atras y crea un dataframe
        Returns:
            pandas.DataFrame: A DataFrame containing attendance data.
        """
        seven_days_ago = timezone.now() - timedelta(days=7)
        asistencias = Asistencia.objects.filter(dia__range=(seven_days_ago, timezone.now()))

        asistencias_df = pandas.DataFrame(asistencias.values())
        return asistencias_df


    def check_missing_dates(self, asistencias_df):
        """
        Checks if the data that is missing is a sunday or another day, if it's another day it will append the index of that day in a list to be used after for the front-end.
        Args:
            asistencias_df (pandas.DataFrame): DataFrame with attendance data.

        Returns:
            python.List: with numbers.
        """
        min_date = asistencias_df['dia'].min()
        max_date = asistencias_df['dia'].max()

        # Create a list of expected dates between the minimum and maximum dates
        expected_dates = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]
        
        # Find the missing dates by comparing the expected dates with the unique dates in the DataFrame
        missing_dates = []
        days_with_assistance = asistencias_df['dia'].unique()
        contador=0
        for date in expected_dates:
            
            if date not in days_with_assistance:
                missing_dates.append(contador)
            contador += 1

        return missing_dates

    def get_asistencias_per_month(self):
        """
        Obtiene la asistencia total de hoy a 12 meses atras y crea un dataframe
        Returns:
            pandas.DataFrame: A DataFrame containing attendance data.
        """
        twelve_month_ago = timezone.now() - timedelta(days=30 * 12)
        asistencias = Asistencia.objects.filter(dia__range=(twelve_month_ago, timezone.now()))

        asistencias_per_month_df = pandas.DataFrame(asistencias.values())

        return asistencias_per_month_df

    def get_asistencias_per_month_count(self, asistencias_per_month_df):
        """
        Cuenta cuantas personas fueron por mes y devuelve diccionario con mes y cantidad

        Args:
            sistencias_per_month_df (pandas.DataFrame): DataFrame with attendance data per month.

        Returns:
            python.Dict: {"2023-08":60},...
        """

        asistencias_per_month_df['month'] = pandas.to_datetime(asistencias_per_month_df['dia']).dt.strftime('%Y-%m')

        # Count the number of persons per month
        persons_per_month_df = asistencias_per_month_df.groupby('month')['usuario_id'].count()
        return persons_per_month_df.to_dict()


    def process_time_slices(self, asistencias_df):
        """
        Establece en que horario llego la persona en base a la división que efectuaste que seria :00 e :30 y crea en el dataframe una columna llamada persons_arrive_per_time con esos valores.

        Args:
            asistencias_df (pandas.DataFrame): DataFrame with attendance data.

        Returns:
            pandas.DataFrame: DataFrame with added 'time_slice' and 'persons_arrive_per_time' columns.
        """

        def categorize_time(time_row):
            for first, second in zip(self.SLICES[::1], self.SLICES[1::1]):
                if first <= time_row < second:
                    return str(first)[:-3]
            return None
        def change_date_order(date):
            year, month, day = str(date).split('-')
            return f'{day}-{month}'

        asistencias_df['time_slice'] = asistencias_df['hora'].apply(categorize_time)
        time_slice_counts_per_day_df = asistencias_df.groupby(['dia', 'time_slice']).size().reset_index(name='persons_arrive_per_time')
      
        #? es para cambiar el formato de año-mes-dia a dia/mes
        time_slice_counts_per_day_df['dia'] = time_slice_counts_per_day_df['dia'].apply(change_date_order)
        
        return time_slice_counts_per_day_df

    def process_daily_total_arrivals(self, time_slice_counts_per_day_df):
        """
        Crea un diccionario con los los dias(key) y cantidad de personas que fueron(values)
        Args:
            time_slice_counts_per_day_df (pandas.DataFrame): DataFrame with daily attendance counts.

        Returns:
            dict: Dictionary containing daily total arrivals data.
        """
        

        daily_total_arrivals_df = time_slice_counts_per_day_df.groupby('dia')['persons_arrive_per_time'].sum()

        # esto es para que te quede el dia de hoy al final del dataframe
        daily_total_arrivals_df = daily_total_arrivals_df.loc[time_slice_counts_per_day_df['dia'].unique()]

        json_data_pandas_daily_total_arrivals = daily_total_arrivals_df.to_json(orient='index')
        daily_total_arrivals_dict = json.loads(json_data_pandas_daily_total_arrivals)
        return daily_total_arrivals_dict

    def process_attendance_per_day_and_time(self, time_slice_counts_per_day_df):
        """
        Procesa el dataframe y crea una cascada de diccionarios asi: {'05-08': {'time_counts': {'12:00': 1}}},

        Args:
            time_slice_counts_per_day_df (pandas.DataFrame): DataFrame with attendance data.

        Returns:
            dict: Dictionary containing attendance data per day and time.
        """


        def dict_time_count(group):
            return dict(zip(group['time_slice'], group['persons_arrive_per_time']))

        #? Group by 'dia' and apply the function to each group, reset_index es para que la columna que tiene los     diccionarios se llame time_counts

        day_and_time_df = time_slice_counts_per_day_df.groupby('dia').apply(dict_time_count).reset_index(name='time_counts')

        day_and_time_df = day_and_time_df.set_index('dia').reindex(time_slice_counts_per_day_df['dia'].unique()).reset_index()


        
        # ?inplace es True: El DataFrame original se modificará directamente y no se devolverá un nuevo DataFrame
        day_and_time_df.set_index('dia', inplace=True)



        # ?con orient index vas a utilizar el indice como key el resto como value
        json_data_pandas = day_and_time_df.to_json(orient='index')

        #? Load JSON data into a Python dictionary
        attendance_per_day_and_time = json.loads(json_data_pandas)
        return attendance_per_day_and_time


    def get_users_df(self):
        """
        Obtiene los usuarios que su vencimiento sea menor de 4 meses y crea un dataframe.
        
        Returns:
            pandas.DataFrame: DataFrame containing user data.

        """
        four_months_ago = timezone.now() - timedelta(days=30 * 3)
        users =  Usuario.objects.filter(Q(vencimiento__gte=four_months_ago) | Q(vencimiento__isnull=True))
        users_df = pandas.DataFrame(list(users.values()))
        return users_df

    def get_sexo_counts(self, users_df):
        """
        Del dataframe cuenta los valores de la columna sexo y hace un diccionario

        Args:
            users_df (pandas.DataFrame): DataFrame containing user data.

        Returns:
            dict: Dictionary containing counts of 'sexo' values.
        """
        sexo_counts_dict = users_df["sexo"].value_counts().to_dict()
        return sexo_counts_dict

    def get_members_active_counts(self, users_df):
        """
        Cuenta cuantos socios activos e inactivos hay.

        Args:
            users_df (pandas.DataFrame): DataFrame with users data.

        Returns:
            dict: Dictionary containing active and unactive users amount.

        """
        active_and_no_active_members_dict = users_df["activo"].value_counts().to_dict()
        return active_and_no_active_members_dict

    def generate_graphics_data(self):
        """
        Es la función que se encarga de orquestar a las démas funciones, y con solo llamar a esta se pone en marcha a todos los metodos del objeto.

        Returns:
            dict: Dictionary containing statistics.

        """
        asistencias_df= self.get_asistencias_per_week_dataframe()
        missing_dates_index = self.check_missing_dates(asistencias_df)
        time_slice_counts_per_day_df = self.process_time_slices(asistencias_df)

        asistencias_per_month_df = self.get_asistencias_per_month()
        asistencias_per_month_dict = self.get_asistencias_per_month_count(asistencias_per_month_df)
        


        daily_total_arrivals_dict = self.process_daily_total_arrivals(time_slice_counts_per_day_df)

        attendance_per_day_and_time = self.process_attendance_per_day_and_time(time_slice_counts_per_day_df)


        users_df = self.get_users_df()
        sexo_counts_dict = self.get_sexo_counts(users_df)

        active_and_no_active_members_dict = self.get_members_active_counts(users_df)

        
        return {
            "attendance_per_day_and_time": attendance_per_day_and_time,
            "daily_total_arrivals_dict": daily_total_arrivals_dict,
            "sexo_counts_dict": sexo_counts_dict,
            "missing_dates_index":missing_dates_index,
            "asistencias_per_month_dict":asistencias_per_month_dict,
            "active_and_no_active_members_dict": active_and_no_active_members_dict,
        }

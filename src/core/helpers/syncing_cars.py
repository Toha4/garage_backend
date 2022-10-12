from django.core.management.base import OutputWrapper
from django.db import connection
from django.db import connections

from app.helpers.featch_db import dictfetchall

from ..models import Car


class SyncingCars:
    """Cинхронизация ТС из программы Путевки"""

    __db: str = "mssql_sync"
    __connection: connection

    def __init__(self, stdout: OutputWrapper = None):
        self.__connection = connections[self.__db]
        self.__stdout = stdout

    def sync(self):
        cars = self.__get_cars()
        for car in cars:
            self.__update_car(car)

    def __get_cars(self) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(
            "select m.[kod_mar] \
            , t.[GOS_NOM] \
            , RTRIM(m.[name]) as name \
            , CASE \
            WHEN ISNUMERIC(t.[REGION]) <> 1 AND LEN(t.[REGION]) = 3 AND SUBSTRING(t.[REGION], 0, 2) = ' ' THEN SUBSTRING(t.[REGION], 2, 3) + ' ' + t.[GOS_NOM] \
            WHEN ISNUMERIC(t.[REGION]) <> 1 AND LEN(t.[REGION]) = 3 THEN SUBSTRING(t.[REGION], 0, 2) + ' ' + t.[GOS_NOM] + SUBSTRING(t.[REGION], 2, 3) \
            WHEN ISNUMERIC(t.[REGION]) <> 1 AND LEN(t.[REGION]) = 2 THEN t.[REGION] + t.[GOS_NOM] \
            WHEN ISNUMERIC(t.[REGION]) = 1 then t.[REGION] \
            END AS full_gos_nom \
            , t.[KOD_WOD] \
            , t.[DATA_SPIS] \
            from putewka.dbo.marka AS m \
            LEFT JOIN putewka.dbo.TARIF AS t ON (m.kod_mar = t.KOD_MAR) \
            where (t.[DATA_SPIS] IS NULL OR t.[DATA_SPIS] > '2022-09-01') AND t.[NAME] is not null AND LEN(t.[REGION]) > 0 "
        )
        data = dictfetchall(cursor)
        return data

    def __update_car(self, car: dict):
        updated_car = Car.objects.filter(gos_nom_in_putewka=car["GOS_NOM"]).first()
        action_name = ""

        if updated_car:
            updated_car.state_number = car["full_gos_nom"]
            updated_car.kod_driver = car["KOD_WOD"]
            updated_car.date_decommissioned = car["DATA_SPIS"]
            action_name = "обновлен"
        else:
            updated_car = Car(
                kod_mar_in_putewka=car["kod_mar"],
                gos_nom_in_putewka=car["GOS_NOM"],
                state_number=car["full_gos_nom"],
                name=car["name"],
                kod_driver=car["KOD_WOD"],
                date_decommissioned=car["DATA_SPIS"],
            )
            action_name = "добавлен"

        updated_car.save()

        if self.__stdout is not None:
            self.__stdout.write(f"{action_name} - {updated_car.name} ({updated_car.state_number})")

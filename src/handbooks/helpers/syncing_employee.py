from django.core.management.base import OutputWrapper
from django.db import connection
from django.db import connections

from app.helpers.featch_db import dictfetchall

from ..models import Employee


class SyncingEmployee:
    """Cинхронизация работников из программы Кадры"""

    __db: str = "mssql_sync"
    __connection: connection

    def __init__(self, stdout: OutputWrapper = None):
        self.__connection = connections[self.__db]
        self.__stdout = stdout

    def sync(self):
        employees = self.__get_employees()
        for employee in employees:
            self.__update_employee(employee)

    def __get_employees(self) -> list:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT k.[nomer] \
            , RTRIM(k.[fam]) AS last_name \
            , RTRIM(k.[name]) AS first_name\
            , RTRIM(k.[otc]) AS patronymic \
            , RTRIM(ds.[name]) as [position] \
            , kz.[data_uwol] \
            , CASE \
            WHEN (ds.[name] LIKE 'ВОДИТЕЛЬ%' OR ds.[name] LIKE 'МАШИНИСТ%' OR ds.[name] LIKE 'ЭКСКАВАТОРЩИК%') THEN 1 \
            WHEN (ds.[name] LIKE 'СЛЕСАРЬ%' OR ds.[name] LIKE 'СЛ.%') THEN 2 \
            WHEN (ds.[name] LIKE 'НАЧАЛЬНИК%' OR ds.[name] LIKE 'ЗАМ%' OR ds.[name] LIKE 'МЕХАНИК%' \
                OR ds.[name] LIKE 'МАСТЕР%' OR ds.[name] LIKE 'ТЕХНИК%' OR ds.[name] LIKE 'ДИСПЕТЧЕР%') THEN 3 \
            ELSE 2 \
            END AS [type] \
            FROM [soft].[dbo].[kadry] as k \
            LEFT JOIN [zarplata].[dbo].[kadry_z] AS kz ON (kz.nomer = k.nomer) \
            CROSS APPLY (SELECT TOP 1 KOD_DOL FROM [soft].[dbo].[dolj_kad] WHERE NOMER = k.nomer ORDER BY DATA_ DESC) as d \
            LEFT JOIN [soft].[dbo].[dolj_spr] AS ds ON (ds.kod_dol = d.KOD_DOL) \
            WHERE kod_otd = 10 AND (kz.[data_uwol] IS NULL OR kz.[data_uwol] > '2022-09-01') \
                AND (ds.[name] NOT LIKE 'УБОРЩ%' AND ds.[name] NOT LIKE 'СТОРОЖ%' AND ds.[name] NOT LIKE 'ПОДС.%')"
        )
        data = dictfetchall(cursor)
        return data

    def __update_employee(self, employee: dict):
        updated_employee = Employee.objects.filter(number_in_kadry=employee["nomer"]).first()
        action_name = ""

        if updated_employee:
            updated_employee.first_name = employee["first_name"]
            updated_employee.last_name = employee["last_name"]
            updated_employee.patronymic = employee["patronymic"]
            updated_employee.position = employee["position"]
            updated_employee.date_dismissal = employee["data_uwol"]

            if updated_employee.position != employee["position"]:
                updated_employee.type = employee["type"]

            action_name = "обновлен"
        else:
            updated_employee = Employee(
                number_in_kadry=employee["nomer"],
                first_name=employee["first_name"],
                last_name=employee["last_name"],
                patronymic=employee["patronymic"],
                position=employee["position"],
                date_dismissal=employee["data_uwol"],
                type=employee["type"],
            )
            action_name = "добавлен"

        updated_employee.save()

        if self.__stdout is not None:
            self.__stdout.write(f"{action_name} - {updated_employee.short_fio} ({updated_employee.position})")

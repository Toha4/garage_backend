from django.db import models


class EmployeeNote(models.Model):
    employee = models.ForeignKey(
        "core.Employee",
        verbose_name="Работник",
        on_delete=models.PROTECT,
        related_name="notes",
    )
    date = models.DateField(verbose_name="Дата")
    note = models.TextField(verbose_name="Текст")

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.employee.short_fio} ({self.note})"

    class Meta:
        verbose_name = "Заметка по работнику"
        verbose_name_plural = "Заметки по работникам"
        ordering = ("-date", "-pk")

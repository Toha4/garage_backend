from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    initials = models.CharField(_("Инициалы"), max_length=12, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class CustomGroup(models.Model):
    group = models.OneToOneField(
        "auth.Group",
        on_delete=models.CASCADE,
        verbose_name="Группа",
        related_name="custom_group",
    )

    edit_access = models.BooleanField(
        verbose_name="Доступ для редактирование",
        help_text="Отметьте, если группа имеет доступ на редактирование данных.",
        default=False,
    )

    class Meta:
        verbose_name = "Настройки группы"
        verbose_name_plural = "Настройки группы"

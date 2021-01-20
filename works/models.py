from django.db import models

CHOICES = [
    ('PL', u'Подтяжка лица'),
    ('PV', u'Пластика век'),
    ('KPG', 'Контурная пластика губ'),
    ('L', 'Липосакция'),
    ('PJ', 'Пластика живота'),
    ('PG', 'Пластика груди'),
    ('PR', 'Пластика дефектов после огнестрельных ранений'),
    ('PZ', 'Пластика заячьей губы'),
    ('PPR', 'Пластика послеоперационных рубцов'),
    ('PTD', 'Пластика травматических дефектов'),
    ('PPK', 'Пластика послеожоговых контрактур'),
    ('PLS', 'Пластика врожденных ложных суставов'),
    ('PDP', 'Пластика дефектов после удаления опухолей'),
    ('EGS', 'Эндопротезирование груди силиконовыми имплантами'),
    ('MSN', 'Микрохирургический шов повреждений нервов верхней конечности'),
    ('MSS', 'Микрохирургический шов сухожилий кисти'),
    ('XS', 'Хирургическое лечение болей в  кисти'),
    ('XKS', 'Хирургическая коррекция деформаций конечностей при ДЦП детей'),
]


class Works(models.Model):
    opera = models.CharField(max_length=255, verbose_name='Виды операции', choices=CHOICES)
    beforeopera = models.ImageField(verbose_name='Фото до операции')
    afteropera = models.ImageField(verbose_name='Фото после операции')
    name = models.CharField(max_length=50, verbose_name='Имя')

    class Meta:
        verbose_name = "Работы"
        verbose_name_plural = "Работы"


class Blogs(models.Model):
    photo = models.ImageField(verbose_name='Фото блога')
    name_blog = models.CharField(max_length=100, verbose_name='Название блога')
    blog = models.CharField(max_length=1000, verbose_name='Описание блога')
    url_blog = models.CharField(max_length=200, verbose_name='Ссылка блога')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'

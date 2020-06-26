from django.db import models




class Shopdata(models.Model):
    # TODO: Define fields here
    days = models.DateField('日付', blank=True)
    CATEGORY = (
        ('0', '目黒'),
        ('1', '上野広小路'),
        ('2', '神保町白山通り'),
        ('3', '北千住'),
  
    )
    shop = models.CharField('店舗', max_length=10,blank=True, choices=CATEGORY)
    sales = models.IntegerField('売上',blank=True,default="0")
    gest = models.IntegerField('客数' , blank=True,default="0")
    gloup = models.IntegerField('組数',  blank=True,default="0")
    one = models.IntegerField('単価', blank=True,default="0")
    maketime= models.IntegerField('生産性', blank=True,default="0")
    labor  = models.FloatField('人件費率', blank=True,default="0")


    class Meta:
        verbose_name = '計数管理'
        verbose_name_plural = '一覧'

    def __unicode__(self):
        return(self.name)

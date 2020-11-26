from django.db import models

# Create your models here.
class PicManage(models.Model):
    title = models.CharField('标题',max_length=100,default='图片.jpg')
    time = models.DateTimeField('上传时间',auto_now_add=True)
    path = models.CharField('路径',max_length=100)
    isShow = models.CharField('是否显示',max_length=1,choices=(('1','show'),
                                                    ('0','unshow')
                                                    ))
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'图片'
        verbose_name_plural = verbose_name
import xadmin
from servermanager.models import PicManage
from xadmin import views

class GlobalSettings(object):
    site_title = 'Aha?'
    site_footer = "ayjin's website"
    menu_style = 'accordion'
xadmin.site.register(views.CommAdminView,GlobalSettings)

class PicAdmin(object):
    list_display = ('title','time','path','isShow',)
    search_fields = ('title',)
    model_icon = 'fa fa-camera-retro'
    list_per_page = 10
xadmin.site.register(PicManage,PicAdmin)


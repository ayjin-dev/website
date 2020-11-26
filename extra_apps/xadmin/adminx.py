from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin.layout import *

from django.utils.translation import ugettext_lazy as _, ugettext

# 配置后台主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)

# 后台系统名称页脚设置、设置后台菜单为收缩样式
# class GlobalSetting(object):
#     site_title = 'ayjin后台管理'
#     site_footer = 'ayjin.com'
#     menu_style = 'accordion'
#
#
# xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)

class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True

xadmin.site.register(UserSettings, UserSettingsAdmin)

class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), 
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''
    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'


xadmin.site.register(Log, LogAdmin)

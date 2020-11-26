from django.shortcuts import render,render_to_response,HttpResponse
from servermanager.models import PicManage
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    picMsgs = PicManage.objects.all()[:4]#查询前4个
    return render_to_response('index.html',locals())

def pictures(request,num=1):
    #获得全部数据库信息
    queryset = PicManage.objects.all()
    #设置每页12个
    paginator = Paginator(queryset,12)
    #总页数
    pageCount = paginator.num_pages
    #当前页面类
    pageInfo = paginator.get_page(num)
    pageInfo.object_list
    return render_to_response('pictures.html',locals())


def picture(request,name,time,path):
    print(path)
    return render(request,'picture.html',{'ImgLink':path,'ImgName':name,'UploadTime':time})

def test(request,age,name,msg):
    print(age)
    print(name)
    print(msg)
    return HttpResponse(age,name)

def page_not_found(request,exception):
    return render(request,'404.html')
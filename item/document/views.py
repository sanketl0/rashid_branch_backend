from django.shortcuts import render
from django.http import HttpResponse
from .models import Doc


# Create your views here.
def home(request):
    context={'file':Doc.objects.all()}
    return render(request, 'document/home.html', context)

def download(request, path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response=HttpResponse(fh.read(),context_type="application/uploadfile")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404

	
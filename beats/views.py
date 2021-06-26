from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage


class Home(TemplateView):
    template_name = 'beats/home.html'


def upload(request):
    context = {}

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()

        # Get updated name of file in case of same-name upload
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

    return render(request, 'beats/upload.html', context)


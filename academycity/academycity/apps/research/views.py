from django.shortcuts import render
from .forms import InputFileForm
from .models import InputFiles
from django.conf import settings
from .potential import ProcessData
import shutil


def potential(request):
    if request.method == 'POST':
        form = InputFileForm(request.POST, request.FILES)
        if form.is_valid():
            data_dir = settings.MEDIA_ROOT + '/research/potential'
            try:
                shutil.rmtree(data_dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

            input_files = InputFiles(user=request.user, title = request.POST.get('title'), file = request.FILES['file'])
            k = input_files.save()
            pd_ = ProcessData(file_name=input_files.file.name)  # , 'Y_1986.xlsx'
            pd_.main()
            pd_.compress()
            input_files.file_result = pd_.gz_file_table
            input_files.save()
    form = InputFileForm()
    # else:
    #     form = InputFileForm()
    researches = InputFiles.objects.filter(user=request.user).all()
    return render(request, 'research/_research_potential.html', {'form': form, 'researches': researches})


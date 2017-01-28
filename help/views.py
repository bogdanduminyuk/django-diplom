from django.shortcuts import render


def common(request):
    return render(request, 'help/common_help.html', {
        'title': 'Справка по проекту',
        'page_header': 'Справка по проекту',
        'panel_heading': 'Общая справка по данному проекту',
        'panel_type': 'panel-info',
    })


def adaptation(request):
    return render(request, 'help/common_help.html', {})


def generation(request):
    return render(request, 'help/common_help.html', {})

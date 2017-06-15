from django.shortcuts import render


def common_help(request):
    return render(request, 'help/common_help.html', {
        'title': 'Справка по проекту',
        'page_header': 'Справка по проекту',
        'panel_heading': 'Общая справка по данному проекту',
        'panel_type': 'panel-info',
    })


def adaptation_help(request):
    return render(request, 'help/common_help.html', {
        'title': 'Справка по адаптации',
        'page_header': 'Справка по адаптации (Наполнить контентом)',
        'panel_heading': 'Общая справка по данному проекту',
        'panel_type': 'panel-info',
    })


def generation_help(request):
    return render(request, 'help/common_help.html', {
        'title': 'Справка по генерации',
        'page_header': 'Справка по генерации (Наполнить контентом)',
        'panel_heading': 'Общая справка по данному проекту',
        'panel_type': 'panel-info',
    })

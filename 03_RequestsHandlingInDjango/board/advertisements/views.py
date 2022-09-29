from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class Advertisement(View):
    count = 0
    advertisements = ['Мастер на час', 'Выведение из запоя',
                      'Услуги экскаватора-погрузчика', 'Услуги гидромолота',
                      'Услуги ямобура']

    def get(self, request):
        return render(request, 'advertisements/advertisement_list.html',
                      {'advertisements': self.advertisements,
                       'count': Advertisement.count})

    def post(self, response):
        Advertisement.count += 1
        message = 'Запрос на создание новой записи успешно выполнен'
        return render(response, 'advertisements/advertisement_list.html',
                      {'advertisements': self.advertisements,
                       'count': Advertisement.count,
                       'message': message})


class Contacts(TemplateView):
    template_name = 'advertisements/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = 'Ленинский просп., 6, стр. 20, Москва'
        context['mail'] = 'skillbox@skillbox.ru'
        context['phone'] = '+7 (495) 291-70-59'

        return context


class AboutUs(TemplateView):
    template_name = 'advertisements/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = 'Skillbox'
        context['text'] = 'Skillbox – это онлайн платформа дистанционного обучения, ' \
                          'ориентированная на цифровые и ИТ-специальности. В активе более 300 образовательных программ, ' \
                          '63 тыс. студентов обучаются на курсах. Для ознакомления с курсами и получения представления о ' \
                          'профессиях предлагаются бесплатные вебинары.'

        return context


class HomePage(TemplateView):
    template_name = 'advertisements/homepage.html'
    categories = {'О нас': '/about', 'Контакты': '/contacts', 'Доска объявлений': '/advertisement'}
    regions = ['Москва', 'Санкт-Петербург', 'Нижегородская область', 'Волгоградская область', 'другое']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HomePage.categories
        context['regions'] = HomePage.regions

        return context
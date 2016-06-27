from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from .models import People
from .forms import FormPeople
import requests
import json
import random
from django.utils.translation import ugettext_lazy as _


class PeopleList(View):
    people_list = []
    template_name = 'core/people_list.html'

    def get(self, request, *args, **kwargs):
        query = Q()
        if request.GET.get('term', False):
            query = Q(name__icontains=request.GET['term'])
        peoples = People.objects.filter(query)
        paginator = Paginator(peoples, 100)
        page = int(request.GET.get('page', 1))

        try:
            self.people_list = paginator.page(page)
        except (EmptyPage, InvalidPage):
            self.people_list = paginator.page(paginator.num_pages)

        response = {
            'people_list': self.people_list,
            'actual': page, 'total': paginator.num_pages,
            'next': page + 1, 'prev': page - 1,
            'list_pages': range(1, paginator.num_pages + 1),
            'st': request.GET.get('st', '0')}

        return render(request, self.template_name, response)


class PeopleCreate(View):
    form_class = FormPeople
    initial = {}
    template_name = 'core/people_form.html'

    try:
        r = requests.get('http://api.randomuser.me/')
        data = json.loads(r.text)
        data = data['results'][0]
        initial = {
            'name': "%s %s" % (data['name']['first'], data['name']['last']),
            'photo': data['picture']['medium'],
            'age': random.randrange(0, 120)}
    except Exception as e:
        print(e)
        # raise e

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(
            request, self.template_name,
            {'form': form, 'name_form': _('New people')})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            people = People(
                name=data['name'], age=data['age'], photo=data['photo'])
            people.save()
            return HttpResponseRedirect('/?st=2')

        return render(
            request, self.template_name,
            {'form': form, 'name_form': _('New people')})


class PeopleUpdate(View):
    form_class = FormPeople
    template_name = 'core/people_form.html'

    def get(self, request, *args, **kwargs):
        self.initial = get_object_or_404(People, pk=kwargs['pk'])
        form = self.form_class(initial=self.initial.__dict__)
        return render(
            request, self.template_name,
            {'form': form, 'name_form': _("Update people")})

    def post(self, request, *args, **kwargs):
        self.people = get_object_or_404(People, pk=kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            self.people.name = data['name']
            self.people.age = data['age']
            self.people.photo = data['photo']
            self.people.save()
            return HttpResponseRedirect('/?st=3')

        return render(
            request, self.template_name,
            {'form': form, 'name_form': _('New people')})


class PeopleDelete(DeleteView):
    model = People
    success_url = '/?st=1'


class PeopleDetail(DetailView):
    context_object_name = 'people'
    queryset = People.objects.all()


class AutoComplete(View):
    def get(self, request, *args, **kwargs):
        query = Q()
        if request.GET.get('term', False):
            query = Q(name__icontains=request.GET['term'])
        peoples = People.objects.filter(query)
        dados = [{'id': people.id, 'name': people.name} for people in peoples]
        mimetype = "application/json;charset=UTF-8"
        js = json.dumps(dados, ensure_ascii=False).encode('utf8')
        return HttpResponse(js, mimetype)

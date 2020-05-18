from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LinkCreationForm
from django.views.generic.edit import FormView
from .models import *


class MainView(FormView):
    template_name = 'main_page.html'
    form_class = LinkCreationForm
    success_url = '/result/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link_list'] = Link.objects.all().order_by('-redirects')
        return context

    def form_valid(self, form):
        new_link = Link(full_link=form.cleaned_data['link'], redirects=0)
        new_link.save()
        new_link.generate_shortened_link().save(force_update=True)
        return redirect(new_link)


def result(request, link_id):
    link = request.build_absolute_uri(Link.objects.get(id=link_id).shortened_link)
    return HttpResponse("Your link is: <a href='%s'>%s</a>" % (link, link))


def redirect_view(request, short_link):
    link = Link.objects.get(shortened_link__contains=short_link)
    link.redirects += 1
    link.save(force_update=True)
    link = link.full_link
    return HttpResponseRedirect(str(link))

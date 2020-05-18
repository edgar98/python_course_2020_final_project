from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LinkCreationForm
from django.views.generic.edit import FormView
from .models import *


"""Views in Linker app"""


class MainView(FormView):
    """Main page view

        This class renders main page of project. That page contains:
            -   Input field for user's link
            -   A button to sent that link
            -   List of short links ordered by their redirects counts
    """
    template_name = 'main_page.html'  # Template used to render result
    form_class = LinkCreationForm  # Form to create Link object

    def get_context_data(self, **kwargs):
        """Create context for template

        This method adds list of links to template context
        """
        context = super().get_context_data(**kwargs)  # Call super method first
        context['link_list'] = Link.objects.all().order_by('-redirects')  # Add list of links to context
        return context

    def form_valid(self, form):
        """Creates Link model after form sent

        This method is invoked while user sent form with link

        :returns: Redirect to success page"""
        new_link = Link(full_link=form.cleaned_data['link'], redirects=0)  # Create new Link object
        new_link.save()  # Save it to DB to get ID
        new_link.generate_shortened_link().save(force_update=True)  # Generate short link and save result
        return redirect(new_link)


def result(request, link_id):
    """Method-view for success page

    This method renders success page for new short link
    :param request: HTTP request object
    :param link_id: ID of Link object from DB, parsed from urls.py
    :return: HttpResponse (Page with new link)
    """
    link = request.build_absolute_uri(Link.objects.get(id=link_id).shortened_link)
    return HttpResponse("Your link is: <a href='%s'>%s</a>" % (link, link))


def redirect_view(request, short_link):
    """Serves redirects from short links

    This method is used to handle redirects to Links' full links.
    It also increment redirects counter in Link model object.
    :param request: HTTP request object
    :param short_link: Short link string, parsed from urls.py
    :type short_link: str
    :return: Redirect to model's full link
    """
    link = Link.objects.get(shortened_link__contains=short_link)  # Find link object to get full URL to redirect
    link.increment_redirects() # Increment redirects counter
    link.save(force_update=True)  # Save changes
    link = link.full_link  # Get Link object's full link
    return HttpResponseRedirect(str(link))

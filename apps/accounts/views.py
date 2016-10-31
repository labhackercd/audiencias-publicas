from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from .forms import SignUpForm


class SignUpView(TemplateView):
    http_method_names = [u'post', u'get']
    template_name = "registration/signup.html"

    def post(self, request):
        user_form = SignUpForm(request.POST)

        if not user_form.is_valid():
            errors = []
            for error in user_form.errors.values():
                errors.append(error[0])
            context = {'errors': errors}
            return TemplateResponse(request, self.template_name, context)

        user = user_form.save(commit=False)

        user.is_active = True
        user.set_password(user_form.cleaned_data['password'])
        user.save()

        return redirect(reverse('home'))

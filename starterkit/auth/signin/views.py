from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context

    def post(self,request):
   
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            success_message = "Login successful"
            return HttpResponse(success_message)

        else:
            error_message = "Invalid username or password. Please try again."
            return JsonResponse({'success': False, 'message': error_message}, status=500)

            # error_message = "Invalid username or password. Please try again."
            # return HttpResponse(error_message)

        return render(request, 'login.html')
    



def logout_req(request):
     logout(request)
     return redirect('/signin')


class AuthverificationView(TemplateView):
    template_name = 'pages/auth/verification.html'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)

    #     # A function to init the global layout. It is defined in _keenthemes/__init__.py file
    #     context = KTLayout.init(context)

    #     KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')

    #     # Define the layout for this module
    #     # _templates/layout/auth.html
    #     context.update({
    #         'layout': KTTheme.setLayout('auth.html', context),
    #     })

    #     return context
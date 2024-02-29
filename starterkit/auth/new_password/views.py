from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
import base64
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthNewPasswordView(TemplateView):
    template_name = 'pages/auth/new-password.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/reset-password/new-password.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context

    # def get(self, request, user_id, *args, **kwargs):
    #     user_id_bytes = base64.b64decode(user_id.encode('utf-8'))
    #     user_id = int(user_id_bytes.decode('utf-8'))
    #     return render(request,"pages/auth/new-password.html",{'user_id':user_id})
        
        # Assuming you want to return JSON with the user_id
        # return JsonResponse({'user_id': user_id})

    def post(self, request, user_id, *args, **kwargs):

        user_id_bytes = base64.b64decode(user_id.encode('utf-8'))
        user_id = int(user_id_bytes.decode('utf-8'))
        # user_id =  int(user_id.decode('utf-8'))
        user = User.objects.get(id=user_id)
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()

        # Assuming you want to return JSON with a success message
        return JsonResponse({'message': 'Password reset successful. You can now log in with your new password.'})
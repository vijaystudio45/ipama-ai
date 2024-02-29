from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse,JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
import base64
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthResetPasswordView(TemplateView):
    template_name = 'pages/auth/reset-password.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/reset-password/reset-password.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context
    
    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_message = {"error": "User with this email does not exist."}
            return JsonResponse(error_message, status=400)

        else:
            self.send_reset_email(request, user)
        success_message = {"msg" :"Password reset email has been sent."}
        return JsonResponse(success_message , status=200)

        # messages.success(request, "Password reset email has been sent.")
        # return redirect('password_reset')

    def send_reset_email(self, request, user):
        user_id_bytes = str(user.id).encode('utf-8')

        encoded_user_id = base64.b64encode(user_id_bytes).decode('utf-8')
        print(encoded_user_id,'encoded_user_idencoded_user_id')
        reset_url = reverse('auth:password_reset_confirm', kwargs={'user_id': encoded_user_id})

        subject = 'Password Reset'
        message = render_to_string('pages/auth/password_reset_email.txt', {
            'user': user,
            'reset_url': request.build_absolute_uri(reset_url),
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

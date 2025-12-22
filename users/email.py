from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    template_name = "emails/activation_email.html"


class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = "emails/password_reset_email.html"


class CustomUsernameResetEmail(email.UsernameChangedConfirmationEmail):
    template_name = "emails/username_reset_email.html"

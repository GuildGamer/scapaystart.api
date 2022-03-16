from django.db import models


class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField("name", max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = self.email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

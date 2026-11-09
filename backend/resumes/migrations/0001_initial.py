from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="CV", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(default="My CV", max_length=160)),
            ("language", models.CharField(choices=[("en","English"),("de","Deutsch")], default="en", max_length=2)),
            ("template", models.CharField(choices=[("modern","Modern"),("classic","Classic")], default="modern", max_length=20)),
            ("data", models.JSONField(blank=True, default=dict)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cvs", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering":["-updated_at"]}),
    ]

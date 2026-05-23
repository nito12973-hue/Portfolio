from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileInfo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Lamarana Diallo", max_length=100)),
                ("title", models.CharField(default="Développeur Web & Bases de données", max_length=150)),
                ("subtitle", models.CharField(
                    default="Étudiant en informatique spécialisé en bases de données et en développement web/mobile.",
                    max_length=250,
                )),
                ("bio", models.TextField(
                    default="Je combine la conception d’interfaces modernes avec la sécurisation et l’optimisation des données."
                )),
                ("avatar_url", models.URLField(default="/static/images/avatar.svg")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Profil", "verbose_name_plural": "Profils"},
        ),
        migrations.CreateModel(
            name="SkillCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=80)),
                ("icon_class", models.CharField(default="bi-code-slash", max_length=80)),
                ("skills_text", models.TextField(blank=True, default="")),
            ],
        ),
    ]

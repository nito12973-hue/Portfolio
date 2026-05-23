# Portfolio Django — Lamarana Diallo

Ce dépôt contient un portfolio développeur modernisé avec Django 5. Tout le contenu public (hero, projets, compétences, formation, contact) est alimenté depuis des modèles Django et administré depuis l'interface `/admin`. Le design repose sur des styles personnalisés (CSS + JS) et la structure respecte les conventions Django : `static/`, `templates/`, une app `portfolio` dédiée, des vues simples et des modèles explicites.

## Fonctionnalités

- **Pages publiques** : Accueil, À propos, Compétences, Projets, Formation et Contact avec formulaire sauvegardé en base.
- **Modèles dynamiques** : `Profile`, `Skill`, `Project`, `Education`, `Interest` et `ContactMessage` gèrent toute la donnée côté serveur. Chaque projet conserve les technologies, un lien, une image et un flag “mis en avant”.
- **Administration** : Django Admin permet d'éditer le profil, les compétences, les projets, la formation et de consulter les messages reçus.
- **UI moderne** : base CSS personnalisée, mode sombre activable, cartes, badges et formulaire responsive. Le site n'utilise plus Bootstrap/JS externes pour éviter les soucis de `collectstatic`.
- **Formulaire de contact** : les messages sont persistés côté serveur et déclenchent une notification utilisateur grâce au framework `messages`.
- **Déploiement prêt pour Render** : `render.yaml`, `Dockerfile` et `Procfile` inclus ; la configuration se concentre sur `python manage.py migrate`, `collectstatic` et `gunicorn`.

## Structure

```
.
├── manage.py
├── portfolio_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── context_processors.py
├── templates/
│   ├── base.html
│   └── home/
│       ├── index.html
│       ├── about.html
│       ├── projects.html
│       ├── skills.html
       ├── formation.html
       └── contact.html
├── static/
│   ├── css/main.css
│   ├── js/main.js
│   └── images/avatar-placeholder.svg
├── db.sqlite3
├── render.yaml
├── Dockerfile
└── requirements.txt
```

## Models et données

- `Profile` : nom, titre, description, email, téléphone, GitHub, localisation, avatar et horodatage. La méthode `get_solo()` garantit une instance unique.
- `Skill` : nom, catégorie et ordre afin de produire des regroupements par catégorie dans les vues.
- `Project` : titre, description, image, technologies (JSON), lien, flag `featured` et dates (création/mise à jour).
- `Education` & `Interest` : listes d'items ordonnés pour les pages formation / centres d'intérêt.
- `ContactMessage` : nom, email, message et date d'envoi ; utilisé par le formulaire de contact.

## Templates & static

- `base.html` : navigation fixe, toggler de thème, footer avec contacts et inclusion de `css/main.css` + `js/main.js`.
- Pages `home/index.html`, `home/about.html`, `home/skills.html`, `home/projects.html`, `home/formation.html`, `home/contact.html` qui affichent respectivement hero, résumé, compétences, projets, formation et formulaire de contact.
- `static/css/main.css` contient le thème sombre clair, les cartes, badges, grilles et animations légères.
- `static/js/main.js` gère le mode sombre automatique et le lissage de scroll.

## Commandes usuelles

```bash
python -m venv .venv
.venv\\Scripts\\activate        # Windows
source .venv/bin/activate      # macOS / Linux
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Le formulaire de contact et les compétences peuvent être alimentés directement depuis `/admin` après avoir créé un superuser.

## Préparer un déploiement Render

- Le `render.yaml` installe les dépendances, lance les migrations et collecte les statiques : `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`.
- Le `Dockerfile` (optionnel) fait la même chose puis démarre `gunicorn portfolio_project.wsgi`.
- Sur Render, définissez `DJANGO_SECRET_KEY` et `DJANGO_DEBUG=0` dans les variables d'environnement.
- Le `Procfile` expose `web: gunicorn portfolio_project.wsgi --bind 0.0.0.0:$PORT`.

## Notes complémentaires

- Les uploads de photos/repos sont stockés dans `media/` (configurée via `MEDIA_ROOT`/`MEDIA_URL`).
- Pour réinitialiser les données, supprimez `db.sqlite3` puis relancez `makemigrations` + `migrate`.
- Le thème est sauvegardé en localStorage pour restaurer le dernier choix utilisateur entre sessions.

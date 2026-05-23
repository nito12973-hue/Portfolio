from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


OUTPUT = Path(__file__).with_name("guide_deploiement_portfolio.pdf")


def bullet_items(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=12) for item in items],
        bulletType="bullet",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=8,
    )


def numbered_items(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=12) for item in items],
        bulletType="1",
        leftIndent=18,
    )


def add_title(story, text, style):
    story.append(Paragraph(text, style))
    story.append(Spacer(1, 0.25 * cm))


def main():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=12,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=18,
    )
    h1 = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#2563eb"),
        spaceBefore=12,
        spaceAfter=6,
    )
    h2 = ParagraphStyle(
        "SubSectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#111827"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#111827"),
        spaceAfter=6,
    )
    code = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        backColor=colors.HexColor("#f3f4f6"),
        borderColor=colors.HexColor("#e5e7eb"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=8,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#6b7280"),
    )

    story = []
    story.append(Paragraph("Guide de deploiement d'un portfolio Django sur Render", title))
    story.append(
        Paragraph(
            "Ce document resume les actions realisees sur le projet Portfolio et donne une methode simple pour redeployer un site web une prochaine fois.",
            subtitle,
        )
    )

    add_title(story, "1. Ce qui a ete fait sur ce projet", h1)
    story.append(
        bullet_items(
            [
                "Correction des erreurs Django et verification des pages principales.",
                "Remplacement des anciens projets par les vrais projets publics du compte GitHub nito12973-hue.",
                "Preparation de la configuration de production pour Render.",
                "Ajout de WhiteNoise pour servir les fichiers statiques en production.",
                "Creation d'un commit Git puis push vers GitHub.",
                "Creation d'un service Render Python appele portfolio-django.",
                "Verification du site deploye sur l'URL publique Render.",
            ],
            body,
        )
    )

    add_title(story, "2. Fichiers importants", h1)
    story.append(
        bullet_items(
            [
                "<b>requirements.txt</b> : liste les dependances Python, dont Django, Gunicorn, Pillow et WhiteNoise.",
                "<b>portfolio_project/settings.py</b> : contient la configuration Django, les fichiers statiques et les hôtes autorises.",
                "<b>render.yaml</b> : indique a Render comment construire et lancer le site.",
                "<b>Procfile</b> : commande de demarrage compatible avec les plateformes type Render/Heroku.",
                "<b>portfolio/fixtures/projects.json</b> : projets charges dans la base au deploiement.",
            ],
            body,
        )
    )

    add_title(story, "3. Preparation Django pour la production", h1)
    story.append(Paragraph("Les points essentiels a verifier avant un deploiement Django :", body))
    story.append(
        numbered_items(
            [
                "Mettre <b>DEBUG=0</b> en production.",
                "Renseigner <b>DJANGO_SECRET_KEY</b> avec une valeur secrete.",
                "Autoriser le domaine de production dans <b>DJANGO_ALLOWED_HOSTS</b>.",
                "Installer et configurer <b>WhiteNoise</b> pour les fichiers statiques.",
                "Lancer les migrations et collecter les fichiers statiques pendant le build.",
            ],
            body,
        )
    )
    story.append(Paragraph("Dependances utilisees :", h2))
    story.append(
        Paragraph(
            "django&gt;=5.0,&lt;6.0<br/>gunicorn&gt;=22.0.0<br/>Pillow&gt;=10.0<br/>whitenoise&gt;=6.6.0",
            code,
        )
    )

    add_title(story, "4. Configuration Render utilisee", h1)
    story.append(
        Paragraph(
            "Commande de build configuree sur Render :",
            body,
        )
    )
    story.append(
        Paragraph(
            "pip install -r requirements.txt &amp;&amp; python manage.py migrate &amp;&amp; python manage.py loaddata projects &amp;&amp; python manage.py collectstatic --noinput",
            code,
        )
    )
    story.append(Paragraph("Commande de demarrage :", body))
    story.append(
        Paragraph(
            "gunicorn portfolio_project.wsgi --bind 0.0.0.0:$PORT",
            code,
        )
    )
    story.append(Paragraph("Variables d'environnement importantes :", body))
    story.append(
        bullet_items(
            [
                "<b>DJANGO_SECRET_KEY</b> : cle secrete Django, ne jamais publier.",
                "<b>DJANGO_DEBUG</b> : mettre 0 en production.",
                "<b>DJANGO_ALLOWED_HOSTS</b> : mettre .onrender.com ou ton domaine personnalise.",
            ],
            body,
        )
    )

    add_title(story, "5. Etapes pour redeployer soi-meme", h1)
    story.append(
        numbered_items(
            [
                "Faire les modifications dans le projet local.",
                "Tester avec <b>python manage.py check</b>.",
                "Tester les pages principales en local si possible.",
                "Ajouter les fichiers avec <b>git add -A</b>.",
                "Creer un commit avec <b>git commit -m \"Message clair\"</b>.",
                "Envoyer sur GitHub avec <b>git push origin main</b>.",
                "Render detecte le push et lance un nouveau deploiement automatiquement si auto-deploy est active.",
                "Ouvrir l'URL Render et verifier les pages principales.",
            ],
            body,
        )
    )

    add_title(story, "6. Creation d'un nouveau service Render", h1)
    story.append(Paragraph("Si tu dois creer un nouveau site depuis zero sur Render :", body))
    story.append(
        numbered_items(
            [
                "Aller sur https://dashboard.render.com/.",
                "Cliquer sur <b>New +</b>, puis choisir <b>Web Service</b> ou <b>Blueprint</b>.",
                "Connecter le depot GitHub.",
                "Choisir le depot et la branche <b>main</b>.",
                "Choisir le runtime <b>Python</b>.",
                "Renseigner la commande de build et la commande de demarrage.",
                "Ajouter les variables d'environnement.",
                "Lancer le deploiement.",
            ],
            body,
        )
    )

    story.append(PageBreak())
    add_title(story, "7. Commandes utiles", h1)
    story.append(Paragraph("Verifier Django :", body))
    story.append(Paragraph("python manage.py check", code))
    story.append(Paragraph("Appliquer les migrations :", body))
    story.append(Paragraph("python manage.py migrate", code))
    story.append(Paragraph("Charger les projets :", body))
    story.append(Paragraph("python manage.py loaddata projects", code))
    story.append(Paragraph("Collecter les fichiers statiques :", body))
    story.append(Paragraph("python manage.py collectstatic --noinput", code))
    story.append(Paragraph("Publier sur GitHub :", body))
    story.append(Paragraph("git add -A<br/>git commit -m \"Deploy Django portfolio\"<br/>git push origin main", code))

    add_title(story, "8. Verification apres deploiement", h1)
    story.append(
        bullet_items(
            [
                "La page d'accueil doit repondre avec un statut 200.",
                "La page /projets/ doit afficher les projets reels comme SunuMarket.",
                "La page /contact/ doit s'ouvrir sans erreur.",
                "Les fichiers CSS, images et scripts doivent charger correctement.",
                "Si le site affiche une erreur 500, regarder les logs Render.",
            ],
            body,
        )
    )

    add_title(story, "9. Resultat de ce deploiement", h1)
    story.append(
        bullet_items(
            [
                "Service Render cree : <b>portfolio-django</b>.",
                "URL publique : <b>https://portfolio-django-8oqq.onrender.com/</b>.",
                "Commit deploye : <b>6ad30da Deploy Django portfolio</b>.",
                "Pages verifiees : accueil, /projets/ et /contact/.",
            ],
            body,
        )
    )

    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Paragraph(
            "Note securite : apres avoir utilise une cle API Render, il faut la supprimer ou la regenerer depuis le tableau de bord Render.",
            small,
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Guide de deploiement Portfolio Django",
        author="Codex",
    )
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    main()

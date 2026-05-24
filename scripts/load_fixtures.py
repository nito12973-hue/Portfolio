import os
import json
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
import django
django.setup()
from portfolio.models import Skill, Interest, Project

# Load skills and interests
fixture_path = os.path.join(os.path.dirname(__file__), '..', 'portfolio', 'fixtures', 'skills_interests.json')
fixture_path = os.path.abspath(fixture_path)

print('Loading fixtures from', fixture_path)

# Try utf-16 then utf-8
for enc in ('utf-16', 'utf-8'):
    try:
        with open(fixture_path, 'r', encoding=enc) as f:
            data = json.load(f)
        print('Loaded JSON with encoding', enc)
        break
    except Exception as e:
        print('Failed to read with', enc, e)
        data = None

if not data:
    print('Could not read fixture file. Exiting.')
    sys.exit(1)

# Load projects
projects_fixture_path = os.path.join(os.path.dirname(__file__), '..', 'portfolio', 'fixtures', 'projects.json')
projects_fixture_path = os.path.abspath(projects_fixture_path)

print('Loading projects fixtures from', projects_fixture_path)

projects_data = None
for enc in ('utf-16', 'utf-8'):
    try:
        with open(projects_fixture_path, 'r', encoding=enc) as f:
            projects_data = json.load(f)
        print('Loaded projects JSON with encoding', enc)
        break
    except Exception as e:
        print('Failed to read projects with', enc, e)

if projects_data:
    data.extend(projects_data)

created = 0
for obj in data:
    model = obj.get('model', '').lower()
    fields = obj.get('fields', {})
    try:
        if model.endswith('skill'):
            name = fields.get('name')
            category = fields.get('category', 'Général')
            order = fields.get('order', 0)
            if not Skill.objects.filter(name=name, category=category).exists():
                Skill.objects.create(name=name, category=category, order=order)
                created += 1
        elif model.endswith('interest'):
            name = fields.get('name')
            order = fields.get('order', 0)
            if not Interest.objects.filter(name=name).exists():
                Interest.objects.create(name=name, order=order)
                created += 1
        elif model.endswith('project'):
            title = fields.get('title')
            description = fields.get('description', '')
            technologies = fields.get('technologies', [])
            link = fields.get('link', '')
            featured = fields.get('featured', False)
            if not Project.objects.filter(title=title).exists():
                Project.objects.create(title=title, description=description, technologies=technologies, link=link, featured=featured)
                created += 1
    except Exception as e:
        print('Error creating', model, e)

print('Created', created, 'objects')

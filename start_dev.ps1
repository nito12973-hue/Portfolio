if (-not (Test-Path -Path ".venv")) {
    python -m venv .venv
}

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned | Out-Null
& .venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata portfolio/fixtures/projects.json

python manage.py runserver

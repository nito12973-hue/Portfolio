# Lamarana Diallo — Portfolio (ASP.NET Core MVC)

Ce projet est un portfolio personnel complet : accueil, compétences, projets, formation, contact.
Les contenus dynamiques (profil et projets) sont stockés dans `data/` sous forme JSON et peuvent être
modifiés via de simples formulaires protégés par une clé `AdminKey`.

## Structure principale

- **Pages publiques** : `HomeController` alimente les vues `Views/Home/*` pour afficher l’accueil,
  le parcours, les compétences, les projets, la formation et le contact avec le style Bootstrap personnalisé.
- **Services** :
  - `JsonProjectRepository` gère `data/projects.json`, avec des valeurs initiales et l’ajout de nouveaux projets.
  - `JsonProfileRepository` gère `data/profile.json` pour les textes d’accueil et l’avatar.
  - Le filtre `ProfileDataFilter` injecte `ViewBag.ProfileData` dans chaque vue pour utiliser les données dynamiques.
- **Sécurité simple** :
  - L’attribut `[AdminKey]` protège les contrôleurs `ProjectAdminController` et `ProfileAdminController`.
  - La clé est définie via `appsettings*.json` (`AdminKey`) ou via une variable d’environnement `AdminKey`.

## Ajouter / modifier le profil

1. Place ton avatar dans `wwwroot/images` (ex. `/images/lama.png`).  
2. Ouvre `/ProfileAdmin/Edit?key=dev-portfolio-admin` (remplace la valeur par ta clé si tu la changes).  
3. Saisis ton nom, titre, sous-titre, bio et URL de l’avatar.  
4. Envoi -> les données sont sauvegardées dans `data/profile.json` et mises à jour sur la homepage (bouton crayon).  
5. Tu peux aussi ajouter la clé dans l’en-tête `X-Admin-Key` au lieu de la query string.

## Ajouter un projet déployé

1. Accède à `/ProjectAdmin/Create?key=dev-portfolio-admin`.  
2. Renseigne titre, description, technologies (virgule) et lien GitHub/demo.  
3. Coche « Mettre en avant » si tu veux voir ce projet dans la section “Focus” de la homepage.  
4. Les projets sont ajoutés à `data/projects.json` et apparaissent immédiatement sur `/Home/Projects` et sur la carte “Projets récents”.

## Données persistées

- `data/projects.json` — liste des `ProjectCard` visibles côté front.  
- `data/profile.json` — informations du profil affichées sur l’accueil.
- Chaque repository veille à créer le dossier `data` et à initialiser les fichiers s’ils n’existent pas.

## Clé `AdminKey`

- Valeur par défaut (à remplacer pour la prod) : `dev-portfolio-admin`.  
- Défini dans `appsettings.json`, `appsettings.Development.json` ou via `AdminKey` en variable d’environnement.  
- Tu peux passer la clé dans la query (`?key=…`) ou l’en-tête HTTP `X-Admin-Key`.
- Sans la clé valide, les routes `/ProjectAdmin/Create` et `/ProfileAdmin/Edit` retournent `401 Unauthorized`.

## Exécution

```bash
dotnet build
dotnet run
```

Le site utilise Bootstrap + Bootstrap Icons et tourne en ASP.NET Core 9.0.

## Prochaines étapes

- Changer la clé `AdminKey` avant un déploiement public et l’injecter via les secrets ou un pipeline.  
- Prévoir éventuellement une authentification plus complète (Azure AD, IdentityServer, etc.) si plusieurs contributeurs doivent éditer le contenu depuis le web.  
- Ajouter une page “Dashboard” listant les projets avec options d’édition/suppression si tu veux aller plus loin.

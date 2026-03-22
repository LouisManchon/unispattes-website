# 🐾 Unis'Pattes — Application web complète


## 📋 Présentation du projet

**Unis'Pattes** est une application web permettant à un refuge animalier de présenter ses animaux à l'adoption et de recevoir des demandes d'adoption en ligne.

### Fonctionnalités principales

- Consultation des animaux disponibles avec filtrage dynamique (espèce, âge, sexe, race)
- Fiche détaillée par animal avec formulaire de demande d'adoption
- Système d'authentification complet (inscription, connexion, déconnexion)
- Interface d'administration pour gérer les animaux et traiter les demandes
- Accès différencié : visiteur (consultation) / utilisateur connecté (soumission de demande)

---

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Back-end | Django 6.0 (Python 3.12) |
| Front-end | HTML5, CSS3, JavaScript vanilla |
| Base de données | MySQL 8.0 |
| Environnement | Docker + Docker Compose |
| Versioning | Git / GitHub |
| Serveur | Django runserver (dev) |

---

## 📁 Structure du projet
```
unispattes-website/
├── backend/
│   ├── animaux/                  # App principale
│   │   ├── migrations/           # 6 migrations
│   │   ├── static/animaux/       # CSS, JS, images
│   │   ├── templates/animaux/    # index, nos_animaux, detail_animal, a_propos
│   │   ├── models.py             # Animal, DemandeAdoption
│   │   ├── views.py              # Vues principales
│   │   ├── forms.py              # DemandeAdoptionForm
│   │   ├── admin.py              # Admin personnalisé
│   │   └── urls.py
│   ├── users/                    # App authentification
│   │   ├── migrations/           # 3 migrations
│   │   ├── templates/users/      # login, register
│   │   ├── models.py             # Utilisateur custom
│   │   ├── views.py              # inscription, connexion, déconnexion
│   │   ├── forms.py              # InscriptionForm, ConnexionForm
│   │   └── urls.py
│   ├── config/                   # Configuration Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── media/                    # Photos uploadées via l'admin
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yml
├── .env                          # Variables d'environnement (non versionné)
└── README.md
```

---

## ⚙️ Prérequis

- [Docker](https://www.docker.com/) (version 20+)
- [Docker Compose](https://docs.docker.com/compose/) (version 2+)
- [Git](https://git-scm.com/)

---

## 🚀 Installation et lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/unispattes-website.git
cd unispattes-website
```

### 2. Créer le fichier `.env`

Créez un fichier `.env` à la racine du projet :
```env
SECRET_KEY=votre_clé_secrète
DEBUG=1

DB_NAME=unispattes_db
DB_USER=unispattes_user
DB_PASSWORD=votre_mot_de_passe
DB_HOST=db
DB_PORT=3306

MYSQL_DATABASE=unispattes_db
MYSQL_USER=unispattes_user
MYSQL_PASSWORD=votre_mot_de_passe
MYSQL_ROOT_PASSWORD=votre_mot_de_passe_root
```

> ⚠️ Ne jamais commiter le fichier `.env` — il doit être dans `.gitignore`

### 3. Lancer les conteneurs
```bash
docker-compose up --build
```

### 4. Créer un superutilisateur
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 5. (Optionnel) Charger les données de démonstration
```bash
docker-compose exec backend python manage.py loaddata animaux_backup.json
```

### 6. Accéder à l'application

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Application principale |
| http://localhost:8000/admin | Interface d'administration |

---

## 🗄️ Base de données

### Schéma relationnel
```
UTILISATEUR
    id, email, password (hashé PBKDF2), first_name, last_name, telephone, adresse

ANIMAL
    id, nom, espece, race, age_annees, age_mois, categorie_age
    sexe, description, photo, disponible, date_arrivee

DEMANDE_ADOPTION
    id
    animal_id ──────────── FK → ANIMAL
    utilisateur_id ─────── FK → UTILISATEUR
    nom_complet, email, telephone, adresse
    type_logement, statut_logement
    motivation, disponibilite
    statut (EN_ATTENTE / ACCEPTEE / REFUSEE)
    notes_admin, date_demande
```

### Relations

- `ANIMAL` → `DEMANDE_ADOPTION` : **One to Many**
- `UTILISATEUR` → `DEMANDE_ADOPTION` : **One to Many**
- Contrainte d'unicité : un utilisateur ne peut faire qu'**une seule demande par animal**

### Commandes migrations
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

---

## 👤 Parcours utilisateur

### Visiteur non connecté

- ✅ Page d'accueil avec les 3 derniers animaux arrivés
- ✅ Page liste des animaux avec filtrage dynamique
- ✅ Page détail de chaque animal
- ✅ Page À propos du refuge
- ❌ Formulaire d'adoption → redirigé vers la connexion

### Utilisateur connecté

- ✅ Toutes les pages visiteur
- ✅ Formulaire d'adoption pré-rempli (nom, email)
- ✅ Soumission d'une demande d'adoption

### Administrateur

- ✅ Interface admin Django (`/admin`)
- ✅ Gestion des animaux (ajout, modification, suppression)
- ✅ Traitement des demandes (accepter / refuser / notes)
- ✅ Acceptation automatique → animal passe en indisponible

---


## 🔐 Sécurité

| Menace | Protection |
|--------|------------|
| Injection SQL | ORM Django  |
| XSS | Échappement automatique des variables dans les templates |
| CSRF | `{% csrf_token %}` sur tous les formulaires POST |
| Vol de session | Cookie `sessionid` en `HttpOnly` |
| Mots de passe | Hashage PBKDF2 + SHA256 - jamais stockés en clair |
| Accès non autorisé | `@login_required` sur les vues sensibles |

### Authentification par sessions

Pas de JWT — le projet utilise le système de sessions natif Django :

1. `authenticate()` compare le hash du mot de passe saisi avec celui en base
2. `login()` crée une session dans `django_session` et envoie un cookie `sessionid`
3. À chaque requête Django lit le cookie et identifie l'utilisateur via `request.user`
4. `logout()` supprime la session et le cookie

---

## 🐳 Architecture Docker

### Services

| Service | Image | Port | Rôle |
|---------|-------|------|------|
| `db` | mysql:8.0 | 3307:3306 | Base de données MySQL |
| `backend` | Python 3.12 | 8000:8000 | Application Django |

### Volumes

| Volume | Contenu |
|--------|---------|
| `mysql_data` | Données MySQL persistées |
| `static_volume` | Fichiers statiques collectés |
| `media_volume` | Photos des animaux uploadées |

### Commandes utiles
```bash
# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Repartir de zéro (supprime les volumes)
docker-compose down -v

# Accès MySQL
docker-compose exec db mysql -u unispattes_user -p unispattes_db
```

---

## 📦 Dépendances Python

| Package | Version | Rôle |
|---------|---------|------|
| Django | 6.0 | Framework web |
| mysqlclient | 2.2.7 | Connecteur MySQL |
| pillow | 12.0.0 | Gestion des images |
| django-admin-interface | 0.32.0 | Admin personnalisé |
| django-colorfield | 0.14.0 | Champs couleur admin |
| asgiref | 3.11.0 | Support ASGI |

---

## 🌐 Variables d'environnement

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `SECRET_KEY` | Clé secrète Django | ✅ |
| `DEBUG` | Mode debug (`1` = activé) | ✅ |
| `DB_NAME` | Nom de la base de données | ✅ |
| `DB_USER` | Utilisateur MySQL | ✅ |
| `DB_PASSWORD` | Mot de passe MySQL | ✅ |
| `DB_HOST` | Hôte MySQL (nom du service Docker) | ✅ |
| `DB_PORT` | Port MySQL | ✅ |

> En production : `DEBUG=0` et `SECRET_KEY` doit être une chaîne longue et aléatoire

---

## 🧪 Tests
```bash
# Tous les tests
docker-compose exec backend python manage.py test

# Par application
docker-compose exec backend python manage.py test animaux
docker-compose exec backend python manage.py test users
```

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre de la formation **Développeur Web et Web Mobile** — RNCP37674 Niveau 5.

Louis Manchon: <https://github.com/LouisManchon>

# Conversion automatique DOCX vers PDF

Script Python permettant de convertir automatiquement tous les fichiers Word (`.docx`) en PDF sous Linux Fedora, avec classement par date de modification du document source.

## Fonctionnalités

- Parcours de tous les fichiers DOCX du dossier `word/`, y compris les sous-dossiers.
- Conversion avec LibreOffice en mode headless.
- Classement des PDF par année, mois et jour.
- Vérification de l'existence des PDF.
- Ignorance des PDF déjà à jour.
- Reconversion des documents modifiés.
- Journalisation des conversions et des erreurs.

## Structure du projet

```text
RENDU/
├── pdf/
├── word/
├── conversion.py
├── README.md
└── .gitignore
```

Les PDF sont enregistrés dans une arborescence organisée par date :

```text
pdf/
└── 2026/
    └── 10/
        └── 24/
            └── document.pdf
```

La date utilisée est celle de la dernière modification du fichier DOCX.

## Prérequis

- Fedora Linux
- Python 3
- LibreOffice

### Installation

Installer Python et LibreOffice :

```bash
sudo dnf install python3 libreoffice
```

Vérifier les installations :

```bash
python3 --version
libreoffice --version
```

## Configuration

Le script utilise les dossiers suivants :

```python
DOSSIER_SOURCE = Path("word")
DOSSIER_DESTINATION = Path("pdf")
```

Les chemins sont relatifs au répertoire depuis lequel le script est exécuté.

- `word/` : documents Word à convertir.
- `pdf/` : destination des fichiers PDF générés.

## Utilisation

Depuis la racine du projet :

```bash
python3 conversion.py
```

Le script parcourt les fichiers DOCX, vérifie les PDF existants et effectue uniquement les conversions nécessaires.

## Règles de conversion

| Situation | Action |
|---|---|
| PDF absent | Création du PDF |
| PDF existant et à jour | Aucune conversion |
| DOCX modifié depuis la conversion | Reconversion |
| Erreur de conversion | Journalisation de l'erreur |

## Remarques

- Le script utilise la date de modification du DOCX, et non sa date réelle de création.
- Les fichiers DOCX temporaires commençant par `~$` sont ignorés.
- Les anciens PDF ne sont pas automatiquement supprimés lorsqu'un DOCX change de date.
- Il est recommandé de lancer le script depuis la racine du projet.

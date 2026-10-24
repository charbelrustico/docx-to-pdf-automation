
from pathlib import Path
from datetime import datetime
import subprocess
import logging

# ==================================================
# CONFIGURATION
# ==================================================

DOSSIER_SOURCE = Path("word")
DOSSIER_DESTINATION = Path("pdf")

DELAI_MAX = 120  # secondes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ==================================================
# CONVERSION D'UN FICHIER DOCX
# ==================================================

def convertir_docx(fichier_docx: Path) -> bool:
    """Convertit un DOCX si son PDF est absent ou obsolète."""

    # Ignorer les fichiers temporaires de Microsoft Word
    if fichier_docx.name.startswith("~$"):
        logging.info("Fichier temporaire ignoré : %s", fichier_docx.name)
        return True

    try:
        # Date de dernière modification du DOCX
        date_modification = fichier_docx.stat().st_mtime
        date_fichier = datetime.fromtimestamp(date_modification)

        # Classement : année / mois / jour
        dossier_date = (
            DOSSIER_DESTINATION
            / date_fichier.strftime("%Y")
            / date_fichier.strftime("%m")
            / date_fichier.strftime("%d")
        )

        dossier_date.mkdir(parents=True, exist_ok=True)

        # Nom du PDF identique à celui du DOCX
        fichier_pdf = dossier_date / f"{fichier_docx.stem}.pdf"

        # Vérifier si le PDF existe et est plus récent
        if fichier_pdf.is_file():
            date_pdf = fichier_pdf.stat().st_mtime

            if date_pdf >= date_modification:
                logging.info("DÉJÀ À JOUR : %s", fichier_pdf)
                return True

        # Conversion avec LibreOffice
        resultat = subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(dossier_date.resolve()),
                str(fichier_docx.resolve()),
            ],
            capture_output=True,
            text=True,
            timeout=DELAI_MAX,
            check=False,
        )

        # Vérifier le résultat de la conversion
        if resultat.returncode == 0 and fichier_pdf.is_file():
            logging.info("CONVERTI : %s", fichier_pdf)
            return True

        logging.error(
            "ÉCHEC : %s | %s",
            fichier_docx,
            resultat.stderr or resultat.stdout or
            "PDF non généré",
        )
        return False

    except subprocess.TimeoutExpired:
        logging.error("DÉLAI DÉPASSÉ : %s", fichier_docx)
        return False

    except OSError as erreur:
        logging.error("ERREUR : %s | %s", fichier_docx, erreur)
        return False


# ==================================================
# TRAITEMENT DE TOUS LES DOCX
# ==================================================

def convertir_tous_les_docx():
    if not DOSSIER_SOURCE.is_dir():
        logging.error(
            "Dossier source introuvable : %s",
            DOSSIER_SOURCE.resolve(),
        )
        return

    fichiers = sorted(DOSSIER_SOURCE.rglob("*.docx"))

    # Ignorer les fichiers temporaires dans le bilan
    fichiers = [
        f for f in fichiers
        if not f.name.startswith("~$")
    ]

    total = len(fichiers)
    succes = 0
    echecs = 0

    logging.info("%d fichier(s) DOCX détecté(s).", total)

    for fichier in fichiers:
        if convertir_docx(fichier):
            succes += 1
        else:
            echecs += 1

    logging.info("=" * 50)
    logging.info("BILAN FINAL")
    logging.info("Total       : %d", total)
    logging.info("Succès      : %d", succes)
    logging.info("Échecs      : %d", echecs)
    logging.info("=" * 50)


# ==================================================
# POINT D'ENTRÉE
# ==================================================

if __name__ == "__main__":
    convertir_tous_les_docx()

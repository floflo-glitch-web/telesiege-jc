"""Archive complete et paquet GitHub, sans executer les scripts du projet."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-22'
TEMP_PARTS = {'.git', '__pycache__', '.venv', 'venv', '.idea', '.vscode'}


def temporary(relative: str) -> bool:
    p = PurePosixPath(relative)
    return bool(TEMP_PARTS.intersection(p.parts)) or p.suffix in {'.pyc', '.pyo', '.tmp', '.log'} or p.name in {'.DS_Store', 'Thumbs.db', 'desktop.ini'}


def for_github(relative: str) -> bool:
    # Meme politique que le .gitignore fourni. Les sources locales restent intactes.
    if temporary(relative):
        return False
    if relative.startswith('references/'):
        return relative == 'references/README.md'
    if relative.startswith('recherche_mesures_2026-10-22/documents/'):
        return relative.endswith('/inventaire_pdf.json')
    if relative.startswith('reprise_codex/documents/'):
        return relative == 'reprise_codex/documents/README.md'
    if relative.startswith(('archives_locales/', 'reprise_codex/constructions/')):
        return False
    if relative == 'reprise_codex/sources_claude/Avancement_bureau_avant_reprise.txt':
        return False
    if relative in {'INVENTAIRE_COMPLET.json', 'INVENTAIRE_GITHUB.json'}:
        return False
    p = PurePosixPath(relative)
    return p.suffix != '.zip' and (not p.name.startswith('.env') or p.name == '.env.example')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory(paths: list[Path]) -> list[dict]:
    return [dict(fichier=p.relative_to(ROOT).as_posix(), octets=p.stat().st_size,
                 sha256=digest(p.read_bytes())) for p in paths]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suffixe', default='', help='Nom court pour une nouvelle sauvegarde sans ecraser les precedentes')
    args = parser.parse_args()
    if args.suffixe and not re.fullmatch(r'[A-Za-z0-9_-]+', args.suffixe):
        parser.error('Suffixe autorise : lettres, chiffres, tiret et soulignement')
    suffix = '-' + args.suffixe if args.suffixe else ''
    outputs = {kind: ROOT.parent / f'Gare-JC-{kind}-{DATE}{suffix}.zip'
               for kind in ('COMPLET', 'GITHUB')}
    report_path = ROOT.parent / f'Gare-JC-VERIFICATION-{DATE}{suffix}.json'
    for p in [*outputs.values(), report_path]:
        if p.exists():
            parser.error(f'Fichier deja present, choisir --suffixe : {p.name}')

    all_paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts)
    # Le fichier d'inventaire se decrit par ses entrees, pas par son propre hash.
    full_paths = [p for p in all_paths if p.relative_to(ROOT).as_posix() != 'INVENTAIRE_COMPLET.json']
    complete = dict(date=DATE, portee='Tous les fichiers du dossier, hors metadonnees .git',
                    inventaire_lui_meme_exclu=True, fichiers=inventory(full_paths))
    full_inventory = ROOT / 'INVENTAIRE_COMPLET.json'
    full_inventory.write_text(json.dumps(complete, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    full_paths.append(full_inventory)
    public_paths = [p for p in all_paths if for_github(p.relative_to(ROOT).as_posix())]
    if any(p.stat().st_size > 25 * 1024 * 1024 for p in public_paths):
        raise ValueError('Un fichier du paquet GitHub depasse 25 MiB')
    if len(public_paths) + 1 > 100:
        raise ValueError('Le paquet GitHub depasse 100 fichiers')
    public_inventory = dict(date=DATE, portee='Travail du projet et liens vers les references externes',
        inventaire_lui_meme_exclu=True, fichiers=inventory(public_paths),
        conserves_dans_archive_complete=[p.relative_to(ROOT).as_posix() for p in full_paths
                                      if not for_github(p.relative_to(ROOT).as_posix())])

    records = []
    for kind, paths in [('COMPLET', full_paths), ('GITHUB', public_paths)]:
        destination = outputs[kind]
        prefix = ROOT.name + '/' if kind == 'COMPLET' else ''
        with ZipFile(destination, 'x', compression=ZIP_DEFLATED, compresslevel=6) as z:
            for p in paths:
                z.write(p, prefix + p.relative_to(ROOT).as_posix())
            if kind == 'GITHUB':
                z.writestr('INVENTAIRE_GITHUB.json', json.dumps(public_inventory, ensure_ascii=False, indent=2) + '\n')
        with ZipFile(destination) as z:
            if z.testzip() is not None:
                raise ValueError('Erreur CRC : ' + destination.name)
            expected = {prefix + p.relative_to(ROOT).as_posix() for p in paths}
            if kind == 'GITHUB':
                expected.add('INVENTAIRE_GITHUB.json')
            if set(z.namelist()) != expected or len(z.namelist()) != len(expected):
                raise ValueError('Fichiers manquants ou dupliques : ' + destination.name)
            for p in paths:
                if digest(z.read(prefix + p.relative_to(ROOT).as_posix())) != digest(p.read_bytes()):
                    raise ValueError('Contenu different : ' + str(p))
            count = len(z.infolist())
            unpacked = sum(x.file_size for x in z.infolist())
        record = dict(archive=destination.name, octets=destination.stat().st_size,
                      fichiers=count, octets_decompresses=unpacked,
                      sha256=digest(destination.read_bytes()),
                      controle_crc='OK', comparaison_chaque_fichier_sha256='OK')
        records.append(record)
        print(f"{destination.name} : {record['octets']/1_000_000:.2f} Mo, {count} fichiers, verification OK", flush=True)
    report_path.write_text(json.dumps(dict(date=DATE, archives=records, aucun_envoi_sur_github=True),
                                        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Rapport : ' + report_path.name, flush=True)


if __name__ == '__main__':
    main()

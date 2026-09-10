from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
skill = root / ".claude" / "skills" / "solution-blueprint"
out = root / "dist"
out.mkdir(exist_ok=True)
zip_path = out / "solution-blueprint-skill.zip"
with ZipFile(zip_path, "w", ZIP_DEFLATED) as z:
    for p in skill.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(skill))
print(zip_path)

"""配布物の内容・基本依存・クリーン導入とsdist再ビルドを検査する。"""
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import venv
import zipfile
from email.parser import BytesParser
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    wheels = list((root / "dist").glob("*.whl"))
    sources = list((root / "dist").glob("*.tar.gz"))
    if len(wheels) != 1 or len(sources) != 1:
        raise RuntimeError("distには今回のwheelとsdistを一つずつ用意してください")
    wheel = wheels[0]
    source = sources[0]

    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        expected = {"minecraft_dev_lab/__init__.py", "minecraft_dev_lab/py.typed"}
        if not expected <= names:
            raise RuntimeError("wheelにパッケージまたは型情報のmarkerがありません")
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(metadata_name))
        if metadata["Name"] != project["name"] or metadata["Version"] != project["version"]:
            raise RuntimeError("配布物の名前またはバージョンが設定と一致しません")
        if set(metadata["Requires-Python"].split(",")) != set(project["requires-python"].split(",")):
            raise RuntimeError("Python対応範囲が設定と一致しません")
        requirements = metadata.get_all("Requires-Dist", [])
        if any("extra ==" not in requirement for requirement in requirements):
            raise RuntimeError("基本パッケージに想定外の実行依存があります")
        if not any("pyside6" in value.lower() and "gui" in value for value in requirements):
            raise RuntimeError("GUI依存がgui extraとして宣言されていません")
        allowed = ("minecraft_dev_lab/", f"minecraft_dev_lab-{project['version']}.dist-info/")
        if any(not name.startswith(allowed) for name in names):
            raise RuntimeError("wheelに想定外のデータが含まれています")

    with tempfile.TemporaryDirectory(prefix="minecraft-dev-lab-build-") as temporary:
        directory = Path(temporary)
        environment = directory / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", str(wheel)],
            cwd=directory,
            check=True,
        )
        subprocess.run(
            [
                str(python),
                "-c",
                "import importlib.metadata as m, importlib.util as u; "
                "import minecraft_dev_lab; "
                "import sys; "
                "assert m.version('minecraft-dev-lab') == sys.argv[1]; "
                "assert u.find_spec('PySide6') is None",
                project["version"],
            ],
            cwd=directory,
            check=True,
        )
        with tarfile.open(source) as archive:
            names = archive.getnames()
            prefix = names[0].split("/", 1)[0]
            required = {
                f"{prefix}/pyproject.toml",
                f"{prefix}/scripts/check_distribution.py",
                f"{prefix}/docs/design.md",
                f"{prefix}/src/minecraft_dev_lab/__init__.py",
            }
            if not required <= set(names):
                raise RuntimeError("sdistに再ビルドまたは設計の材料がありません")
            archive.extractall(directory / "source", filter="data")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "build",
                "--wheel",
                "--outdir",
                str(directory / "rebuilt"),
                str(directory / "source" / prefix),
            ],
            cwd=directory,
            check=True,
        )
        if not (directory / "rebuilt" / wheel.name).is_file():
            raise RuntimeError("sdistから同じ名前のwheelを再構築できません")
    print("配布物・Qtなしのクリーン導入・sdist再ビルドを確認しました")


if __name__ == "__main__":
    main()

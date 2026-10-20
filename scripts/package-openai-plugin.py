import argparse
import json
import zipfile
from pathlib import Path


def main(output_path: Path) -> None:
    script_dir = Path(__file__).resolve().parent
    openai_plugin_dir = script_dir.parent / "openai"
    assert openai_plugin_dir.exists()

    plugin = json.loads((openai_plugin_dir / "plugin.json").read_text())
    package_filename = f"{plugin['name']}-openai-{plugin['version']}.zip"
    dest = output_path / package_filename

    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in openai_plugin_dir.walk(on_error=print, follow_symlinks=True):
            for file in files:
                full_path = root / file
                arcname = full_path.relative_to(openai_plugin_dir)
                zf.write(root / file, arcname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="package openai plugin")
    parser.add_argument("output_dir", type=Path, help="Directory where package file is created", default=Path("."))

    args = parser.parse_args()
    main(args.output_dir)

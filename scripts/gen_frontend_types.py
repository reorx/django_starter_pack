import glob
import logging
import os
import sys
from contextlib import redirect_stdout
from importlib import import_module
from io import StringIO
from pathlib import Path

import django
from pydantic2ts import generate_typescript_defs, logger


logger.setLevel(logging.WARN)

json2ts_cmd = "./frontend/node_modules/.bin/json2ts"


def main():
    print('configure python path')
    package_path = sys.argv[1]
    package_name = package_path.split("/")[-1]
    sys.path.insert(0, Path(package_path).parent)

    print('setup django')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{package_name}.settings')
    django.setup()

    print("\ngenerating types modules interfaces")
    for path in glob.glob(f"{package_path}/types/*.py"):
        stem = Path(path).stem
        if stem in ["base"]:
            continue
        import_path = f"{package_name}.types.{stem}"
        output_path = f"frontend/types/{stem}.ts"
        print(f"- {import_path} -> {output_path}")
        generate_typescript_defs(
            import_path,
            output_path,
            json2ts_cmd=json2ts_cmd,
        )

    print("\ngenerating routes modules interfaces")
    for path in glob.glob(f"{package_path}/**/routes/*.py"):
        rel_path = Path(path).relative_to(package_path)
        import_path = f"{package_name}.{rel_path.replace('/', '.')[:-3]}"
        output_path = f"frontend/services/{import_path.split(".")[-1]}/params.ts"
        print(f"- {import_path} -> {output_path}")

        # only include pydantic models that ends with 'Params' or 'Response'
        def include_func(model):
            name: str = model.__name__
            if name.endswith("Params") or name.endswith("Response") or name.endswith("Item"):
                return True
            return False

        generate_typescript_defs(
            import_path,
            output_path,
            include_func=include_func,
            json2ts_cmd=json2ts_cmd,
        )

    print("\ngenerating consts")
    for path in glob.glob(f"{package_path}/consts/*.py"):
        stem = Path(path).stem
        import_path = f"{package_name}.consts.{stem}"
        name = stem
        # remove leading underscore from name
        if name.startswith("_"):
            name = name[1:]
        output_path = f"frontend/consts/{name}.ts"
        print(f"- {import_path} -> {output_path}")

        m = import_module(import_path)
        buf = StringIO()
        with redirect_stdout(buf):
            m.to_ts()

        with open(output_path, "w") as f:
            f.write(buf.getvalue())


if __name__ == "__main__":
    main()

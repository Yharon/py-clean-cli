from sys import path as sys_path
from pathlib import Path
from typing import Optional
from inspect import getmodule, currentframe, getfile
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec


PROJECT_ROOT = str(Path.cwd())
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)


def discover_commands(package_path: Optional[str] = None) -> None:
    """
    Descobre e carrega comandos dinamicamente de um pacote

    Se package_path for None, tenta descobrir no mesmo pacote que o módulo atual.
    """
    if package_path is None:
        current_module = getmodule(currentframe())
        if current_module is not None:
            package_path = str(Path(getfile(current_module)).parent)
        else:
            return

    if not Path(package_path).is_dir():
        return

    # Importar todos os módulos Python no diretório
    for file in Path(package_path).rglob("*.py"):
        if file.name.startswith("_"):
            continue

        try:
            rel_path = file.relative_to(Path(PROJECT_ROOT))
            parts = rel_path.with_suffix("").parts
            module_path = ".".join(parts)
            import_module(module_path)
        except (ImportError, ValueError) as e:
            print(f"Erro ao importar módulo {file.name}: {e}")
            # Tenta importação alternativa usando o nome do arquivo
            try:
                module_name = file.stem
                spec = spec_from_file_location(module_name, file)
                if spec and spec.loader:
                    module = module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"Módulo {module_name} importado com sucesso usando spec")
            except Exception as e2:
                print(f"Falha ao importar {file.name} usando spec: {e2}")

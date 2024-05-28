$root_cache_paths = @(
    ".\.pytest_cache"
    ".\.ruff_cache"
    ".\.mypy_cache"
    ".\.tox"
    ".\build"
    ".\dist"
    ".\htmlcov"
    ".\*.egg-info"
)
foreach ($path in $root_cache_paths) {
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
    }
}

$recurse_cache_paths = @(
    "__pycache__"
    ".pytest_cache"
    ".ipynb_checkpoints"
    "build"
    "target"
    "*.pyd"
    "*.dll"
    "*.mod"
    "*.lock"
    # "*.lib"
    # "*.a"
    # "*.obj"
    "tempCodeRunnerFile.*"
)
foreach ($path in $recurse_cache_paths) {
    Remove-Item * -Include $path -Recurse -Force
}

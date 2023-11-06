$root_cache_paths = @(
    ".\build"
    ".\dist"
    ".\*.egg-info"
    ".\htmlcov"
    ".\.pytest_cache"
    ".\.ruff_cache"
)
foreach ($path in $root_cache_paths) {
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
    }
}

$recurse_cache_paths = @(
    "__pycache__"
    "build"
    # "*.dll"
    # "*.lib"
    "*.pyd"
    # "*.a"
    # "*.obj"
    "tempCodeRunnerFile.*"
)
foreach ($path in $recurse_cache_paths) {
    Remove-Item * -Include $path -Recurse -Force
}

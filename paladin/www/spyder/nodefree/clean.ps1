$root_cache_paths = @(
    ".\*.txt"
    ".\*.yaml"
    ".\*.yml"
)
foreach ($path in $root_cache_paths) {
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
    }
}

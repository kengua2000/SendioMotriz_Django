# Directorio base
$baseDir = "templates"

# Estructura de carpetas y archivos
$estructura = @{
    "clientes"   = @("lista.html", "form.html", "eliminar.html")
    "empleados"  = @("lista.html", "form.html")
    "productos"  = @("lista.html", "form.html")
    "vehiculos"  = @("lista.html", "form.html")
    "facturas"   = @("form.html", "agregar_detalle.html", "ver.html")
}

# Crear carpetas y archivos
foreach ($folder in $estructura.Keys) {
    $folderPath = Join-Path -Path $baseDir -ChildPath $folder
    New-Item -ItemType Directory -Path $folderPath -Force | Out-Null

    foreach ($file in $estructura[$folder]) {
        $filePath = Join-Path -Path $folderPath -ChildPath $file
        New-Item -ItemType File -Path $filePath -Force | Out-Null
    }
}

# Archivo en el directorio base
New-Item -ItemType File -Path (Join-Path -Path $baseDir -ChildPath "dashboard.html") -Force | Out-Null

Write-Host "Estructura creada en el directorio: $baseDir" -ForegroundColor Green

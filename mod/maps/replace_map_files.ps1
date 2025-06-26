# Define the source and destination directories
$source = Get-Location
$destination = "G:\mods\titanfall 2\made\Berdox.WallKickTrainingMapNS\Berdox.WallKickTrainingMap\mod\maps"

# Create the destination directory if it doesn't exist
if (!(Test-Path -Path $destination)) {
    New-Item -ItemType Directory -Path $destination
}

# Copy all files (excluding subdirectories)
Get-ChildItem -Path $source -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $destination
}

Write-Host "All files copied successfully!"
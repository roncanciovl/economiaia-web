Get-ChildItem "d:\workspace\marketing_ws\resources\*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $changed = $false
    
    if ($content -match '·') {
        # Replace unicode middot with HTML entity in Sigma-related text
        $content = $content.Replace('Razonamiento activo · Llama 3.3', 'Razonamiento activo &middot; Llama 3.3')
        $content = $content.Replace('Sigma · razonado en contexto', 'Sigma &middot; razonado en contexto')
        $changed = $true
    }
    
    if ($changed) {
        # Write without BOM to avoid encoding issues
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($_.FullName, $content, $utf8NoBom)
        Write-Host "FIXED: $($_.Name)"
    } else {
        Write-Host "SKIP: $($_.Name)"
    }
}

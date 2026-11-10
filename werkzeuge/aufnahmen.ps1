param([string]$Arbeit = $PSScriptRoot, [string]$Ziel = "C:\Users\mario\source\repos\imagiter-webseite\bilder")
# Bildschirmfotos für die Webseite: Vorschau (Port 8071) und Studio (Port 8072) müssen laufen,
# dazu ein einfacher Dateiserver für den Arbeitsordner auf Port 8073. Eigener Edge (Port 9351), nicht der gemeinsame Testbrowser.
. "$Arbeit\cdp-eigen.ps1"
function Groesse($w, $h, $mobil = $false, $faktor = 1) { Cdp "Emulation.setDeviceMetricsOverride" @{ width = $w; height = $h; deviceScaleFactor = $faktor; mobile = $mobil } | Out-Null }
function Knopf($text) { Ev "[...document.querySelectorAll('#page button')].find(b=>b.textContent.includes('$text')).click(); 'ok'" | Out-Null }

Groesse 1440 900
Open "http://127.0.0.1:8071/"; Start-Sleep 2; Knopf "blättern"; Start-Sleep 3; Shot "w-jahresseite"
Open "http://127.0.0.1:8071/"; Ev "window.speechSynthesis.speak=function(u){ setTimeout(function(){u.onend&&u.onend();},2600); }; HTMLMediaElement.prototype.play=function(){return Promise.resolve();}; 'ok'" | Out-Null; Knopf "Zeitreise starten"; Start-Sleep 11; Shot "w-trailer"
Open "http://127.0.0.1:8071/"; Knopf "Quiz"; Start-Sleep 2; Ev "[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='Rosenheim').click(); 'ok'" | Out-Null; Start-Sleep 1; Shot "w-quiz"
Groesse 1600 900
Open "http://127.0.0.1:8072/#/z/anna-paul"; Start-Sleep 2; Ev "document.querySelector('[data-reiter=jahre]').click(); 'ok'" | Out-Null; Start-Sleep 2; Ev "[...document.querySelectorAll('button')].find(b=>b.textContent.includes('Seitenvorschau')).click(); 'ok'" | Out-Null; Start-Sleep 4; Shot "w-studio"
Groesse 390 844 $true 2
Open "http://127.0.0.1:8071/"; Knopf "blättern"; Start-Sleep 2; Ev "document.getElementById('next').click(); 'ok'" | Out-Null; Start-Sleep 3; Shot "w-handy"

# In WebP umwandeln (über den Dateiserver, damit das Bild im Canvas gelesen werden darf)
Groesse 1440 900
Open "http://127.0.0.1:8073/"
foreach ($e in @(@("w-jahresseite","jahresseite",1440), @("w-trailer","trailer",1440), @("w-quiz","quiz",1440), @("w-studio","studio",1600), @("w-handy","handy",780))) {
  $js = "new Promise(function(ok){ var i=new Image(); i.onload=function(){ var w=Math.min($($e[2]), i.naturalWidth), h=Math.round(i.naturalHeight*w/i.naturalWidth); var c=document.createElement('canvas'); c.width=w; c.height=h; var g=c.getContext('2d'); g.imageSmoothingQuality='high'; g.drawImage(i,0,0,w,h); ok(c.toDataURL('image/webp',0.84).split(',')[1]); }; i.src='shots/$($e[0]).png?'+Date.now(); })"
  [IO.File]::WriteAllBytes("$Ziel\$($e[1]).webp", [Convert]::FromBase64String((Ev $js)))
}
Done
Get-ChildItem $Ziel -Filter *.webp | Select-Object Name, @{n='KB';e={[math]::Round($_.Length/1KB)}}

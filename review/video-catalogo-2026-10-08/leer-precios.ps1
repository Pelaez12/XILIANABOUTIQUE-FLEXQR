Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$taskMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 } | Select-Object -First 1
function Wait-Operation($operation, $resultType) {
 $task = $taskMethod.MakeGenericMethod($resultType).Invoke($null,@($operation))
 $task.Wait()
 $task.Result
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$rows = @()
foreach ($photo in (Get-ChildItem -LiteralPath "$PSScriptRoot/frames" -Filter '*.jpg')) {
 $file = Wait-Operation ([Windows.Storage.StorageFile]::GetFileFromPathAsync($photo.FullName)) ([Windows.Storage.StorageFile])
 $stream = Wait-Operation ($file.OpenReadAsync()) ([Windows.Storage.Streams.IRandomAccessStreamWithContentType])
 $decoder = Wait-Operation ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
 $bitmap = Wait-Operation ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
 $ocr = Wait-Operation ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
 $rows += @{ frame=$photo.BaseName; second=[int]$photo.BaseName.Substring(1)-1; lines=@($ocr.Lines | ForEach-Object { @{text=$_.Text;y=$_.Words[0].BoundingRect.Y} }) }
 $bitmap.Dispose();$stream.Dispose()
}
$rows | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath "$PSScriptRoot/ocr.json" -Encoding UTF8
Write-Output "OCR: $($rows.Count) fotogramas"

Import-Module Selenium -Scope Local
$downloadUrl = "https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_win32.zip"
$zip = "C:\Users\$env:UserName\Desktop\chromedriver_win32.zip"
$chromeDriver = "C:\Users\$env:UserName\Desktop\"
Invoke-WebRequest $downloadUrl -OutFile $zip
Expand-Archive -Path "C:\Users\$env:UserName\Desktop\chromedriver_win32.zip" -DestinationPath "C:\Users\$env:UserName\Desktop\" -Force
$chromeOptions = New-Object OpenQA.Selenium.chrome.chromeOptions
$chromeDriver = New-Object OpenQA.Selenium.chrome.chromeDriver($chromeDriver,$chromeOptions)
$chromeDriver.Navigate().GoToUrl("https://www.microsoft.com")

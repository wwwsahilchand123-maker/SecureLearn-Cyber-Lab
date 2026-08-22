' ==========================================================
' SecureLearn Cyber Lab - Create Desktop Shortcut
' ==========================================================

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

CurrentDir = FSO.GetParentFolderName(WScript.ScriptFullName)
DesktopPath = WshShell.SpecialFolders("Desktop")
ShortcutPath = DesktopPath & "\SecureLearn Phishing Simulator.lnk"
TargetVbs = CurrentDir & "\Start_App.vbs"

Set oLink = WshShell.CreateShortcut(ShortcutPath)
oLink.TargetPath = "wscript.exe"
oLink.Arguments = """" & TargetVbs & """"
oLink.WorkingDirectory = CurrentDir
oLink.Description = "Launch SecureLearn AI Phishing Detection Simulator"
oLink.WindowStyle = 7 ' Minimized / Hidden
oLink.IconLocation = "shell32.dll,220" ' Shield icon
oLink.Save

WshShell.Popup "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & "You can now launch the app directly from your Desktop by double-clicking 'SecureLearn Phishing Simulator'.", 5, "Shortcut Created", 64

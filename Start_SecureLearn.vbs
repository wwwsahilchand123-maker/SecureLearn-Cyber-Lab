Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' This VBS file is inside the inner project folder
projectPath = FSO.GetParentFolderName(WScript.ScriptFullName)

' venv is one folder above the inner project folder
pythonw = FSO.GetParentFolderName(projectPath) & "\venv\Scripts\python.exe"

' Server file is in the same folder as this VBS
server = projectPath & "\run_server.py"

' Check Python
If Not FSO.FileExists(pythonw) Then
    MsgBox "Python not found:" & vbCrLf & pythonw, 16, "SecureLearn Error"
    WScript.Quit
End If

' Check server
If Not FSO.FileExists(server) Then
    MsgBox "run_server.py not found:" & vbCrLf & server, 16, "SecureLearn Error"
    WScript.Quit
End If

' Start Flask server silently
WshShell.Run """" & pythonw & """ """ & server & """", 0, False

' Wait for Flask to start
WScript.Sleep 7000

' Open website
WshShell.Run "http://127.0.0.1:5000/", 1, False
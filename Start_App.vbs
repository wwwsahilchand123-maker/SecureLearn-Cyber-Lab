' ==========================================================
' SecureLearn Cyber Lab - Silent 1-Click Launcher (No Terminal)
' ==========================================================

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get current script directory
CurrentDir = FSO.GetParentFolderName(WScript.ScriptFullName)

' Find PythonW path in venv
PythonW = ""
If FSO.FileExists(CurrentDir & "\..\venv\Scripts\pythonw.exe") Then
    PythonW = FSO.GetAbsolutePathName(CurrentDir & "\..\venv\Scripts\pythonw.exe")
ElseIf FSO.FileExists(CurrentDir & "\venv\Scripts\pythonw.exe") Then
    PythonW = FSO.GetAbsolutePathName(CurrentDir & "\venv\Scripts\pythonw.exe")
Else
    PythonW = "pythonw.exe"
End If

ServerScript = CurrentDir & "\run_server.py"

' Function to check if server is running
Function IsServerRunning()
    On Error Resume Next
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    http.setTimeouts 1000, 1000, 1000, 1000
    http.Open "GET", "http://127.0.0.1:5000/health", False
    http.Send
    If Err.Number = 0 And http.Status = 200 Then
        IsServerRunning = True
    Else
        IsServerRunning = False
    End If
    Set http = Nothing
    On Error GoTo 0
End Function

' Start server silently if not already running
If Not IsServerRunning() Then
    ' Run completely hidden (0 = hide window)
    WshShell.CurrentDirectory = CurrentDir
    WshShell.Run """" & PythonW & """ """ & ServerScript & """", 0, False

    ' Wait for server to start up (up to 10 seconds)
    For i = 1 To 20
        WScript.Sleep 500
        If IsServerRunning() Then Exit For
    Next
End If

' Open in default browser or Edge App mode
WshShell.Run "http://127.0.0.1:5000/"

' ==========================================================
' SecureLearn Cyber Lab - Silent 1-Click Server Stopper
' ==========================================================

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
CurrentDir = FSO.GetParentFolderName(WScript.ScriptFullName)

' 1. Send shutdown request to Flask endpoint
On Error Resume Next
Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
http.setTimeouts 1000, 1000, 1000, 1000
http.Open "POST", "http://127.0.0.1:5000/api/shutdown", False
http.Send
Set http = Nothing
On Error GoTo 0

' 2. Check PID file if it exists
PidFile = CurrentDir & "\.server.pid"
If FSO.FileExists(PidFile) Then
    On Error Resume Next
    Set f = FSO.OpenTextFile(PidFile, 1)
    pid = Trim(f.ReadAll)
    f.Close
    If IsNumeric(pid) Then
        WshShell.Run "taskkill /F /T /PID " & pid, 0, True
    End If
    FSO.DeleteFile PidFile, True
    On Error GoTo 0
End If

WScript.Sleep 500

WshShell.Popup "SecureLearn Phishing Simulator server has been stopped.", 3, "Server Stopped", 64

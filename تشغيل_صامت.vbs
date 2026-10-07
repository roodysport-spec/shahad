Set WshShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath

' Stop old servers
WshShell.Run "taskkill /f /im python.exe /t", 0, True
WshShell.Run "taskkill /f /im node.exe /t", 0, True
WScript.Sleep 1000

' Start Backend
WshShell.Run "py -3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000", 0, False

' Start Frontend
WshShell.Run "cmd /c cd /d """ & strPath & "\frontend"" && npm run dev -- --host 127.0.0.1 --port 5173", 0, False

' Wait 4 seconds then open browser
WScript.Sleep 4000
WshShell.Run "http://localhost:5173"
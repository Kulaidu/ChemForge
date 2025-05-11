[Setup]
AppName=ChemForge
AppVersion=1.0
AppPublisher=Parkoya ni Edmar
DefaultDirName={userappdata}\ChemForge
DefaultGroupName=ChemForge
OutputBaseFilename=ChemForgeInstaller 1.0
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "ChemForge-win32-x64\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ChemForge"; Filename: "{app}\ChemForge.exe"
Name: "{group}\Uninstall ChemForge"; Filename: "{uninstallexe}"
Name: "{commondesktop}\ChemForge"; Filename: "{app}\ChemForge.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\ChemForge.exe"; Description: "Launch ChemForge"; Flags: nowait postinstall skipifsilent

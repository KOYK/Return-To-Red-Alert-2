[Setup]
AppName=YR to RA2 Mod
AppVersion=1.0
DefaultDirName={autopf}\Westwood\Red Alert 2
DefaultGroupName=YR to RA2 Mod
OutputDir=dist
OutputBaseFilename=RA2_Mod_Installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
; 1. The generated MIX file
Source: "expandmd24.mix"; DestDir: "{app}"; Flags: ignoreversion

; 2. Everything else in Source/, EXCEPT the expandmd24 folder
Source: "Source\*"; DestDir: "{app}\"; Flags: ignoreversion recursesubdirs createallsubdirs
; Explicitly exclude the raw folder (files are already in the .mix)
Source: "Source\expandmd24\*"; DestDir: "{app}\"; Flags: dontcopy

[Icons]
Name: "{group}\Run Mod"; Filename: "{app}\RunAres.bat"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
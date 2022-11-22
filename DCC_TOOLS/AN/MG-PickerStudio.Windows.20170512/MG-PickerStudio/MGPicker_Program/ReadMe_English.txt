All folders & files within MGPicker_Program folder are factory files. 
Please do not change them, if you want to add your own files, such as AutoSourced files and converters, please put them in the MGPicker_UserConfig folder.

AutoLoaders:	The loader python modules.
		Refer to help manual section "Loader and Lister" for more information.
		With custom loader and rigLister, you can distribute your designed picker files in any way!

AutoSourced:	The factory scripts be auto-sourced when MG-PickerStudio loads.

CodeSnippets:	The factory scripts serve as code snippets, whose content will be inserted into code editor.

CommandButtonPresets:	The factory command-button presets. 
		the content of them will be the command of the command-button,
		and the file name of them will be the label of the command-button, except the "_" are all replaced by " ".
		eg. the command-button label for the preset "Reset_Selection.mel" will be "Reset Selection".			
			
Converters:	The factory converter scripts.
		The converter enables the MG-PickerStudio to autoload other type of in-scene picker nodes, 
		or read an external other type of picker file.

HotkeySets:	For showing hotkeys in hotkey dialog.

Icons: 	The icons MG-PickerStudio use. 

Installer: MG-PickerStudio installer. Use the installer mel inside to install program to other versions of maya.

LanguageRes: 	MG-PickerStudio's language resource. 

Plug-ins: 	MG-PickerStudio's plugin files. 

Python: 	Python API Modules.

ServerConfig:	The manual config files, setting some hard-coded variable to change the program behavior.
		eg. The licence connector directory path.
		This is usually done by software administrator so that user do need to setup themselves.

SnapshotStyles: Factory default snapshot styles, it is for image auto-processing. 
		All styles filename here has a "~" prefix to indicate it is a factory style.
		A style file without a prefix "~" will be ignored. 

Templates: Factory picker templates, you can create picker based on these templates, 
		also these picker templates could used as example pickers to learn how to create pickers in MG-PickerStudio.

Terms: 	MG-PickerStudio's agreement & terms. Do not alter any content inside please.

UI: Contains the script for tool ui. Do not alter any content inside please.

VersionHisotry: The version history of MG-Picker Studio, the release notes.

MGPicker.ver: 	MG-PickerStudio version vlaue. Do not change it's content please.

MGPicker_WrittenByMiguel.mel: 	The loader and the serve scripts for the program. Do not change it please.
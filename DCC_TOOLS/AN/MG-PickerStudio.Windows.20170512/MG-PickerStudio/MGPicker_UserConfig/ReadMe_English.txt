AutoSourced:	Put your own mel/python scripts if you want them to be auto-sourced when MG-PickerStudio loads.
		These scripts are usually the scripts that support your picker functions.
		Mel scripts will be sourced using source command, and python scripts will be imported using execfile();

CodeSnippets:	Stores your own code snippets as mel/script file, for mel scritp please put it in MEL subfolder,
		for python scripts please put them in Python subfolder.
		These scripts serve as code snippets and their content will be inserted into the code editor.

CommandButtonPresets:	The user command-button presets. 
		Put your own mel/python script inside,organize with folders named with their categories.
		the content of them will be the command of the command-button,
		and the file name of them will be the label of the command-button, except the "_" are all replaced by " ".
		eg. the command-button label for the preset "My_Command_Preset.mel" will be "My Command Preset".			
			
Converters:	The user converter scripts, for now its mel only.
		The converter enables the MG-PickerStudio to autoload other type of in-scene picker nodes, 
		or read an external other type of picker file.

LanguageRes: 	MG-PickerStudio's user language resource. 
		If you have a full tranlation files for this program in your own language other than English & Chinese, 
		please email to mgpickerstudio@gmail.com and for future release the language resource will be published with program.

SnapshotStyles: The image processing style preset for doing the picker panel background image snapshoting.
		Also be used when you created iconed pose command-button.

UIConfig: 	Store the UI size & position of MG-PickerStudio in its Animator/Designer/Minimized mode.

GeneralConfig.ini: 		Stores the generic configurations.

PickerCreatingConfig.ini: 	Stores the picker item creation configurations.
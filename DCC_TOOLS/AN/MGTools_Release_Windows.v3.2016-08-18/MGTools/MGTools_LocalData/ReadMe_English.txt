MGTools_LocalData:	The root directory that stores all the MGTools user configs in files.
			The configs stored with Maya's optionVar mechanism is not stored here. 
			(But in the userPrefs.mel in Maya's user pref directory)

MGTools_LicenseData:	When you distribute MGTools among many machines under you production context,
			This folder stores all the user computer info and MGTools user codes files.
			These info files then could be used to batch register MGTools in multiple machines.
			Generally, This folder won't be installed in your machine, 
			it only exists in the MGTools Pro installation source.
			Check out the help manual to know more.

MGTools_GlobalData:	There is also a config root folder made by MGTools, 
			called "MGTools_GlobalData" in maya's user root directory,
			(normally the "My Document/maya/MGTools_GlobalData" directory in Windows) 
			which stores MG-PoseAnim Library and MG-Asset Library local library files.
			The folder sits beyond each specific maya version user directory, 
			so that the library files could be used among all the maya version in your local machine,
			while config files store in MGTools_LocalData directory could only be used by a specific Maya version.
			
./MG_AnimationBank:	Store all files exported by MG-AnimationBank tools.
			Basically you only use these files to export/import animation between scenes,
			use MG-PoseAnimation Library tools if you want to build up animation library.

./MG_AutoLoadConfig:	Store MGTools autoloading config files. 
			MGTools reads the config to load specific tools durning a Maya startup.

./MG_CamSwitchConfig:	Store MG-CameraSwitch config files.
			It records the camera switch list used by the tool.

./MG_DisplaySet:	Store MG-DisplaySet config files.
			Each set file records a display layer information, 
			which could be used to speed up the display layer creation process.

./MG_HUDConfig:		Store MG-HUD config files.
			Share the files among your pipeline to standardize the playblast burn-in.
	
./MG_OpenDirectoryConfig:	Store the directory shortcut configs.
				You can use these configs to browse a folder really quickly in Maya.
				
./MG_OpenExternalFileConfig:	Store the file shortcut configs.
				You can use these configs to open a file / load an external program in Maya, 
				such as Photoshop, Nuke, etc.

./MG_SelectionSet:	MG-SelectionSet files.

./MG_Shelves:		MG-Shelf config files.

./MG_SnapshotCameraBookmarks:	MGTools camera bookmark files, which store the attributes of a camera / multiple cameras.
	`			Used by MG-PoseAnimLibrary and MG-AssetLibrary tools to help making icons.
				
./MG_UIConfig:		Stores the normal & minimized sizes & positions of the bars of MGTools, 
			ConstraintTools, MG-Shelf, PivotTools,in files with a ".tmp" extension.
			It also stores the hidden states of each tools in MGTools bar in a file called "MG_ToolsChoice.cfg".

./MG_UpdatePackages:	Store update and rollback packages. This folder also stores all the update description text file.

			The subfolder UpdatePackages/ stores all the off-line update packages (*.mgu) 
			downloaded by the online updating feature.
			(You could also download the .mgu files manually through internet and put them here of course)
			You may need to copy these files to the offline machine, 
			use the "Offline Update" feature to apply these updates.
			
			The subfolder RollbackPackages/ stores the rollback datas, 
			it is a backup generated before each file is actually updated. 
                        You could use these rollback feature to rollback the MGTools version to older ones.

./MG_UserIcon:		This is a place that user could store some arbitrary icons that wish to copy/moved with MGTools.
			The main useage is storing the user icons that be used by MG-Shelf tool.

./MG_ViewSwitchConfig:	Stores the view switch config files used by the viewswitch tool.
			
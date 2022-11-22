MGTools_LocalData:	用来存储所有MGTools用户配置文件的根目录。
			以Maya的optionVar机制存储的用户配置不会存在这里面, 
			而是存在Maya的用户配置目录里的userPrefs.mel这个文件。

MGTools_LicenseData:	当你在线上的多台机子上分发MGTools时，
			这个文件夹用来接收用户机子提交的用户码，机子IP等信息。
			这些信息接下来可以用在批量注册MGTools上。
			基本上这个文件夹不会被安装到您的本地机子上，只存在于MGTools安装源里。
			请查看“分发MGTools”的帮助页面来了解更多。

MGTools_GlobalData:	MGTools在Maya配置目录的根目录里，创建了一个叫"MGTools_GlobalData"的目录,
			一般路径是 我的文档/maya/MGTools_GlobalData。 
			这个目录用来存储MG-Pose动画库及MG-资产库的本地端库文件。
			这个目录独立于所有的maya特定版本，可以为所有本机的所有装了MGTools的不同版本maya同时使用。
			相对应的，MGTools_LocalData里存储的配置，则只为本机的单个Maya版本所用。
			
./MG_AnimationBank:	存储MG-动画银行的文件。用来导出、导入动画。
			如果你要建立动画库，请用MG-Pose动画库工具。动画银行比较适合于只是导出导入动画时用。

./MG_AutoLoadConfig:	存储MGTools自动加载配置。
			在Maya启动时，MGTools自动读取这些配置，来自动加载相应的MGTools工具。

./MG_CamSwitchConfig:	存储MG-摄像机切换配置文件。
			这些配置文件是一些摄像机的切换清单。

./MG_DisplaySet:	存储MG-显示层集。
			这些集存储了显示层的一些创建信息，用来提升显示层的创建效率。
			用MG-显示层集工具来使用这些集。

./MG_HUDConfig:		存储MG-屏幕信息显示工具的配置文件。
			您可以在您的制作线上分享这些配置文件，以统一大家playblast出来的视频里显示的信息。

	
./MG_OpenDirectoryConfig:	存储文件夹快捷方式。
				使用这些信息，你可以在Maya里快速打开浏览某个文件夹。
				
./MG_OpenExternalFileConfig:	存储外部文件快捷方式。
				使用这些信息，你可以在Maya里快速打开某个文件,或启动某个外部程序，如Photoshop,Nuke等。

./MG_SelectionSet:	存储MG-选择集。

./MG_Shelves:		存储MG-工具架。

./MG_SnapshotCameraBookmarks:	MGTools使用的摄像机书签文件，这些文件每个都存储了一个或多个摄像机的信息。
				主要用来在MG-Pose动作库及MG-资产库中使用，来辅助这些工具生成图标，预览图及预览视频。
				
./MG_UIConfig:		存储了MGTools，约束工具，MG-工具架，轴心工具条这些界面的正常大小位置及最小化大小位置 
			（以 ".tmp"为扩展名的文件)
			它也存储了用户的MGTools工具隐藏设置，即在MGTools工具条上，哪些工具不要显示的设置。

./MG_UpdatePackages:	存储MGTools的更新相关的数据包，及每个更新的描述文本。 

			UpdatePackages子目录存储了离线更新包(*.mgu), 由MGTools的在线更新工具自动下载。
			(当然也可以手动在网上下载)
			你可以把这些离线更新包复制到不能上网的机子上的MGTools同样位置，然后使用"离线更新"工具应用这些更新。
			
			RollbackPackages子目录里存储了撤消更新用的回卷数据(*.mgr)。
			你可以在MGTools里使用这些回卷数据包，来使MGTools撤消最近的一些更新，重新恢复到旧版本。

./MG_UserIcon:		这个目录用来供用户存储想在MGTools里用的图标。主要用来存储MG-工具架所用的外部图标。

./MG_ViewSwitchConfig:	存储视图切换工具的配置文件。
			
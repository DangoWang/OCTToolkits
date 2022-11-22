AutoSourced:	在里面放置你想要在MG-Picker工作室启动时就自动加载的mel或python脚本。
		这些脚本基本上是用来支持你的picker里的代码功能的。
		MEL脚本将会用source命令来自动加载，python脚本将会用execfile()方式导入。

CodeSnippets:	在里面放置代码片段的脚本，mel请放到里面的MEL目录，python脚本请放到里面的Python目录。
		这些脚本的内容，将来被使用时将会被插入到当前代码编辑器的鼠标位置。

CommandButtonPresets:	用户的命令按钮预设。有了这些预设，用户就可以快速创建命令按钮且无需再敲代码。
		请在里面放入这些预设的mel或python脚本，并用他们的功能分类作为文件夹组织起来。
		这些脚本的内容将会是被创建的命令按钮的command，
		脚本的文件名将会是被创建的命令按钮的标签，并且文件名中所有的"_"字符将被替换成空格。
		比如使用了"My_Command_Preset.mel"这个预设文件创建的命令按钮，其标签是"My Command Preset"。			
			
Converters:	用户的picker转换器脚本，目前只支持MEL.
		这些转换器用来读取其它picker程序的picker节点或文件。

LanguageRes: 	MG-Picker工作室的语言文件。
		如果你有除英文及中文外的语言翻译文件，请邮件到mgpickerstudio@gmail.com，以便将来这个语言资源被正式发布到程序目录里。

SnapshotStyles: 图片处理预设，在生成picker面板的背景图时将自动被采用，在生成带图标的pose命令按钮时也用到。

UIConfig: 	存储界面在动画师/设计师/最小化模式时的大小及位置。

GeneralConfig.ini: 		存储用户的配置。

PickerCreatingConfig.ini: 	存储用户创建picker对象的配置。
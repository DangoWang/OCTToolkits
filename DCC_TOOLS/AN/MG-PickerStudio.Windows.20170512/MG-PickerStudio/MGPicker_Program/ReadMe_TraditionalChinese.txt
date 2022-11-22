MGPicker_Program目錄內的所有文件&文件夾都是程序自帶的，請不要改變他們，
如果您要添加用戶文件，比如自動載入的文件或轉換器等，請放置到MGPicker_UserConfig的相關目錄內。

AutoLoaders:	放置用戶自定義的loaders及rigLister.
		參考幫助文檔裡的"Loader 和 Lister" 來瞭解更多資訊.
		使用自定義的loader及rigLister類,你可以用任意方式來分發你設計的picker文件！

AutoSourced:	內置的隨MG-Picker工作室啟動而自動中載的一些腳本。

CodeSnippets:	內置的代碼片段的腳本。這些腳本的內容，將來被使用時將會被插入到當前代碼編輯器的滑鼠位置。

CommandButtonPresets:	內置的命令按鈕預設。有了這些預設，用戶就可以快速創建命令按鈕且無需再敲代碼。
		這些腳本的內容將會是被創建的命令按鈕的command，
		腳本的文件名將會是被創建的命令按鈕的標籤，並且文件名中所有的"_"字元將被替換成空格。
		比如使用了"Reset_Selection.mel"這個預設文件創建的命令按鈕，其標籤是"Reset Selection"。			
			
Converters:	內置的picker轉換器腳本.
		這些轉換器用來讀取其它picker程序的picker節點或文件。

HotkeySets:	用來在快捷鍵對話框裡顯示出快捷鍵。

Icons: 	MG-PickerStudio使用的圖標. 

Installer: MG-PickerStudio安裝器，裡面的安裝mel可以用來將工具裝到其它不同的maya版本。

LanguageRes: 	MG-Picker工作室內置的語言文件。目前只有英文，簡體中文，繁體中文。
		如果你有除英文中文外的語言翻譯文件，請郵件到mgpickerstudio@gmail.com，以便將來這個語言資源被正式發佈到程序目錄裡。

Plug-ins: 	MG-Picker工作室的插件文件. 

Python: 	Python API模塊.

ServerConfig:	手動修改的配置檔，用來改變程序行為. 目前主要用來修改浮動授權連接器的路徑。		
		這些修改將影響所有遠程調用該程序的用戶，像是程序的默認初始配置，不過可以被用戶本身的配置所覆蓋。

SnapshotStyles: 內置的圖片處理風格預設，主要用來截圖等的自動處理。
		所有的預設文件均以~字元開頭，以顯示這些預設是內置預設。
		不以"~"字元開頭的預設文件將被忽略。

Templates: 內置的Picker模板，你可以基於這些模板快速創建picker.
	   同時這些模板picker也可以被用做picker例子，從中瞭解如何用MG-Picker工作室創建picker.

Terms:	MG-Picker工作室的程序用戶協議及條款，請不要更動裡面內容。  

UI: 包含工具界面的腳本，請不要更動裡面內容。	

VersionHisotry: MG-Picker Studio版本釋出歷史。	

MGPicker.ver: 	MG-Picker工作室的當前版本數值，請不要更動裡面內容。

MGPicker_WrittenByMiguel.mel: 	MG-Picker工作室載入用mel，它也提供了工具不可或缺的腳本支持，請不要更動裡面內容。
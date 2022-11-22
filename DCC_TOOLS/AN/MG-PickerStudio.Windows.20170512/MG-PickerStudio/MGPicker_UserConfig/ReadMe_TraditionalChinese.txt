AutoSourced:	在裡面放置你想要在MG-Picker工作室啟動時就自動載入的mel或python指令碼。
		這些指令碼基本上是用來支援你的picker裡的程式碼功能的。
		MEL指令碼將會用source命令來自動載入，python指令碼將會用execfile()方式匯入。

CodeSnippets:	在裡面放置程式碼片段的指令碼，mel請放到裡面的MEL目錄，python指令碼請放到裡面的Python目錄。
		這些指令碼的內容，將來被使用時將會被插入到當前程式碼編輯器的滑鼠位置。

CommandButtonPresets:	使用者的命令按鈕預設。有了這些預設，使用者就可以快速創建命令按鈕且無需再敲程式碼。
		請在裡面放入這些預設的mel或python指令碼，並用他們的功能分類作為資料夾組織起來。
		這些指令碼的內容將會是被創建的命令按鈕的command，
		指令碼的檔名將會是被創建的命令按鈕的標籤，並且檔名中所有的"_"字元將被替換成空格。
		比如使用了"My_Command_Preset.mel"這個預設檔案創建的命令按鈕，其標籤是"My Command Preset"。			
			
Converters:	使用者的picker轉換器指令碼，目前只支援MEL.
		這些轉換器用來讀取其它picker程式的picker節點或檔案。

LanguageRes: 	MG-Picker工作室的語言檔案。
		如果你有除英文及中文外的語言翻譯檔案，請郵件到mgpickerstudio@gmail.com，以便將來這個語言資源被正式釋出到程式目錄裡。

SnapshotStyles: 圖片處理預設，在生成picker面板的背景圖時將自動被採用，在生成帶圖示的pose命令按鈕時也用到。

UIConfig: 	存儲介面在動畫師/設計師/最小化模式時的大小及位置。

GeneralConfig.ini: 		存儲使用者的配置。

PickerCreatingConfig.ini: 	存儲使用者創建picker物件的配置。
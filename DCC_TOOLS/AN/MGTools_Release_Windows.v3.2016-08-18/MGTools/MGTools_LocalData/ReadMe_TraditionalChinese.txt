MGTools_LocalData:	用來存儲所有MGTools使用者配置檔案的根目錄。
			以Maya的optionVar機制存儲的使用者配置不會存在這裡面, 
			而是存在Maya的使用者配置目錄裡的userPrefs.mel這個檔案。

MGTools_LicenseData:	當你線上上的多臺機子上分發MGTools時，
			這個資料夾用來接收使用者機子提交的使用者碼，機子IP等資訊。
			這些資訊接下來可以用在批量註冊MGTools上。
			基本上這個資料夾不會被安裝到您的本地機子上，只存在於MGTools安裝源裡。
			請檢視“分發MGTools”的幫助頁面來瞭解更多。

MGTools_GlobalData:	MGTools在Maya配置目錄的根目錄裡，創建了一個叫"MGTools_GlobalData"的目錄,
			一般路徑是 我的檔案/maya/MGTools_GlobalData。 
			這個目錄用來存儲MG-Pose動畫庫及MG-資產庫的本地端庫檔案。
			這個目錄獨立於所有的maya特定版本，可以為所有本機的所有裝了MGTools的不同版本maya同時使用。
			相對應的，MGTools_LocalData裡存儲的配置，則只為本機的單個Maya版本所用。
			
./MG_AnimationBank:	存儲MG-動畫銀行的檔案。用來匯出、匯入動畫。
			如果你要建立動畫庫，請用MG-Pose動畫庫工具。動畫銀行比較適合於只是匯出匯入動畫時用。

./MG_AutoLoadConfig:	存儲MGTools自動載入配置。
			在Maya啟動時，MGTools自動讀取這些配置，來自動載入相應的MGTools工具。

./MG_CamSwitchConfig:	存儲MG-攝像機切換配置檔案。
			這些配置檔案是一些攝像機的切換清單。

./MG_DisplaySet:	存儲MG-顯示層集。
			這些集存儲了顯示層的一些創建資訊，用來提升顯示層的創建效率。
			用MG-顯示層集工具來使用這些集。

./MG_HUDConfig:		存儲MG-螢幕資訊顯示工具的配置檔案。
			您可以在您的製作線上分享這些配置檔案，以統一大家playblast出來的視訊裡顯示的資訊。

	
./MG_OpenDirectoryConfig:	存儲資料夾快捷方式。
				使用這些資訊，你可以在Maya裡快速開啟瀏覽某個資料夾。
				
./MG_OpenExternalFileConfig:	存儲外部檔案快捷方式。
				使用這些資訊，你可以在Maya裡快速開啟某個檔案,或啟動某個外部程式，如Photoshop,Nuke等。

./MG_SelectionSet:	存儲MG-選擇集。

./MG_Shelves:		存儲MG-工具架。

./MG_SnapshotCameraBookmarks:	MGTools使用的攝像機書籤檔案，這些檔案每個都存儲了一個或多個攝像機的資訊。
				主要用來在MG-Pose動作庫及MG-資產庫中使用，來輔助這些工具生成圖示，預覽圖及預覽視訊。
				
./MG_UIConfig:		存儲了MGTools，約束工具，MG-工具架，軸心工具條這些介面的正常大小位置及最小化大小位置 
			（以 ".tmp"為副檔名的檔案)
			它也存儲了使用者的MGTools工具隱藏設定，即在MGTools工具條上，哪些工具不要顯示的設定。

./MG_UpdatePackages:	存儲MGTools的更新相關的資料包，及每個更新的描述文字。 

			UpdatePackages子目錄存儲了離線更新包(*.mgu), 由MGTools的線上更新工具自動下載。
			(當然也可以手動在網上下載)
			你可以把這些離線更新包複製到不能上網的機子上的MGTools同樣位置，然後使用"離線更新"工具應用這些更新。
			
			RollbackPackages子目錄裡存儲了撤消更新用的回捲資料(*.mgr)。
			你可以在MGTools裡使用這些回捲資料包，來使MGTools撤消最近的一些更新，重新恢復到舊版本。

./MG_UserIcon:		這個目錄用來供使用者存儲想在MGTools裡用的圖示。主要用來存儲MG-工具架所用的外部圖示。

./MG_ViewSwitchConfig:	存儲檢視切換工具的配置檔案。
			
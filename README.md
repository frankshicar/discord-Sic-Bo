# discord-Sic-Bo
## 專案描述
在當今的數位時代，遊戲不僅是娛樂的一種形式，更是人們社交互動的重要途徑。然而，大多數遊戲類 Discord 機器人往往涉及複雜的遊戲機制，且通常需要在公共群組中遊玩，這可能會對初學者或尋求簡單樂趣的玩家構成障礙。因此，我設計了「簡易樂趣骰寶」——一個輕鬆上手且充滿樂趣的 Discord 機器人，旨在為用戶提供一個簡單、刺激且私密的遊戲體驗。

這款機器人在本機運行，無需複雜的設置或維護。用戶只需執行簡單的命令，即可與朋友一起享受骰寶遊戲的樂趣，無論是在私人會話中還是在封閉的群組裡。遊戲規則直觀明瞭，使玩家無需深入瞭解複雜的背景知識即可快速上手。

且機器人具備玩家點數追蹤系統。通過連接到一個mysql資料庫，機器人能夠記錄玩家的點數，即使在機器人重啟後也能保持數據的持續性。這意味著玩家的每一次投注和勝利都將被記錄下來，增加了遊戲的連續性和參與感。

我的目標是創造一種輕鬆愉快的社交遊戲體驗，使玩家可以在享受遊戲的同時，也能與朋友保持互動。

## 專案功能
#### 使用者
- 註冊帳號
- 登入帳號
- 查看點數
- 查看遊戲規則
- 選擇要玩的玩法並下注


## 如何使用
### 操作程式
1. 資料庫設定
    1. 先至[mysql官網](https://dev.mysql.com/downloads/mysql/) 下載mysql，mac須再下載[mysql workbench](https://dev.mysql.com/downloads/workbench/)
    2. 建立一個名為`discord_players`的資料庫
    3. 在`discord_players`資料庫中建立`playsers`的資料表，並在資料表中建立`username`(主鍵)及`points`兩個欄位
2. discord 機器人建立
    1. 先至[discord官網](https://discord.com/)註冊discrod帳號
    2. 至[discord developers網站](https://discord.com/developers/applications)登入您的discord帳號
    3. 參考這篇文章[discord 機器人建立](https://ithelp.ithome.com.tw/articles/10319049)來創建您個人的機器人
3. 套件安裝
    1. 確認是否安裝python
       - mac: `python3 --version` 或 `pip3 --version`
       - windows: `python --version` 或 `pip --version`
    2. 安裝discord.py
       - mac: `pip3 install discord.py`
       - windows: `pip install discord.py`
    3. 安裝mysql-connector-python
       - mac: `pip3 install mysql-connector-python`
       - windows: `pip install mysql-connector-python`
    4. 安裝pyyaml
       - mac: `pip3 install pyyaml`
       - windows: `pip install pyyaml`
4. 程式運行
    1. Fork 這個專案
    2. 複製你剛剛 Fork 的專案至本地
    3. 打開SIC-BO.py
    4. 創建`config.yml`檔案
    5. 在`config.yml`檔案中輸入
      ```
      bot_token: "your_bot_token"
      guild_id: "your_guild_id"
      ```
      



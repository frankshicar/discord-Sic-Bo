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
      
## 如何玩
### 1. 註冊帳號
首先輸入`/register`註冊一個使用者 
<br>
<img width="302" alt="截圖 2024-02-19 下午4 16 18" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/7557ac8a-7638-4b57-b5ab-5d45afeb869c">
<br>
<br>
<img width="293" alt="截圖 2024-02-19 下午4 10 12" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/279fc7bc-c04b-41d4-bb47-95f0cc142da7">
<br>

### 2. 登入
將註冊過後的使用`/login`輸入用戶名進行登入
<br>
<img width="288" alt="截圖 2024-02-19 下午4 17 12" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/3323e886-e390-487d-93eb-502f2e1a24d7">
<br>
<br>
<img width="279" alt="截圖 2024-02-19 下午4 19 01" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/20fc9151-eef6-4aec-8b1d-c75e73fb2868">
<br>

### 3. 查看遊戲規則
使用`/rule`查看不同玩法的規則及賠率
<br>
<img width="489" alt="截圖 2024-02-19 下午4 20 51" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/95aef62f-66a1-4b32-b50b-b5f7e2828a57">
<br>

### 4. 查看分數
使用`/points輸入玩家名稱查看玩家分數
<br>
<img width="302" alt="截圖 2024-02-19 下午4 23 06" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/8b7e812f-0792-4c32-9214-c8e1962eb877">
<br>

### 5. 根據規則來選擇玩法
以大小當作範例
使用`/大小`輸入你要猜大或小病輸入你要下注多少點
<br>
<img width="333" alt="截圖 2024-02-19 下午4 26 18" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/3267d5f4-999a-455b-b578-4d0cda93ff58">
<br>
<br>
<img width="356" alt="截圖 2024-02-19 下午4 26 48" src="https://github.com/frankshicar/discord-Sic-Bo/assets/93965977/d0cba31e-ae6b-4b8c-bb79-147120e2ed8e">
<br>



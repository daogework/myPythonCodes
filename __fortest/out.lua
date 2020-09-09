local CircleBroadcastMessage
local CommonModule = {
    ctor = function(self)
        self.AutoRegister = true
        self.itemList = {}
        self.levelUpItemList = {}
    end,

    waitLockCount = 0,
    WaitLockCount = {
        get = function(self)  return self.waitLockCount end,
        set = function(self, value) 
            if (value > 0) then
                UIManager.Instance.OpenUI(EnumUIType.WaitResponseUI)
            else
                UIManager.Instance.CloseUI(EnumUIType.WaitResponseUI) end
            self.waitLockCount = value
        end,
    },

    OnLoad = function(self)
        local oldonPlayerLevelChanged = self.onPlayerLevelChanged
        self.onPlayerLevelChanged = function(msg) oldonPlayerLevelChanged(self, msg) end
        MessageCenter.Instance:AddListener(MsgType.CLIENT_PLAYER_LEVEL, self.onPlayerLevelChanged)

        local oldonPlayerVIPLevelChanged = self.onPlayerVIPLevelChanged
        self.onPlayerVIPLevelChanged = function(msg) oldonPlayerVIPLevelChanged(self, msg) end
        MessageCenter.Instance:AddListener(MsgType.CLIENT_PLAYER_VIPLEVEL, self.onPlayerVIPLevelChanged)

        local oldmessageBroadcastNtf = self.messageBroadcastNtf
        self.messageBroadcastNtf = function(msg) oldmessageBroadcastNtf(self, msg) end
        MessageCenter.Instance:AddListener(MsgType.NET_MESSAGEBROADCAST_NTF, self.messageBroadcastNtf)

    end,

    OnRelease = function(self)
        MessageCenter.Instance:RemoveListener(MsgType.CLIENT_PLAYER_LEVEL, self.onPlayerLevelChanged)
        MessageCenter.Instance:RemoveListener(MsgType.CLIENT_PLAYER_VIPLEVEL, self.onPlayerVIPLevelChanged)
        MessageCenter.Instance:RemoveListener(MsgType.NET_MESSAGEBROADCAST_NTF, self.messageBroadcastNtf)
    end,

    Update = function(self)
        --  Debug.Log("CommonModule Update")
        if (not openUI) then
            if (not(circleBroadcastList==nil) and circleBroadcastList.Count > 0) then
                local serverTime = TimeHelper.GetServerTimestamp()
                if (circleBroadcastList.First().Timestamp <= serverTime) then
                    UIManager.Instance:OpenUI(EnumUIType.SystemNoticeUI)
                    self.openUI = true
                end
            end
        end
    end,

    --#region award
    itemList = nil,
    SetItemData = function(self,itemInfos,action)
        itemList:Clear()
        if (not(itemInfos==nil)) then
            local len = itemInfos.Length
            for  i = 0, (len-1) do
                itemList.Add(itemInfos[i]) end
        end
        UIManager.Instance:OpenUI(EnumUIType.AwardUI, action)
    end,
    SetPlayerCoin = function(self)
        --local player = ((GamePlayer)GlobalLuaShareWithCSharp.GetObj("GamePlayer"))
    end,
    GetShowItemList = function(self)
        return itemList
    end,
    GetShowLevelUpItemList = function(self)
        return levelUpItemList
    end,
    --#endregion

    --#region levelUp
    levelUpItemList = nil,
    onPlayerLevelChanged = function(self,msg)
        levelUpItemList:Clear()
        local itemArr = msg["Rewards"]
        if (not(itemArr==nil)) then
            local len = itemArr.Length
            for  i = 0, (len-1) do
                levelUpItemList.Add(ItemInfo(itemArr[i].item_id, itemArr[i].item_sub_id, itemArr[i].item_count)) end
        end
        UIManager.Instance:OpenUI(EnumUIType.LevelUpUI)
    end,

    onPlayerVIPLevelChanged = function(self,msg)
        local isChanged = bool.Parse(msg["VIPLevelChange"]:ToString())
        if (isChanged) then
            UIManager.Instance:OpenUI(EnumUIType.VIPLevelUpUI)
        end
    end,
    --#endregion

    --#region 系统消息
    --消息通知
    messageBroadcasQueue = nil,
    circleBroadcastList = nil,
    openUI = false,
    messageBroadcastNtf = function(self,msg)
        local rsp = msg.Content
        if ((messageBroadcasQueue==nil)) then
            self.messageBroadcasQueue = newQueue() end
 --TO DO 上面一句是方括号类型 typename=CLPFMessageBroadcastNtf
        if (rsp.type == 12) then
            if ((circleBroadcastList==nil)) then
                self.circleBroadcastList = {} end

            parseCircleBroadcast(rsp)

            if (not openUI) then
                UIManager.Instance:OpenUI(EnumUIType.SystemNoticeUI)
                self.openUI = true
            end
        elseif (rsp.type == 13) then
            local contents = JArray.Parse(rsp.content)
            local msgId = int.Parse(contents[0]:ToString())
            local count = circleBroadcastList.Count
            for  i = (count - 1), 0, -1 do
                local broadcast = circleBroadcastList[i]
                if (msgId == broadcast.Id) then
                    circleBroadcastList.Remove(broadcast) end
            end
        else
            messageBroadcasQueue.Enqueue(rsp)
            if (not openUI) then
                UIManager.Instance:OpenUI(EnumUIType.SystemNoticeUI)
                self.openUI = true
            end
        end
    end,

    GetMessageBroadcastDequeue = function(self)
        self.CLPFMessageBroadcastNtfntf = nil

        if (not(circleBroadcastList==nil) and circleBroadcastList.Count > 0) then
            local serverTime = TimeHelper.GetServerTimestamp()
            if (circleBroadcastList.First().Timestamp <= serverTime) then
                self.ntf = circleBroadcastList.First().Ntf
                circleBroadcastList.RemoveAt(0)
                return ntf
            end
        end

        if (not(messageBroadcasQueue==nil) and messageBroadcasQueue.Count > 0) then
            self.ntf = messageBroadcasQueue.Dequeue()
        else
            self.messageBroadcasQueue = nil
            self.openUI = false
        end
        return ntf
    end,

    OnCloseSystemNotice = function(self)
        self.openUI = false
    end,

    parseCircleBroadcast = function(self,rsp)
        local contents = JArray.Parse(rsp.content)
        local msgId = int.Parse(contents[0]:ToString())
        local sendTime = ulong.Parse(contents[1]:ToString()) * 1000
        local lastTime = ulong.Parse(contents[2]:ToString()) * 1000
        local interval = ulong.Parse(contents[3]:ToString()) * 1000
        local message = contents[4]:ToString()
        local endTime = sendTime + lastTime
        local curTime = sendTime

--TODO 这里是do while,需要处理
        while (curTime <= endTime) do
            circleBroadcastList.Add(CircleBroadcastMessage.ctor(msgId, curTime, message, rsp))
            curTime = curTime + interval
        end

        sortCircleBroadcast()
    end,

    sortCircleBroadcast = function(self)
        circleBroadcastList.Sort(function(a, b)
            if (a.Timestamp > b.Timestamp) then return 1
            elseif (a.Timestamp == b.Timestamp) then return 0
            else return -1 end
        end)
    end,
    --#endregion
}

CircleBroadcastMessage = {
    Id = nil,
    Timestamp = nil,
    Message = nil,
    Ntf = nil,

    ctor = function(self,id,timestamp,message,ntf)
        self.Id = id
        self.Timestamp = timestamp
        self.Message = message
        self.Ntf = ntf
		return self
    end,
}



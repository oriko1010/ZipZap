import json
import re
from datetime import datetime
import os

def charaCollection(response):
    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        response['charaList'] = json.load(f)

def charaListCompose(response):
    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        response['charaList'] = json.load(f)
    with open('data/user/userCardList.json', encoding='utf-8') as f:
        response['cardList'] = json.load(f)

def charaTop(response):
    with open('data/user/gameUser.json', encoding='utf-8') as f:
        response['gameUser'] = json.load(f)

def configTop(response):
    with open('data/user/user.json', encoding='utf-8') as f:
        user = json.load(f)
    response['canChangeLoginName'] = True
    response['setPassword'] = user['setPassword']

def followTop(response):
    with open('data/user/userFollowList.json', encoding='utf-8') as f:
        response['userFollowList'] = json.load(f)
    with open('data/user/user.json', encoding='utf-8') as f:
        user = json.load(f)
    response['followers'] = user['followCount']
    response['blocked'] = 0

def gachaHistory(response):
    with open('data/user/gachaHistoryList.json', encoding='utf-8') as f:
        response['gachaHistoryList'] = json.load(f)
    response['gachaHistoryCount'] = len(response['gachaHistoryList'])

def gachaTop(response):
    with open('data/user/userGachaGroupList.json', encoding='utf-8') as f:
        response['userGachaGroupList'] = json.load(f)
    with open('data/gachaScheduleList.json', encoding='utf-8') as f:
        response['gachaScheduleList'] = json.load(f)

def magiRepo(response):
    with open('data/magiRepoList.json', encoding='utf-8') as f:
        response['magiRepoList'] = json.load(f)

def pieceArchive(response):
    with open('data/user/userPieceList.json', encoding='utf-8') as f:
        userPieceList = json.load(f)
    response['userPieceArchiveList'] = [userPiece for userPiece in userPieceList if userPiece['archive']]

def pieceCollection(response):
    response['userPieceCollectionList'] = []

def presentList(response):
    response['presentList'] = []

def shopTop(response):
    with open('data/shopList.json', encoding='utf-8') as f:
        response['shopList'] = json.load(f)
    with open('data/user/userShopItemList.json', encoding='utf-8') as f:
        response['userShopItemList'] = json.load(f)

def storyCollection(response):
    response['eventStoryList'] = []
    response['arenaBattleFreeRankClassList'] = []
    with open('data/user/userArenaBattle.json', encoding='utf-8') as f:
        response['userArenaBattle'] = json.load(f)

def supportSelect(response):
    with open('data/npc.json', encoding='utf-8') as f:
        npc = json.load(f)
    response['npcHelpList'] = [npc]

specialCases = {
    "CharaCollection": charaCollection,
    "CharaTop": charaTop,
    "ConfigTop": configTop,
    "FollowTop": followTop,
    "GachaHistory": gachaHistory,
    "GachaTop": gachaTop,
    "GachaResult": gachaTop,
    "MagiRepo": magiRepo,
    "PieceArchive": pieceArchive,
    "PieceCollection": pieceCollection,
    "PresentList": presentList,
    "ShopTop": shopTop,
    "StoryCollection": storyCollection,
    "SupportSelect": supportSelect
}

# TODO: clear history on first day's login
def login(user):
    print('logging in')
    nowstr = str(datetime.now()).split('.')[0].replace('-', '/')
    lastLogin = datetime.strptime(user['lastLoginDate'], '%Y/%m/%d %H:%M:%S')
    if (lastLogin.date()-datetime.today().date()).days == 1:
        user['loginDaysInRow'] += 1
        user['todayFirstAccessDate'] = nowstr
        user['dataPatchedAt'] = nowstr
    
    user['loginCount'] += 1
    user['penultimateLoginDate'] = user['lastLoginDate']
    user['lastLoginDate'] = nowstr
    user['lastAccessDate'] = nowstr
    user['indexingTargetDate'] = nowstr
    return user

def addArgs(response, args, isLogin):
    with open('data/user/user.json', encoding='utf-8') as f:
        user = json.load(f)

    lastLogin = datetime.strptime(user['lastLoginDate'], '%Y/%m/%d %H:%M:%S')
    # need to check if midnight passed; logins have to happen then too
    if isLogin or (lastLogin.date()-datetime.today().date()).days > 0:
        user = login(user)
        with open('data/user/user.json', 'w+', encoding='utf-8') as f:
            json.dump(user, f, ensure_ascii=False)

    for arg in args:
        if arg in ['user', 'gameUser', 'userStatusList',
        'userLive2dList', 'userCardList', 'userCharaList', 'userDeckList', 'userFormationSheetList',
        'userPieceList', 'userPieceSetList', 'userItemList', 'userSectionList', 'userGiftList',
        'userQuestAdventureList', 'userQuestBattleList', 'userChapterList']:
            print('loading ' + arg + ' from json')
            with open('data/user/'+arg+'.json', encoding='utf-8') as f:
                response[arg] = json.load(f)
        elif arg.lower().endswith('list'):
            response[arg] = []

def handlePage(request, isLogin):
    with open('data/events.json', encoding='UTF-8') as f:
        response = json.load(f)

    endpoint_and_args = request.path.replace('/magica/api/page/', '')
    endpoint, args = endpoint_and_args.split('?')
    args = re.sub(r'&timeStamp=\d+', '', args) \
            .replace('value=', '') \
            .split(',')

    if endpoint in specialCases.keys():
        specialCases[endpoint](response)
    
    if endpoint=='ResumeBackground':
        print('resuming')

    addArgs(response, args, isLogin)
    
    return json.dumps(response)
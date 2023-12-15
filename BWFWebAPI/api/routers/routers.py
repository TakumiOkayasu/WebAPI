from fastapi import APIRouter
from typing import List
import api.schemas.schemas as player_schema
import requests
from bs4 import BeautifulSoup

router = APIRouter()

# プレイヤーの検索結果一覧を取得
@router.get("/find/{keyword}", response_model=List[player_schema.PlayerInfo])
async def get_player_list(keyword: str):
    if len(keyword) < 3:
        return []
    
    search_url_prefix = "https://bwf.tournamentsoftware.com/find/player?q="
    res = requests.get(search_url_prefix + keyword.replace(' ', '+'))
    soup = BeautifulSoup(res.content, 'html.parser')
    player_elems = [ elems for elems in soup.find_all('h5', {'class': 'media__title'})]
    ret = []

    for e in player_elems:
        tmp = player_schema.PlayerInfo()
        tmp.profile = e.a.get('href').replace('/player-profile/', '')
        d = e.find_all('span')
        tmp.name = d[0].text
        tmp.id = int(d[1].text.replace('(','').replace(')',''))
        ret.append(tmp)

    return ret

# IDで指定した選手のアイコン画像を取得
@router.get("/icon/{id}")
async def get_player_icon_url(id: int):
    # この後ろにIDを追加すれば自動的にプロフィール画面に飛べる
    profile_url = "https://bwfbadminton.com/player/"
    # リダイレクト先のURLを取得する
    res = requests.get(profile_url + str(id) + "/")
    print( res )
    redirect_url = res.headers#["Location"]
    print( redirect_url )
    # 要素を取得
    #profile_page = requests.get(redirect_url)
    #soup = BeautifulSoup(profile_page.content, 'html.parser')
    #elements = soup.find_all('div', { 'class': 'playertop-avatar'} )
    #print( elements )
    return
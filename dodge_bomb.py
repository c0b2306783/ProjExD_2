import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
        pg.K_UP:(0, -5),
        pg.K_DOWN:(0, 5),
        pg.K_LEFT:(-5, 0),
        pg.K_RIGHT:(5, 0),
        }

def game_over(screen: pg.Surface) -> None:
    """
    引数:screen
    戻り値:None
    """
    # ブラックアウト実装
    bl_img = pg.Surface((WIDTH, HEIGHT))  # 空のSurface
    pg.draw.rect(bl_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    pg.Surface.set_alpha(bl_img, 128)
    bl_rct = bl_img.get_rect()
    bl_rct = 0, 0

    # ぴえんこうかとん2匹
    crkk_img = pg.image.load("fig/8.png")
    crkk_rct1 = crkk_img.get_rect()
    crkk_rct2 = crkk_img.get_rect()
    crkk_rct1 = WIDTH/2-200, HEIGHT/2-50
    crkk_rct2 = WIDTH/2+200, HEIGHT/2-50
    
    # Game Overの文字列
    owarimoji = pg.font.Font(None, 80)
    txt = owarimoji.render("Game Over", True, (255, 255, 255))

    # 表示
    screen.blit(bl_img, bl_rct)
    screen.blit(crkk_img, crkk_rct1)
    screen.blit(crkk_img, crkk_rct2)
    screen.blit(txt, (WIDTH/2-130, HEIGHT/2-50))

    pg.display.update()

    # 五秒表示
    time.sleep(5)

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数:こうかとんRectか爆弾Rect
    戻り値:真理値タプル(yoko, tate)。画面内でTrue
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # こうかとんの頭が画面上から出たらor脚が画面下から出たら
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)

    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # bb_imgに赤い半径10の円を書く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾の中心座標設定
    vx, vy = 5, 5

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # ゲームオーバー判定
            game_over(screen)
            return

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key,tpl in DELTA.items():  # 辞書に.items()するとキーと値がタプルで取り出せる
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]


        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # こうかとんが画面外なら元の場所へ戻す
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出たら
            vx *= -1
        if not tate:  # 縦にはみ出たら
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

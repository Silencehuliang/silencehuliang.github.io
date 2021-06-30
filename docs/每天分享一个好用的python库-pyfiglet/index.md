# 每天分享一个好用的Python库-pyfiglet


## 前言

学习`Linux`命令的朋友们肯定都学过或者听说过`figlet`这个有趣的命令，今天分享是`Python`中实现这个命令的第三方库：`pyfiglet`。

## pyfiglet

### 简介

`pyfiglet`是用Python写的figlet命令的第三方库，可以使用字符组成ASCII艺术图片。

### 安装

```python
pip install pyfiglet
```

### 简单使用

- 查看可以使用的字体
	- 在`Python`文件中查看

    ```python
    >>> from pyfiglet import FigletFont
    >>> FigletFont().getFonts()
    ['clb6x10', 'nipples', 'computer', 'charact1', 'xtty', 'xcourb', 'xchartr', 'future_1', 'lcd', 'letters', 'fp2_____', 'rev', 'caus_in_', 'roman___', 'barbwire', 'threepoint', 'smkeyboard', 'couri', '1943____', 'heroboti', 'madrid', 'grand_pr', '3-d', 'radical_', 'atc_____', 'bubble_b', 'skate_ro', 'xsans', 'aquaplan', 'nvscript', 'brite', 'p_s_h_m_', 'tiles', 'xsbooki', 'pyramid', 'crawford', 'charact2', 'utopiai', 'future_2', 'shadow', 'italics_', 'asslt__m', 'new_asci', 'future_3', 'c2______', 'characte', 'charact3', 'sans', 'xsansbi', 'com_sen_', 'bulbhead', 'clr5x8', 'mshebrew210', 'doh', 'script__', 'platoon2', 'nancyj-fancy', 'mike', 'odel_lak', 'sansb', 'b_m__200', 'dwhistled', 'slide', 'future_7', 'joust___', '5x8', 't__of_ap', 'smscript', 'xbritebi', 'convoy__', 'alligator', 'graceful', 'gothic__', 'starwars', 'cli8x8', 'future_6', 'charact6', 'super_te', 'zig_zag_', 'xsansi', 'relief2', 'atc_gran', 'basic', 'vortron_', 'sm______', 'tecrvs__', 'pawn_ins', 'clb8x10', 'colossal', 'decimal', 'britei', 'unarmed_', 'funky_dr', 'jerusalem', 'fbr_stri', 'charact4', 'future_4', 'small', 'dcs_bfmo', 'future_5', 'britebi', 'charact5', 'courbi', 'morse', 'fender', 'clr7x8', 'notie_ca', '6x10', 'usaflag', 'hollywood', 'skateord', 'poison', 'pepper', 'rot13', 'coil_cop', 'master_o', 'puffy', 'raw_recu', 'times', 'eftitalic', 'stencil1', 'a_zooloo', 'catwalk', 'cour', 'isometric1', 'chunky', 'xcour', 'xbriteb', 'inc_raw_', 'yie-ar__', 'eftifont', 'tsalagi', 'block', 'rainbow_', 'mirror', 'avatar', 'defleppard', 'clr5x10', 'ok_beer_', 'stealth_', 'runyc', 'thick', 'univers', 'isometric3', 'top_duck', 'stencil2', 'utopiabi', 'alphabet', 'assalt_m', 'isometric2', 'banner3-D', 'ugalympi', 'char3___', 'script', 'tty', 'fair_mea', 'ti_pan__', 'ripper!_', 'war_of_w', '6x9', 'slscript', 'asc_____', 'fbr12___', 'twopoint', 'kgames_i', 'cosmike', 'deep_str', 'tsm_____', '4x4_offr', 'house_of', 'mnemonic', 'rok_____', 'clr7x10', 'nancyj-underlined', 'xhelvbi', '5lineoblique', 'tav1____', 'greek', 'eftiwater', '64f1____', 'subteran', 'sbookb', 'eftirobot', 'eftipiti', 'tombstone', 'modern__', 'kban', 'italic', 'clr6x8', 'smshadow', 'char1___', 'whimsy', 'cursive', 'hyper___', 'heavy_me', 'binary', 'xsbook', 'fbr_tilt', 'street_s', 'mini', 'xhelv', 'xhelvi', 'helv', 'helvb', 'isometric4', 'sblood', 'road_rai', 'ticks', 'fireing_', 'tsn_base', 'spc_demo', 'nancyj', 'rad_____', 'diamond', 'sketch_s', 'eftiwall', 'straight', 'sbookbi', 'xchartri', 'stellar', 'bubble__', 'pacos_pe', 'wavy', 'rci_____', 'beer_pub', 'invita', 'slant', 'bubble', 'npn_____', 'taxi____', 'marquee', 'twin_cob', 'clr6x6', 'rastan__', 'eftichess', 'contrast', 'cricket', 'trek', 'gothic', 'ascii___', 'goofy', 'speed', 'calgphy2', 'clr8x8', 'krak_out', 'z-pilot_', 'phonix__', 'cybersmall', 'banner3', 'zone7___', 'pebbles', 'platoon_', 'ebbs_1__', 'coinstak', 'green_be', 'letterw3', 'digital', 'demo_1__', 'fourtops', 'gauntlet', 'moscow', 'xbritei', 'xtimes', 'yie_ar_k', 'maxfour', 'f15_____', 'clr4x6', 'fraktur', 'hypa_bal', 'hills___', 'e__fist_', 'char4___', 'term', 'usa_pq__', 'chartri', 'katakana', 'ticksslant', 'xsbookbi', 'rockbox_', 'xcourbi', 'caligraphy', 'fbr2____', 'relief', 'chartr', 'jazmine', 'sbook', 'dotmatrix', 'nfi1____', 'mayhem_d', 'banner4', 'home_pak', 'doom', 'helvi', 'linux', 'tengwar', 'battlesh', 'xhelvb', 'lexible_', 'rowancap', 'peaks', 'mig_ally', 'ivrit', 'rad_phan', 'ghost_bo', 'acrobatic', 'contessa', 'battle_s', 'eca_____', 'ntgreek', 'smtengwar', 'flyn_sh', 'cyberlarge', 'larry3d', 'rounded', 'devilish', 'short', 'faces_of', 'type_set', 'hex', 'usa_____', 'tanja', 'r2-d2___', 'sbooki', 'big', 'rectangles', 'fp1_____', 'sansbi', 'c_consen', 'epic', 'pawp', 'utopia', 'p_skateb', 'c_ascii_', 'arrows', 'shimrod', 'char2___', 'xbrite', 'helvbi', 'smisome1', 'lockergnome', 'drpepper', 'magic_ma', 'graffiti', 'future_8', 'ebbs_2__', '5x7', 'tec_7000', 'star_war', 'letter_w', 'skateroc', 'fbr1____', 'gradient', 'utopiab', 'ts1_____', 'xsbookb', 'clr8x10', 'charset_', 'timesofl', 'high_noo', 'clr5x6', 'stop', 'xttyb', 'tomahawk', 'broadway', 'o8', 'tinker-toy', 'courb', 'etcrvs__', 'c1______', 'stacey', 'alligator2', 'demo_2__', 'triad_st', 'octal', 'lean', 'd_dragon', 'bell', 'ucf_fan_', 'xcouri', 'lazy_jon', 'rozzo', 'demo_m__', 'ttyb', 'fairligh', 'hades___', 'fuzzy', 'os2', 'smslant', 'rampage_', 'tubular', 'finalass', 'tec1____', 'ogre', 'stampatello', 'pod_____', 'rally_sp', 'clb8x8', 'outrun__', 'weird', 'kik_star', 'serifcap', 'briteb', 'mcg_____', 'standard', 'trashman', 'thin', 'xsansb', 'cybermedium', 'space_op', 'cosmic', 'fantasy_', 'double', 'advenger', 'druid___', 'sansi', 'rally_s2', 'mad_nurs', 'clr6x10', '3x5', 'bigchief', 'baz__bil', 'roman', 'runic', 'panther_', 'banner']
    ```
    
  - 在终端中查看
  
    ```bash
    pyfiglet -l 
    或
    pyfiglet --list_fonts
    ```
  
- 选一个喜欢的字体来输出艺术字吧

  ```python
  >>> from pyfiglet import Figlet
  >>> f = Figlet(font="xtty")
  >>> f.renderText('Life is short, I use Python！')
  '                                                                   \n       #   ###          #             #                            \n#         #                           #               #        ### \n#    ### ####   ##    ###  ###    ### # #   ##  # ## ####       #  \n#      #  #    #  #     # #      #    ## # #  # ## #  #         #  \n#      #  #    ####     # ##     ##   #  # #  # #     #         #  \n#      #  #    #        #   ##     ## #  # #  # #     #         #  \n#      #  #    #        #    #      # #  # #  # #     #    #    #  \n####   #  #     ###     # ###    ###  #  #  ##  #      ##  #   ### \n                                                           #       \n                                                          #        \n                                               \n                                #              \n                 ###        #   #              \n#  #  ###  ##    #  # #  # #### # #   ##  # #  \n#  # #    #  #   #  # #  #  #   ## # #  # ## # \n#  # ##   ####   ###  #  #  #   #  # #  # #  # \n#  #   ## #      #     ##   #   #  # #  # #  # \n# ##    # #      #     ##   #   #  # #  # #  # \n # # ###   ###   #     #     ## #  #  ##  #  # \n                      #                        \n                      #                        \n'
  
  ```
  
  这里由于不能换行看的不是很清楚我们可以在`pycharm`中运行查看
  
  ![pyfiglet展示](//tvax3.sinaimg.cn/large/00729CCqgy1gs0a1orf40j30w80dbmz3.jpg)
  
- 上面由于太长了到了第二行，我们也可以指定宽度

  ```python
  from pyfiglet import Figlet
  
  f = Figlet(width=2000)
  print(f.renderText("Life is short, I use Python！"))
  ```
![pyfiglet指定宽度](//tvax2.sinaimg.cn/large/00729CCqgy1gs0a5h24vaj319406g0uf.jpg)

### 作用

写代码也可以是有趣的，可以通过这个库实现一些有趣的展示效果！

## 尾巴

`Python`中还有很多第三方库是`Linux`命令的`Python`版本，大家还知道那些，欢迎留言讨论呀~

[官方文档地址](https://pypi.org/project/pyfiglet/)

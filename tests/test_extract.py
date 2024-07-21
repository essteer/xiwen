import os
import unittest
from src.xiwen.utils.config import ENCODING
from src.xiwen.utils.extract import filter_hanzi_by_unicode, filter_hanzi_from_html


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))

TEST_CASES = {
    # Simplified only
    "bjzd.txt": ["Simplified", 18896, 1751, 18647, 13477, 249],
    # Traditional only
    "ttc.txt": ["Traditional", 5686, 810, 4390, 5466, 206],
    # Latin alphabet (no hanzi)
    "iliad.txt": ["Unknown", 0, 0, 0, 0, 0],
    # Unknown - 50:50 simplified : traditional
    "ping50.txt": ["Unknown", 360, 2, 180, 180, 0],
    # Unknown - 50:50 simplified : traditional
    "mix50.txt": ["Unknown", 40, 40, 20, 20, 0],
    # Simplified - 90:10 simplified : traditional
    "mix90.txt": ["Simplified", 20, 20, 18, 1, 1],
    # Traditional - 10:90 simplified : traditional
    "mix10.txt": ["Traditional", 20, 20, 1, 18, 1],
}


class TestFilterHanzi(unittest.TestCase):
    def test_character_filter(self):
        """Test bools are correct for hanzi"""
        hanzi = "爱气车电话点脑视东读对儿饭飞机钟兴个燚"
        self.assertEqual(
            [filter_hanzi_by_unicode(zi) for zi in hanzi], [True for _ in hanzi]
        )

    def test_non_hanzi_filter(self):
        """Test non-Chinese characters and punctuation filtered out"""
        hanzi = "爱a气3车g电6话h点6脑j视D东@读$对{儿y饭s飞X机O钟3兴;个.燚p"
        self.assertEqual(
            [filter_hanzi_by_unicode(zi) for zi in hanzi],
            [True if i % 2 == 0 else False for i in range(len(hanzi))],
        )

    def test_hanzi_punctuation(self):
        """Test Chinese punctuation is filtered out"""
        hanzi = "爱。气！车、电，话；点'脑"
        self.assertEqual(
            [filter_hanzi_by_unicode(zi) for zi in hanzi],
            [True if i % 2 == 0 else False for i in range(len(hanzi))],
        )


class TestFilterText(unittest.TestCase):
    def test_only_simplified_hanzi(self):
        """Test all characters returned from simplified Chinese"""
        # Pure Chinese
        simp = "当发获饥罗弥铺签叹坛团为纤绣须赞脏证钟涩卤恶线荡仑苏汇历尽复炉锐挣壶哑纷搅忆类绳谚凭榄烃剂睁谓轧旧滩犹卢选纠储蝉届腊双见键遥螨蛴质阎宾够饶烂乌剥评湾剑涨绩风渔项铝献厅滨蝼饲恋尘马"
        self.assertEqual(filter_hanzi_from_html(simp), [x for x in simp])
        # Chinese in HTML
        html = " <h1>郝景芳《北京折叠》</h1>\n<h3>（1）</h3>\n<p>清晨4:50，老刀穿过熙熙攘攘的步行街，去找彭蠡。</p>\n<p>从垃圾站下班之后，老刀回家洗了个澡，换了衣服。白色衬衫和褐色裤子，这是他唯一一套体面衣服，衬衫袖口磨了边，他把袖子卷到胳膊肘。老刀四十八岁，没结婚，已经过了注意外表的年龄，又没人照顾起居，这一套衣服留着穿了很多年，每次穿一天，回家就脱了叠上。他在垃圾站上班，没必要穿得体面，偶尔参加谁家小孩的婚礼，才拿出来穿在身上。这一次他不想脏兮兮地见陌生人。他在垃圾站连续工作了五小时，很担心身上会有味道。</p>\n<p>步行街上挤满了刚刚下班的人。拥挤的男人女人围着小摊子挑土特产，大声讨价还价。食客围着塑料桌 子，埋头在酸辣粉的热气腾腾中，饿虎扑食一般，白色蒸汽遮住了脸。油炸的香味弥漫。货摊上的酸枣和核桃堆成山，腊肉在头顶摇摆。这个点是全天最热闹的时间，基本都收工了，忙碌了几个小时的人们都赶过来吃一顿饱饭，人声鼎沸。</p>\n<p>老刀艰难地穿过人群。 端盘子的伙计一边喊着让让一边推开挡道的人，开出一条路来，老刀跟在后面。</p>\n<p>彭蠡家在小街深处。老刀上楼，彭蠡不在家。 问邻居，邻居说他每天快到关门才回来，具体几点不清楚。</p>\n"
        simp = "郝景芳北京折叠清晨老刀穿过熙熙攘攘的步行街去找彭蠡从垃圾站下班之后老刀回家洗了个澡换了衣服白色衬衫和褐色裤子这是他唯一一套体面衣服衬衫袖口磨了边他把袖子卷到胳膊肘老刀四十八岁没结婚已经过了注意外表的年龄又没人照顾起居这一套衣服留着穿了很多年每次穿一天回家就脱了叠上他在垃圾站上班没必要穿得体面偶尔参加谁家小孩的婚礼才拿出来穿在身上这一次他不想脏兮兮地见陌生人他在垃圾站连续工作了五小时很担心身上会有味道步行街上挤满了刚刚下班的人拥挤的男人女人围着小摊子挑土特产大声讨价还价食客围着塑料桌子埋头在酸辣粉的热气腾腾中饿虎扑食一般白色蒸汽遮住了脸油炸的香味弥漫货摊上的酸枣和核桃堆成山腊肉在头顶摇摆这个点是全天最热闹的时间基本都收工了忙碌了几个小时的人们都赶过来吃一顿饱饭人声鼎沸老刀艰难地穿过人群端盘子的伙计一边喊着让让一边推开挡道的人开出一条路来老刀跟在后面彭蠡家在小街深处老刀上楼彭蠡不在家问邻居邻居说他每天快到关门才回来具体几点不清楚"
        self.assertEqual(filter_hanzi_from_html(html), [x for x in simp])

    def test_only_traditional_hanzi(self):
        """Test all characters returned from traditional Chinese"""
        # Pure Chinese
        trad = "闆闢錶彆蔔佈纔綵蟲醜齣邨噹黨澱弔鼕髮範豐穀僱颳廣鬨後穫幾機饑姦薑藉捲剋睏誇囉纍釐灕樑瞭黴瀰衊麼麼蘋僕舖樸籤捨瀋勝術鬆祂歎罈妳體衕塗糰餵爲縴鹹絃繡鬚燻醃葉傭湧遊於餘籲鬱慾禦願嶽雲讚"
        self.assertEqual(filter_hanzi_from_html(trad), [x for x in trad])
        # Chinese in HTML
        html = " <h1>老子《道德經》</h1>\n<h3>第一章</h3>\n<p>道可道，非常道。名可名，非常名。無，名天地之始﹔有，名萬物之母。\n故常無，欲以觀其妙；常有，欲以觀其徼。此兩者，同出而異名，同謂之\n玄。玄之又玄，眾妙之門。</p>\n<h3>第二章</h3>\n<p>天下皆知美之為美，斯惡矣﹔皆知善之為善，斯不善矣。故有無相生，難\n易相成，長短相形，高下相傾，音聲相和，前後相隨。是以聖人處「無為\n」之事，行「不言」之教。萬物作焉而不辭，生而不有，為而不恃，功成\n而弗居。夫唯弗居，是以不去。</p>\n<h3>第三章</h3>\n<p>不尚賢，使民不爭﹔不貴難得之貨，使民不為盜﹔不見可欲，使民心不亂\n。是以「聖人」之治，虛其心，實其腹，弱其志，強其骨。常使民無知無\n欲。使夫智者不敢為也。為「無為」，則無不治。</p>\n"
        trad = "老子道德經第一章道可道非常道名可名非常名無名天地之始有名萬物之母故常無欲以觀其妙常有欲以觀其徼此兩者同出而異名同謂之玄玄之又玄眾妙之門第二章天下皆知美之為美斯惡矣皆知善之為善斯不善矣故有無相生難易相成長短相形高下相傾音聲相和前後相隨是以聖人處無為之事行不言之教萬物作焉而不辭生而不有為而不恃功成而弗居夫唯弗居是以不去第三章不尚賢使民不爭不貴難得之貨使民不為盜不見可欲使民心不亂是以聖人之治虛其心實其腹弱其志強其骨常使民無知無欲使夫智者不敢為也為無為則無不治"
        self.assertEqual(filter_hanzi_from_html(html), [x for x in trad])

    def test_mixed_content(self):
        """Test mixed Chinese and Latin characters in HTML"""
        text = '<h2><span class="mw-headline" id="Song_poetry">Song poetry</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Chinese_poetry&amp;action=edit&amp;section=8" title="Edit section: Song poetry"><span>edit</span></a><span class="mw-editsection-bracket">]</span></span></h2>\n<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096"><div role="note" class="hatnote navigation-not-searchable">Main article: <a href="/wiki/Song_poetry" title="Song poetry">Song poetry</a></div>\n<p>By the <a href="/wiki/Song_dynasty" title="Song dynasty">Song dynasty</a> (960–1279), another form had proven it could provide the flexibility that new poets needed: the <i><a href="/wiki/Ci_(poetry)" title="Ci (poetry)">ci</a></i> (词/詞) lyric—new lyrics written according to the set rhythms of existing tunes. Each of the tunes had music that has often been lost, but having its own meter. Thus, each <i>ci</i> poem is labeled "To the tune of [Tune Name]" (调寄[词牌]/調寄[詞牌]) and fits the meter and rhyme of the tune (much in the same way that Christian hymn writers set new lyrics to pre-existing tunes).'
        self.assertEqual(
            filter_hanzi_from_html(text),
            ["词", "詞", "调", "寄", "词", "牌", "調", "寄", "詞", "牌"],
        )

    def test_known_figures(self):
        """Test figures match for known quantities"""
        for test_case in TEST_CASES.keys():
            with open(
                os.path.join(TEST_ASSETS, test_case), "r", encoding=ENCODING
            ) as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi = filter_hanzi_from_html(text)
            # Test total character count
            self.assertEqual(len(hanzi), TEST_CASES[test_case][1])
            # Test unique character count
            self.assertEqual(len(set(hanzi)), TEST_CASES[test_case][2])


if __name__ == "__main__":
    unittest.main()

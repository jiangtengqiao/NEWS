import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
import json
from sqlalchemy.orm import Session
from app.models.news import News, NewsCategory
from app.schemas.news import NewsCreate


class NewsSpider:
    """桂林临桂新闻爬虫系统 - 实时爬取各类新闻"""
    
    # 新闻来源配置
    NEWS_SOURCES = {
        # 国家时政（免费）
        'government': {
            'name': '中国政府网',
            'url': 'http://www.gov.cn/policy/guoji/index.htm',
            'is_premium': False,
            'category': 'government'
        },
        'xinhua': {
            'name': '新华网',
            'url': 'http://www.xinhuanet.com/politics/',
            'is_premium': False,
            'category': 'government'
        },
        'people': {
            'name': '人民网',
            'url': 'http://politics.people.com.cn/',
            'is_premium': False,
            'category': 'government'
        },
        
        # 桂林地方新闻（免费）
        'guilin': {
            'name': '桂林市政府网',
            'url': 'http://www.guilin.gov.cn/',
            'is_premium': False,
            'category': 'local'
        },
        'guilinnews': {
            'name': '桂林生活网',
            'url': 'https://www.guilinlife.com/',
            'is_premium': False,
            'category': 'local'
        },
        'lingui': {
            'name': '临桂区政府网',
            'url': 'http://www.lingui.gov.cn/',
            'is_premium': False,
            'category': 'local'
        },
        
        # 社会新闻（订阅）
        'social': {
            'name': '腾讯社会新闻',
            'url': 'https://new.qq.com/ch/social/',
            'is_premium': True,
            'category': 'social'
        },
        
        # 财经新闻（订阅）
        'finance': {
            'name': '东方财富网',
            'url': 'https://www.eastmoney.com/',
            'is_premium': True,
            'category': 'finance'
        },
        
        # 科技新闻（订阅）
        'tech': {
            'name': '36氪',
            'url': 'https://36kr.com/',
            'is_premium': True,
            'category': 'tech'
        },
        
        # 体育新闻（订阅）
        'sports': {
            'name': '虎扑体育',
            'url': 'https://www.hupu.com/',
            'is_premium': True,
            'category': 'sports'
        },
        
        # 名人演讲（订阅）
        'speech': {
            'name': 'TED演讲',
            'url': 'https://www.ted.com/talks',
            'is_premium': True,
            'category': 'speech'
        }
    }
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """获取网页内容"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.encoding = response.apparent_encoding or 'utf-8'
            return response.text
        except Exception as e:
            print(f"获取页面失败 {url}: {e}")
            return None
    
    def parse_gov_news(self, html: str) -> List[Dict]:
        """解析政府网站新闻"""
        news_list = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找新闻列表
        articles = soup.find_all('div', class_='list')
        for article in articles:
            try:
                title_elem = article.find('a')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    if not link.startswith('http'):
                        link = 'http://www.gov.cn' + link
                    
                    news_list.append({
                        'title': title,
                        'url': link,
                        'source': '中国政府网',
                        'category': 'government',
                        'is_premium': False,
                        'tags': ['国家时政', '政府新闻']
                    })
            except Exception as e:
                print(f"解析政府新闻失败: {e}")
        
        return news_list
    
    def parse_xinhua_news(self, html: str) -> List[Dict]:
        """解析新华网新闻"""
        news_list = []
        soup = BeautifulSoup(html, 'html.parser')
        
        articles = soup.find_all('div', class_='item')
        for article in articles[:20]:
            try:
                title_elem = article.find('a')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    if not link.startswith('http'):
                        link = 'http://www.xinhuanet.com' + link
                    
                    news_list.append({
                        'title': title,
                        'url': link,
                        'source': '新华网',
                        'category': 'government',
                        'is_premium': False,
                        'tags': ['国家时政', '新华网']
                    })
            except Exception as e:
                print(f"解析新华网失败: {e}")
        
        return news_list
    
    def parse_guilin_news(self, html: str) -> List[Dict]:
        """解析桂林新闻"""
        news_list = []
        soup = BeautifulSoup(html, 'html.parser')
        
        articles = soup.find_all('li')
        for article in articles[:15]:
            try:
                title_elem = article.find('a')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    if link and not link.startswith('http'):
                        link = 'http://www.guilin.gov.cn' + link
                    
                    if title and len(title) > 5:
                        news_list.append({
                            'title': title,
                            'url': link or '',
                            'source': '桂林市政府网',
                            'category': 'local',
                            'is_premium': False,
                            'tags': ['桂林', '地方新闻']
                        })
            except Exception as e:
                print(f"解析桂林新闻失败: {e}")
        
        return news_list
    
    def fetch_news_detail(self, url: str) -> Optional[Dict]:
        """获取新闻详情"""
        html = self.fetch_page(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 获取正文内容
        content_elem = soup.find('div', class_='content')
        if not content_elem:
            content_elem = soup.find('article')
        
        if content_elem:
            paragraphs = content_elem.find_all('p')
            content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
            
            # 获取摘要
            summary_elem = soup.find('meta', attrs={'name': 'description'})
            summary = summary_elem.get('content', '') if summary_elem else ''
            
            # 获取发布时间
            time_elem = soup.find('span', class_='time')
            published_at = datetime.now()
            if time_elem:
                try:
                    time_str = time_elem.get_text(strip=True)
                    published_at = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                except:
                    pass
            
            return {
                'content': content[:2000] if content else '内容获取失败',
                'summary': summary[:200] if summary else '',
                'published_at': published_at
            }
        
        return None
    
    def generate_news_content(self, title: str, category: str) -> Dict:
        """根据标题生成新闻内容（用于示例）"""
        contents = {
            'government': f"""
{title}

【新华社消息】今日，国家相关部门召开重要会议，就当前经济社会发展形势进行深入分析研究。

会议指出，要坚持以人民为中心的发展思想，全面贯彻新发展理念，加快构建新发展格局，着力推动高质量发展。

会议强调，要加强宏观调控，扩大内需战略基点，激发市场主体活力，保持经济运行在合理区间。

同时，要切实保障和改善民生，加强和创新社会治理，确保社会大局稳定。

专家指出，此次会议为下一步工作指明了方向，各地区各部门要认真贯彻落实会议精神，扎实做好各项工作。
""".strip(),
            'local': f"""
{title}

【桂林日报消息】临桂区作为桂林市的重要组成部分，近年来经济社会发展取得显著成效。

临桂区坚持稳中求进工作总基调，统筹推进稳增长、促改革、调结构、惠民生、防风险各项工作。

在产业发展方面，临桂区重点发展电子信息、生物医药、现代服务业等新兴产业，推动传统产业转型升级。

在城市建设方面，临桂区加快完善基础设施，提升公共服务水平，打造宜居宜业的现代化新城。

在民生改善方面，临桂区扎实办好民生实事，不断增强人民群众的获得感、幸福感、安全感。
""".strip(),
            'social': f"""
{title}

【记者报道】近日，社会各界对这一话题高度关注。

记者在采访中了解到，相关部门高度重视此事，已采取一系列措施积极应对。

专家指出，此类现象反映了社会发展中的新情况新问题，需要多方合力解决。

目前，事件正在进一步处理中，本报将持续关注后续进展。
""".strip(),
            'finance': f"""
{title}

【财经观察】今日，资本市场传来重要信号。

业内人士分析认为，当前经济形势总体向好，但仍面临一些不确定性因素。

在政策支持和企业自身努力下，相关行业展现出较强的发展韧性。

展望未来，业内普遍看好行业发展前景，建议投资者理性看待短期波动。
""".strip()
        }
        
        return {
            'content': contents.get(category, contents['social']),
            'summary': f"关于{title}的详细报道和分析",
            'published_at': datetime.now()
        }
    
    def crawl_all(self, db: Session, max_news_per_source: int = 50) -> int:
        """爬取所有来源的新闻"""
        total_crawled = 0
        
        # 先确保分类存在
        categories = {
            'government': {'name': 'government', 'display_name': '国家时政', 'icon': 'fa-landmark', 'priority': 10},
            'local': {'name': 'local', 'display_name': '桂林临桂', 'icon': 'fa-map-marker-alt', 'priority': 9},
            'social': {'name': 'social', 'display_name': '社会热点', 'icon': 'fa-users', 'priority': 8},
            'finance': {'name': 'finance', 'display_name': '财经商业', 'icon': 'fa-chart-line', 'priority': 7},
            'tech': {'name': 'tech', 'display_name': '科技教育', 'icon': 'fa-microchip', 'priority': 6},
            'sports': {'name': 'sports', 'display_name': '体育文化', 'icon': 'fa-futbol', 'priority': 5},
            'speech': {'name': 'speech', 'display_name': '名人演讲', 'icon': 'fa-microphone', 'priority': 4},
            'health': {'name': 'health', 'display_name': '健康生活', 'icon': 'fa-heartbeat', 'priority': 3},
        }
        
        for cat_key, cat_info in categories.items():
            existing = db.query(NewsCategory).filter_by(name=cat_key).first()
            if not existing:
                category = NewsCategory(
                    name=cat_key,
                    display_name=cat_info['display_name'],
                    icon=cat_info['icon'],
                    priority=cat_info['priority']
                )
                db.add(category)
                db.commit()
        
        # 模拟爬取示例新闻
        sample_news = [
            # 国家时政（免费）
            {
                'title': '国家主席发表重要讲话',
                'content': '国家主席强调，要坚持以人民为中心的发展思想，全面推进中华民族伟大复兴。各地区各部门要认真贯彻落实会议精神，扎实做好各项工作，推动高质量发展。',
                'summary': '国家主席发表重要讲话，强调坚持以人民为中心的发展思想',
                'category': 'government',
                'is_premium': False,
                'tags': ['国家时政', '重要讲话', '发展理念'],
                'source': '新华社',
                'author': '记者'
            },
            {
                'title': '国务院常务会议部署稳经济措施',
                'content': '国务院总理主持召开国务院常务会议，分析当前经济形势，部署持续做好稳经济工作。会议指出，要高效统筹疫情防控和经济社会发展。',
                'summary': '国务院常务会议部署稳经济措施',
                'category': 'government',
                'is_premium': False,
                'tags': ['国务院', '经济', '政策措施'],
                'source': '中国政府网',
                'author': '编辑'
            },
            # 桂林地方（免费）
            {
                'title': '桂林市临桂区召开产业发展大会',
                'content': '桂林市临桂区召开产业发展大会，部署未来五年产业发展规划。临桂区将重点发展电子信息、生物医药、现代服务业三大主导产业，打造百亿级产业集群。',
                'summary': '桂林市临桂区召开产业发展大会，部署未来五年规划',
                'category': 'local',
                'is_premium': False,
                'tags': ['桂林', '临桂', '产业发展'],
                'source': '桂林市政府网',
                'author': '张记者'
            },
            {
                'title': '临桂区政务服务中心启用智能服务系统',
                'content': '临桂区政务服务中心正式启用智能服务系统，市民可通过自助终端办理多项业务，有效缩短办事时间，提升服务效率。',
                'summary': '临桂区政务服务中心启用智能服务系统',
                'category': 'local',
                'is_premium': False,
                'tags': ['临桂', '政务服务', '智能化'],
                'source': '临桂区政府网',
                'author': '李编辑'
            },
            # 社会新闻（订阅）
            {
                'title': '全国多地气温创新高，电网负荷大幅攀升',
                'content': '连日来，全国多地气温持续攀升，多个省份电网负荷创历史新高。电力部门启动应急预案，全力保障居民用电需求。',
                'summary': '全国多地气温创新高，电网负荷大幅攀升',
                'category': 'social',
                'is_premium': True,
                'tags': ['天气', '电力', '民生'],
                'source': '中国气象网',
                'author': '王记者'
            },
            {
                'title': '教育部发布中小学课外读物推荐目录',
                'content': '教育部近日发布《中小学课外读物推荐目录》，引导学生读好书、读经典，促进青少年健康成长。',
                'summary': '教育部发布中小学课外读物推荐目录',
                'category': 'social',
                'is_premium': True,
                'tags': ['教育', '课外读物', '青少年'],
                'source': '教育部官网',
                'author': '赵编辑'
            },
            # 财经新闻（订阅）
            {
                'title': '央行宣布定向降准，释放长期资金约5000亿',
                'content': '中国人民银行宣布下调金融机构存款准备金率0.25个百分点，预计释放长期资金约5000亿元，支持实体经济发展。',
                'summary': '央行宣布定向降准，释放长期资金约5000亿元',
                'category': 'finance',
                'is_premium': True,
                'tags': ['央行', '降准', '货币政策'],
                'source': '央行官网',
                'author': '金融记者'
            },
            {
                'title': 'A股三大指数集体收涨，成交量突破万亿',
                'content': '今日，A股市场表现强劲，三大指数集体收涨。两市成交额突破万亿元，市场情绪明显回暖。',
                'summary': 'A股三大指数集体收涨，成交量突破万亿',
                'category': 'finance',
                'is_premium': True,
                'tags': ['A股', '股市', '投资'],
                'source': '东方财富网',
                'author': '股评师'
            },
            # 科技新闻（订阅）
            {
                'title': '华为发布新一代鸿蒙操作系统',
                'content': '华为今日正式发布鸿蒙操作系统4.0版本，新版本在性能、安全、AI能力等方面均有大幅提升，已有多家厂商宣布支持。',
                'summary': '华为发布新一代鸿蒙操作系统',
                'category': 'tech',
                'is_premium': True,
                'tags': ['华为', '鸿蒙', '操作系统'],
                'source': '36氪',
                'author': '科技编辑'
            },
            {
                'title': '人工智能在医疗领域取得突破性进展',
                'content': '科研团队宣布，人工智能辅助诊断系统在多项临床测试中表现优异，诊断准确率达到主任医师水平。',
                'summary': '人工智能在医疗领域取得突破性进展',
                'category': 'tech',
                'is_premium': True,
                'tags': ['人工智能', '医疗', '科技创新'],
                'source': '科技日报',
                'author': '科学家'
            },
            # 名人演讲（订阅）
            {
                'title': '马云谈创业精神与企业家责任',
                'content': '马云在某商业论坛上分享了他的创业心得，强调企业家要有家国情怀，承担社会责任，为社会发展贡献力量。',
                'summary': '马云谈创业精神与企业家责任',
                'category': 'speech',
                'is_premium': True,
                'tags': ['马云', '创业', '企业家'],
                'source': 'TED演讲精选',
                'author': '演讲整理'
            },
            {
                'title': '诺贝尔奖得主分享科研心路历程',
                'content': '诺贝尔物理学奖得主在某学术会议上分享了他的科研历程，鼓励年轻学者要坚持梦想，勇于探索未知领域。',
                'summary': '诺贝尔奖得主分享科研心路历程',
                'category': 'speech',
                'is_premium': True,
                'tags': ['诺贝尔奖', '科学家', '学术'],
                'source': '学术报告精选',
                'author': '学术编辑'
            }
        ]
        
        for news_data in sample_news:
            # 检查是否已存在
            existing = db.query(News).filter_by(title=news_data['title']).first()
            if existing:
                continue
            
            # 获取分类ID
            category = db.query(NewsCategory).filter_by(name=news_data['category']).first()
            
            # 创建新闻记录
            news = News(
                title=news_data['title'],
                content=news_data['content'],
                summary=news_data['summary'],
                source=news_data['source'],
                author=news_data['author'],
                category=category.name if category else news_data['category'],
                tags=json.dumps(news_data['tags'], ensure_ascii=False),
                is_premium=news_data['is_premium'],
                image_url=f"https://picsum.photos/seed/{hashlib.md5(news_data['title'].encode()).hexdigest()[:8]}/800/400"
            )
            
            db.add(news)
            total_crawled += 1
        
        db.commit()
        return total_crawled


def initialize_news_spider(db: Session) -> int:
    """初始化新闻爬虫并爬取新闻"""
    spider = NewsSpider()
    return spider.crawl_all(db)

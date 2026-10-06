# -*- coding: utf-8 -*-
"""从 docs/ 中已生成的 HTML 反向提取 Hugo 源文件(content/*.md)。

策略:
- 每个含 single-title 的 docs/<name>/index.html 视为一篇文章(about 单独处理为根级页面)
- og: meta 提取 title/date/lastmod; 文章页链接提取 categories/tags
- <div class="content"> 内部:
    * chroma 代码块(lntable 带行号) -> 还原 ```lang 围栏代码
    * lazyload 图片(data-src) -> 还原 ![]() 真实地址
    * admonition/details 短代码 -> 还原 {{< admonition ... >}}
    * bilibili iframe -> 还原 {{< bilibili ... >}}
    * 其余 HTML 交给 pandoc 转 gfm
"""
import glob
import json
import os
import re
import shutil
from urllib.parse import unquote

from bs4 import BeautifulSoup
import pypandoc

DOCS = 'docs'
OUT_POSTS = os.path.join('content', 'posts')
OUT_ROOT = 'content'

# zh-CN 下 admonition 的默认标题(T $type 的取值),用于判断是否省略 title 参数
ADMONITION_I18N = {
    'note': '注意', 'abstract': '摘要', 'info': '信息', 'tip': '小贴士',
    'success': '成功', 'question': '问题', 'warning': '警告', 'failure': '失败',
    'danger': '危险', 'bug': 'Bug', 'example': '示例', 'quote': '引用',
}


def decode_path(href):
    """/categories/%E7%B3%BB%E7%BB%9F/ -> 系统优化"""
    if not href:
        return ''
    return unquote(href.strip().strip('/').split('/')[-1])


def code_block_token(counter):
    return 'ZCODEBLOCKZTOKEN%dZEND' % counter


def replace_code_blocks(soup):
    """把 highlight 代码块替换成占位符,返回 {token: fenced_markdown}"""
    blocks = {}
    n = 0
    for div in soup.select('div.highlight'):
        lang = ''
        code_text = ''
        # 结构A: lntable(带行号列) —— 取第二个 td 的 code
        tds = div.select('table.lntable td.lntd')
        if len(tds) >= 2:
            code = tds[1].select_one('code')
            if code:
                lang = code.get('data-lang', '') or ''
                cls = code.get('class', []) or []
                for c in cls:
                    if c.startswith('language-'):
                        lang = c[len('language-'):]
                code_text = code.get_text()
        else:
            code = div.select_one('pre code') or div.select_one('code')
            if code:
                lang = code.get('data-lang', '') or ''
                for c in (code.get('class', []) or []):
                    if c.startswith('language-'):
                        lang = c[len('language-'):]
                code_text = code.get_text()
        if code is None:
            continue
        code_text = code_text.rstrip('\n')
        token = code_block_token(n)
        fence = '```' + lang + '\n' + code_text + '\n```'
        blocks[token] = fence
        n += 1
        p = soup.new_tag('p')
        p.string = token
        div.replace_with(p)
    return blocks


def fix_images(soup):
    """lazyload 图片: 用 data-src 覆盖 src, 主题自动生成的 title/alt 一并去掉。"""
    for img in soup.find_all('img'):
        real = img.get('data-src') or img.get('src')
        if not real:
            img.decompose()
            continue
        src = img.get('src', '')
        alt = img.get('alt', '')
        title = img.get('title', '')
        # alt/title 是主题自动补的(alt=title=src) -> 去掉
        if title and title in (alt, src, real):
            del img['title']
        if alt and alt in (src, real):
            del img['alt']
        img['src'] = real
        for k in ('data-src', 'data-srcset', 'data-sizes', 'srcset', 'sizes'):
            if img.has_attr(k):
                del img[k]
        cls = [c for c in (img.get('class') or []) if c not in ('lazyload', 'logo')]
        extra = ' '.join(cls)
        token = 'ZIMGTOKEN%dZEND' % fix_images.n
        fix_images.n += 1
        if not extra and not img.get('style'):
            fix_images.tokens[token] = '![%s](%s)' % (img.get('alt', ''), real)
        else:
            # 带额外 class/style, 保留 raw HTML
            keep = ['class', 'alt', 'title', 'style', 'width', 'height']
            attrs = ' '.join('%s="%s"' % (k, img.get(k)) for k in keep if img.get(k))
            fix_images.tokens[token] = '<img %s src="%s" />' % (attrs, real)
        img.replace_with(soup.new_string(token))


fix_images.n = 0
fix_images.tokens = {}


def replace_admonitions(soup):
    """admonition / details 短代码 -> 占位符。返回 {token: shortcode_markdown}"""
    out = {}
    n = 0
    # admonition(含 details 样式): div.admonition
    for div in soup.select('div.admonition'):
        classes = div.get('class', []) or []
        types = [c for c in classes if c in ADMONITION_I18N]
        atype = types[0] if types else 'note'
        is_details = 'details' in classes
        open_flag = 'open' in classes
        title_el = div.select_one('.details-summary.admonition-title, .admonition-title')
        title = ''
        if title_el:
            title = re.sub(r'\s+', ' ', title_el.get_text(strip=True))
        content_el = div.select_one('.admonition-content') or div
        inner_html = content_el.decode_contents() if content_el is not div else div.decode_contents()
        inner_md = pypandoc.convert_text(inner_html, 'gfm', format='html',
                                         extra_args=['--wrap=none']).replace('\r\n', '\n').strip()
        # 重组短代码。positional 参数依次为 type title open,
        # 标题等于默认值时用空串占位,避免 open 错位成标题
        parts = ['admonition', atype]
        if title and title != ADMONITION_I18N.get(atype):
            parts.append('"%s"' % title.replace('"', '\\"'))
        if open_flag:
            if len(parts) < 3:
                parts.append('""')
            parts.append('true')
        token = 'ZADMTOKEN%dZEND' % n
        out[token] = '{{< %s >}}\n%s\n{{< /admonition >}}' % (' '.join(parts), inner_md)
        n += 1
        p = soup.new_tag('p')
        p.string = token
        div.replace_with(p)
    # 纯 details 短代码(无 admonition 类)
    for div in soup.select('div.details'):
        classes = div.get('class', []) or []
        if 'admonition' in classes or 'toc' in classes:
            continue
        open_flag = 'open' in classes
        title_el = div.select_one('.details-summary')
        title = re.sub(r'\s+', ' ', title_el.get_text(strip=True)) if title_el else ''
        content_el = div.select_one('.details-content')
        inner_md = pypandoc.convert_text(content_el.decode_contents(), 'gfm', format='html',
                                         extra_args=['--wrap=none']).replace('\r\n', '\n').strip() if content_el else ''
        token = 'ZDETAILSTOKEN%dZEND' % n
        out[token] = '{{< details "%s"%s >}}\n%s\n{{< /details >}}' % (
            title.replace('"', '\\"'), ' true' if open_flag else '', inner_md)
        n += 1
        p = soup.new_tag('p')
        p.string = token
        div.replace_with(p)
    return out


def replace_bilibili(soup):
    """bilibili iframe -> 占位符。返回 {token: shortcode}"""
    out = {}
    n = 0
    for div in soup.select('div.bilibili'):
        iframe = div.find('iframe')
        src = iframe.get('src', '') if iframe else ''
        bvid = ''
        page = '1'
        m = re.search(r'[?&]bvid=([^&]+)', src)
        if m:
            bvid = m.group(1)
        m = re.search(r'[?&]page=([^&]+)', src)
        if m:
            page = m.group(1)
        m = re.search(r'[?&]aid=([^&]+)', src)
        if m and not bvid:
            bvid = 'aid=' + m.group(1)
        token = 'ZBILITOKEN%dZEND' % n
        out[token] = '{{< bilibili %s%s >}}' % (bvid, '' if page == '1' else ' ' + page)
        n += 1
        p = soup.new_tag('p')
        p.string = token
        div.replace_with(p)
    return out


def simplify_links(soup):
    """LoveIt 的 render-link 钩子会给外链自动加 rel/target,
    还原为纯 markdown 链接(占位符后替换,避免 pandoc 转义 markdown 符号)。"""
    for a in soup.find_all('a'):
        href = a.get('href')
        if not href or not (a.get('rel') or a.get('target')):
            continue
        rel = ' '.join(a.get('rel', []) or [])
        if rel != 'noopener noreffer' or a.get('target') != '_blank':
            continue
        if a.find('img') or a.get('class') or a.get('id'):
            continue
        title = a.get('title', '')
        token = 'ZLINKTOKEN%dZEND' % simplify_links.n
        simplify_links.n += 1
        inner_md = pypandoc.convert_text(a.decode_contents(), 'gfm', format='html',
                                         extra_args=['--wrap=none']).replace('\r\n', '\n').strip()
        inner_md = re.sub(r'^<p>|</p>$', '', inner_md).strip()
        if title:
            simplify_links.tokens[token] = '[%s](%s "%s")' % (inner_md, href, title.replace('"', '\\"'))
        else:
            simplify_links.tokens[token] = '[%s](%s)' % (inner_md, href)
        a.replace_with(soup.new_string(token))


simplify_links.n = 0
simplify_links.tokens = {}


def replace_token_block(md, token, block):
    """把占位符替换回块内容; 若占位符独立成行(通常在列表里被 pandoc 缩进),
    则整块继承该缩进, 避免破坏列表结构。"""
    pattern = re.compile(r'^([ \t]*)' + re.escape(token) + r'[ \t]*$', re.M)

    def repl(m):
        indent = m.group(1)
        if not indent:
            return block
        return '\n'.join(indent + line if line else line for line in block.split('\n'))

    md2, n = pattern.subn(repl, md)
    if n == 0:
        md2 = md.replace(token, block)
    return md2


def html_to_md(inner_html):
    """div.content 内部 HTML -> markdown(先保护代码块/短代码/图片/链接)"""
    soup = BeautifulSoup(inner_html, 'lxml')
    blocks = {}
    blocks.update(replace_code_blocks(soup))
    blocks.update(replace_admonitions(soup))
    blocks.update(replace_bilibili(soup))
    fix_images(soup)
    simplify_links(soup)
    body = soup.decode_contents()
    md = pypandoc.convert_text(body, 'gfm', format='html', extra_args=['--wrap=none'])
    md = md.replace('\r\n', '\n')
    all_tokens = {}
    all_tokens.update(blocks)
    all_tokens.update(fix_images.tokens)
    all_tokens.update(simplify_links.tokens)
    fix_images.tokens.clear()
    simplify_links.tokens.clear()
    for token, fence in all_tokens.items():
        md = replace_token_block(md, token, fence)
    # pandoc 可能把占位符里的 _ 转义成 \_,规范化后再替换一次
    md = re.sub(r'@@(CODEBLOCK|ADM|DET|BILI|IMG|LINK)_\\?(\d+)@@', r'@@\1_\2@@', md)
    for token, fence in all_tokens.items():
        if token in md:
            md = replace_token_block(md, token, fence)
    # 清理多余空行
    md = re.sub(r'\n{3,}', '\n\n', md).strip()
    return md


def extract_single(path):
    html = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(html, 'lxml')

    title = ''
    m = re.search(r'<meta property="og:title" content="([^"]*)"', html)
    if m:
        title = m.group(1)
    date = re.search(r'<meta property="article:published_time" content="([^"]*)"', html)
    lastmod = re.search(r'<meta property="article:modified_time" content="([^"]*)"', html)
    date = date.group(1) if date else ''
    lastmod = lastmod.group(1) if lastmod else ''

    art = soup.select_one('article.page') or soup
    categories = [decode_path(a.get('href')) for a in art.select('.post-category a')]
    tags = [decode_path(a.get('href')) for a in art.select('.post-tags a')]

    content_div = soup.select_one('div.content#content') or soup.select_one('div#content')
    if content_div is None:
        return None
    md = html_to_md(content_div.decode_contents())

    fm = []
    fm.append('title: %s' % json.dumps(title, ensure_ascii=False))
    if date:
        fm.append('date: %s' % date)
    if lastmod and lastmod != date:
        fm.append('lastmod: %s' % lastmod)
    fm.append('draft: false')
    if categories:
        fm.append('categories: [%s]' % ', '.join(json.dumps(c, ensure_ascii=False) for c in categories))
    if tags:
        fm.append('tags: [%s]' % ', '.join(json.dumps(t, ensure_ascii=False) for t in tags))
    front = '---\n' + '\n'.join(fm) + '\n---\n\n'
    return front + md + '\n'


def main():
    if os.path.exists('content'):
        shutil.rmtree('content')
    os.makedirs(OUT_POSTS, exist_ok=True)

    manifest = []
    skipped = []
    for path in sorted(glob.glob(os.path.join(DOCS, '*', 'index.html'))):
        name = os.path.basename(os.path.dirname(path))
        if name in ('posts', 'categories', 'tags', 'page', 'about', 'svg', 'css', 'js', 'lib'):
            continue
        html = open(path, encoding='utf-8').read()
        if 'single-title' not in html:
            continue
        md = extract_single(path)
        if md is None:
            skipped.append(name)
            continue
        fname = os.path.join(OUT_POSTS, name + '.md')
        with open(fname, 'w', encoding='utf-8', newline='\n') as f:
            f.write(md)
        manifest.append({'dir': name, 'file': fname})

    # about 页(根级页面)
    about = os.path.join(DOCS, 'about', 'index.html')
    if os.path.exists(about):
        md = extract_single(about)
        if md:
            with open(os.path.join(OUT_ROOT, 'about.md'), 'w', encoding='utf-8', newline='\n') as f:
                f.write(md)
            manifest.append({'dir': 'about', 'file': 'content/about.md'})

    # posts section 标题
    with open(os.path.join(OUT_POSTS, '_index.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('---\ntitle: 所有文章\ndraft: false\n---\n')

    with open('scripts/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print('extracted posts:', len(manifest))
    if skipped:
        print('skipped(no content):', skipped)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""把 content/ 中失效的外链图片(sinaimg 防盗链 / localhost)替换为本地占位图。
原图地址保留在 HTML 注释中,便于将来找回原图后一键还原。"""
import glob
import re

PLACEHOLDER = '/images/broken-image.svg'
# 新浪图床(全部 403)与本地开发遗留地址
DEAD = r'(https?://[^)\s"\']*(?:sinaimg\.cn|127\.0\.0\.1|localhost)[^)\s"\']*)'


def replace_markdown_images(md):
    def md_sub(m):
        alt, url = m.group(1), m.group(2)
        return ('<!-- 原图(已失效): %s -->\n' % url) + ('![%s](%s)' % (alt or '图片失效', PLACEHOLDER))

    md, n1 = re.subn(r'!\[([^\]]*)\]\(%s\)' % DEAD, md_sub, md)

    def html_sub(m):
        url = m.group(1)
        return ('<!-- 原图(已失效): %s -->\n' % url) + ('<img src="%s" alt="图片失效" />' % PLACEHOLDER)

    md, n2 = re.subn(r'<img[^>]*src="%s"[^>]*/?>' % DEAD, html_sub, md)
    return md, n1 + n2


def main():
    total = 0
    files = 0
    for f in glob.glob('content/**/*.md', recursive=True):
        md = open(f, encoding='utf-8').read()
        new, n = replace_markdown_images(md)
        if n:
            with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(new)
            total += n
            files += 1
    print('替换失效图片: %d 张, 涉及 %d 个文件' % (total, files))


if __name__ == '__main__':
    main()

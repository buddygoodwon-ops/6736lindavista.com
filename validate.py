from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.err = []

    def handle_starttag(self, t, a):
        if t not in ('img', 'br', 'hr', 'meta', 'link', 'input', 'iframe'):
            self.stack.append(t)

    def handle_endtag(self, t):
        if self.stack and self.stack[-1] == t:
            self.stack.pop()
        elif t in self.stack:
            while self.stack and self.stack[-1] != t:
                self.err.append('unclosed:' + self.stack.pop())
            self.stack.pop()
        else:
            self.err.append('stray:/' + t)


p = P()
p.feed(open('index.html', encoding='utf-8').read())
p.close()
print('unclosed:', p.stack if p.stack else 'NONE')
print('errors:', p.err[:10] if p.err else 'NONE')
import re,base64
fd='/home/claude/render/fonts'
def f64(n): return base64.b64encode(open(f'{fd}/{n}','rb').read()).decode()
rng={'cyrillic':'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116','latin':'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD,U+20BD'}
faces=''
for fam,fn,w in (('Unbounded','unbounded-%s-900-normal.woff2','800 900'),('Onest','onest-%s-400-normal.woff2','400 500'),('Onest','onest-%s-700-normal.woff2','700')):
    for sub in ('cyrillic','latin'):
        faces+=f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{f64(fn%sub)}) format('woff2');unicode-range:{rng[sub]}}}"
h=open('/home/claude/site2/index.html').read()
h=re.sub(r'<link rel="preconnect"[^>]*>','',h)
h=re.sub(r'<link href="https://fonts.googleapis[^>]*>','<style>'+faces+'</style>',h)
open('/home/claude/site2/dropdealer-presentation.html','w').write(h)

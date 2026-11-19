import re,base64,io
from PIL import Image
def b64png(path,maxw):
    im=Image.open(path).convert('RGBA')
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    bb=io.BytesIO();im.save(bb,'PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(bb.getvalue()).decode()
svg=open('/home/claude/maptool/map.svg').read()
paths=re.findall(r'<path d="([^"]*)"',svg);NEI,RUS=paths[0],paths[1]
css=open('css.txt').read()
css=re.sub(r'(?<![\w#.\-])(-?\d*\.?\d+)u(?![\w\-])',lambda m:f'calc(var(--u)*{m.group(1)})',css)
js=open('js.txt').read()
def b64(n): return 'data:image/jpeg;base64,'+base64.b64encode(open(f'/home/claude/assets/logo-{n}.jpg','rb').read()).decode()
ICONS={'shield':'<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/>','bolt':'<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>','chart':'<path d="M4 20V11M10 20V4M16 20v-7M22 20H2"/>','clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>','lock':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>','users':'<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 3-5.5 6-5.5s6 2 6 5.5M15 15c3-.3 6 1 6 4"/>','sliders':'<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>','globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3.5 3 3.5 15 0 18M12 3c-3.5 3-3.5 15 0 18"/>','headset':'<path d="M4 14v-2a8 8 0 0116 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>'}
def ic(n): return f'<div class="ico"><svg viewBox="0 0 24 24">{ICONS[n]}</svg></div>'
def H(lines,base=.1,step=.09,tag='h2',cls=''):
    out=[];i=0
    for line in lines:
        ws=[]
        for w in line:
            t,c=(w if isinstance(w,tuple) else (w,''))
            ws.append(f'<span class="w"><span style="--d:{base+i*step:.2f}s"{(" class=%s"%c) if c else ""}>{t}</span></span>');i+=1
        out.append(' '.join(ws))
    return f'<{tag} class="h {cls}">'+'<br>'.join(out)+f'</{tag}>'
ICO={'ПРИЛОЖЕНИЕ':b64png('/home/claude/icon_dropdealer.png',120),'MAX':b64png('/home/claude/icon_max.png',120),'TELEGRAM':b64png('/home/claude/icon_telegram.png',120)}
LINKS={'ПРИЛОЖЕНИЕ':'https://app.dropdealer.ru','MAX':'https://max.ru/join/2rA2kvRL6sa1yu-Qorso-G_hOcH6ofVObEl90T9q0vI','TELEGRAM':'https://t.me/dropdealerofficial'}
BTN={'ПРИЛОЖЕНИЕ':'ПЕРЕЙТИ В ПРИЛОЖЕНИЕ','MAX':'ПЕРЕЙТИ В MAX','TELEGRAM':'ПЕРЕЙТИ В TG'}
def phone(name,c,pd):
    return f'<a class="phone {c}" href="{LINKS[name]}" target="_blank" rel="noopener" aria-label="Открыть: {name}" style="--pd:{pd}s"><div class="ph-in"><div class="ph-top"><span class="pn">{name}</span><i class="live"><s></s>LIVE</i></div><div class="ph-img"><img src="{ICO[name]}" alt=""></div><div class="ph-ln"></div><div class="ph-ln s"></div><div class="ph-btn">{BTN[name]}</div></div></a>'
def pt(x,y): return f'left:{x/1040*100:.2f}%;top:{y/700*100:.2f}%'
def cd(i,t,s): return f'<div class="card cd rv" style="--d:{.5+i*.12:.2f}s">{ic(["sliders","globe","chart","users"][i] if False else i)}<div><h4>{t}</h4><p>{s}</p></div></div>'
def card4(icon,t,s,d): return f'<div class="card cd rv" style="--d:{d:.2f}s">{ic(icon)}<div><h4>{t}</h4><p>{s}</p></div></div>'
def bc(icon,t,s,d): return f'<div class="bc"><div style="--d:{d:.2f}s">{ic(icon)}<div><h4>{t}</h4><p>{s}</p></div></div></div>'
def chip(icon,t,s,d): return f'<div class="chip rv" style="--d:{d:.2f}s">{ic(icon)}<div><b>{t}</b><span>{s}</span></div></div>'
names=[('avtoportret','Автопортрет'),('avtostil','Автостиль'),('avangard','Авангард'),('piter-lada','Питер-Лада'),('avtomir','Автомир'),('avtoprodiks','Автопродикс')]
logos=''.join(f'<div class="lg" style="--d:{.4+i*.12:.2f}s;--fx:{"-8%" if i%2==0 else "8%"}"><img src="{b64png("/home/claude/logos/"+n+".png",760)}" alt="{t}"></div>' for i,(n,t) in enumerate(names))
tar=[('До 25 сделок','80 000 ₽',32),('26–50 сделок','130 000 ₽',52),('51–70 сделок','150 000 ₽',60),('71–100 сделок','200 000 ₽',80),('Более 100 сделок','250 000 ₽',100)]
lad=''.join(f'<div class="lr{" top" if p==100 else ""}" style="--d:{.5+i*.13:.2f}s;--p:{p}%"><i></i><div><span>{a}{'<small class="pb">окупается с 1 сделки</small>' if i==0 else ''}</span><b>{b}</b></div></div>' for i,(a,b,p) in enumerate(tar))

import json,subprocess,datetime
try:
    raw=subprocess.run(['curl','-sS','--retry','4','--retry-all-errors','https://dropdealer.ru/api/lots?limit=100&status=active'],capture_output=True,text=True,timeout=90).stdout
    its=json.loads(raw); its=its.get('items',its)
    now=datetime.datetime.utcnow().isoformat()
    LOTS=sorted([{'t':x['title'],'c':x.get('city') or '','p':x.get('currentPrice') or x.get('startPrice'),'e':x['auctionEnd']} for x in its if x.get('auctionEnd') and x['auctionEnd']>now],key=lambda z:z['e'])[:14]
    json.dump(LOTS,open('lots_snapshot.json','w'),ensure_ascii=False)
except Exception as ex:
    print('lots fetch failed',ex);LOTS=json.load(open('lots_snapshot.json'))
print('lots',len(LOTS))
LOTS_JS='<script>window.LOTS0='+json.dumps(LOTS,ensure_ascii=False)+'</script>'
BORIS='data:image/jpeg;base64,'+base64.b64encode(open('boris_av.jpg','rb').read()).decode()
S=[]
S.append(f'''<section class="sl" id="s1"><div class="in">
<div class="eyebrow rv"><i class="live"><s></s>ТОРГИ ИДУТ</i> · <span id="eb1">автоаукцион для дилеров</span></div>
<h1 class="h h1"><span class="w bk"><span style="--d:.15s">Один</span></span> <span class="w"><span style="--d:.24s">аукцион.</span></span><br><span class="w"><span style="--d:.33s">Три</span></span> <span class="w"><span style="--d:.42s">экрана.</span></span></h1>
<p class="sub rv" style="--d:.7s">Приложение, MAX и Telegram. Одни торги, одна цена, одни ставки — в любом месте, где удобно дилеру.</p>
<div class="phones"><div class="tapnote rv" style="--d:1.1s"><svg viewBox="0 0 24 24"><path d="M12 4v14M6 12l6 6 6-6"/></svg>Кликабельно — нажми на кнопку</div>{phone("ПРИЛОЖЕНИЕ","l",.7)}{phone("MAX","mm",.9)}{phone("TELEGRAM","r",1.1)}</div>
</div><div class="tick" id="tick"><div class="tl"><s></s>LIVE</div><div class="tkw"><div class="tt" id="tt"></div></div></div>
<div class="hint">ЛИСТАЙ</div></section>''')
S.append(f'''<section class="sl" id="s2"><div class="in">
<div class="eyebrow rv"><i class="live"><s></s>ПРИМЕР ИЗ ПРАКТИКИ</i></div>
{H([["Больше","участников"],["— выше","цена."]],.1)}
<div class="cmpw"><div class="cmp">
<div class="row a rv" style="--d:.4s"><div class="rh"><div class="who">20–100 участников<span class="tag">ваш аукцион</span><small>каждая точка — один покупатель</small></div><div class="price">850 000 ₽</div></div><div class="fieldw"><canvas id="cA" class="field"></canvas></div></div>
<div class="row b rv" style="--d:.9s"><div class="rh"><div class="who">1 600 участников<small>на DROPDEALER</small></div><div class="price" id="pB">900 000 ₽</div></div><div class="fieldw"><canvas id="cB" class="field"></canvas></div><div class="stamp">Продано</div></div>
</div><div class="badge">+50 000 ₽</div></div>
<div class="bidrow rv" style="--d:1.3s"><button class="bidbtn" id="bid" type="button">Сделать ставку · +10 000 ₽</button></div>
<p class="note rv" style="--d:1.2s">На внутренних аукционах дилеров обычно 20–100 участников, и это в лучшем случае. Чем больше покупателей видят лот, тем выше уходит цена.</p>
</div></section>''')
S.append(f'''<section class="sl" id="sc"><div class="in">
<div class="eyebrow rv">Калькулятор выгоды</div>
{H([["Посчитайте"],["свою","выгоду."]],.1)}
<div class="calc rv" style="--d:.4s">
<div class="ctl">
<div class="fld"><label>Цена автомобиля<b id="vP">850 000 ₽</b></label><input id="rgP" type="range" min="300000" max="3000000" step="50000" value="850000" aria-label="Цена автомобиля"></div>
<div class="fld"><label>Машин в месяц<b id="vC">10</b></label><input id="rgC" type="range" min="1" max="30" step="1" value="10" aria-label="Машин в месяц"></div>
</div>
<div class="cres"><small>Дополнительно в месяц</small><div class="big" id="rM">+500 000 ₽</div><div class="yr" id="rY">≈ 6 000 000 ₽ в год</div><div class="per" id="rPer">+50 000 ₽ с одной машины</div></div>
</div>
<p class="calcnote rv" style="--d:.7s">Реальный результат зависит от автомобиля и числа участников торгов.</p>
</div></section>''')
S.append(f'''<section class="sl" id="s3"><div class="in two">
<div><div class="eyebrow rv">Результаты платформы за 9 месяцев</div>
{H([["Это","уже"],["работает."]],.1)}
<div class="ringrow rv" style="--d:.4s"><div class="ring"><svg viewBox="0 0 120 120"><circle class="tr" cx="60" cy="60" r="50"/><circle class="fg" cx="60" cy="60" r="50" pathLength="314"/></svg><b data-to="65" data-suf="%">0%</b></div><div class="ringtx">лотов продано<small>доля лотов, ушедших с торгов</small></div></div>
<div class="tiles">
<div class="tile" style="--td:.5s"><div class="n" data-to="2688">0</div><p>зарегистрированных покупателей</p></div>
<div class="tile" style="--td:.65s"><div class="n" data-to="1652">0</div><p>активных покупателей · ≈61% от зарегистрированных</p></div>
<div class="tile y" style="--td:.8s"><div class="n" data-to="2850" data-suf="+">0</div><p>проведённых аукционов</p></div>
<div class="tile k" style="--td:.95s"><div class="n" data-to="17">0</div><p>дилерских центров в 7 городах</p></div>
</div></div>
<div class="mapw"><svg viewBox="0 0 1040 700" aria-label="Карта: города, где работают дилерские центры DROPDEALER">
<path d="{NEI}" fill="#F7F7F3" stroke="#E6E6DE" stroke-width="1.5" stroke-linejoin="round"/>
<path d="{RUS}" fill="#ECEDE6" stroke="#C4C6BC" stroke-width="2" stroke-linejoin="round"/>
<path class="rtp" pathLength="1" d="M225,276L229,323L318,413L317,430L527,515L540,524L796,362"/></svg>
<div class="city L" style="{pt(225,276)};--cd:.9s"><u></u><i></i><em>Санкт-Петербург</em></div>
<div class="city L" style="{pt(229,323)};--cd:1.2s"><u></u><i></i><em>Великий Новгород</em></div>
<div class="city L" style="{pt(317,422)};--cd:1.7s"><u></u><i></i><em>Москва · Яхрома</em></div>
<div class="city D" style="{pt(533,520)};--cd:2.6s"><u></u><i></i><em>Самара · Тольятти</em></div>
<div class="city T" style="{pt(796,362)};--cd:3.3s"><u></u><i></i><em>Тюмень</em></div>
<div class="mapcap"><b class="u">17</b><span>ДИЛЕРСКИХ ЦЕНТРОВ · 7 ГОРОДОВ</span></div></div>
</div></section>''')
S.append(f'''<section class="sl" id="s4"><div class="in">
<div class="eyebrow rv">Подключение и управление</div>
{H([["Простое","подключение."],[("Максимальный","g"),("контроль.","g")]],.1)}
<div class="conn"><div class="cards">
{card4('sliders','Вы полностью управляете лотом','Длительность аукциона, шаг ставки и другие параметры',.5)}
{card4('globe','Торги всегда под рукой','Веб-приложение, Telegram и MAX',.62)}
{card4('chart','Полный контроль','Участники, ставки, история торгов',.74)}
{card4('users','Всю организацию берём на себя','Подключение, обучение, сопровождение и поддержка 24/7',.86)}
</div>
<div class="card y tcard rv" style="--d:.7s"><div class="lab">ПОДКЛЮЧЕНИЕ ЗА</div><div class="clock"><svg viewBox="0 0 120 120"><circle class="tr" cx="60" cy="60" r="50"/><circle class="fg" cx="60" cy="60" r="50" pathLength="314"/></svg><b><span data-to="30">0</span><small>МИНУТ</small></b></div><div class="and">и вы уже на торгах</div></div>
</div>
<div class="chips">{chip('users','Больше покупателей','без изменения ваших процессов',1.0)}{chip('shield','Надёжная работа','стабильная платформа',1.1)}{chip('headset','Поддержка 24/7','на всех этапах',1.2)}</div>
</div></section>''')
S.append(f'''<section class="sl" id="s5"><div class="in">
<div class="eyebrow rv">Выгода для дилера</div>
{H([["Зарабатывайте","больше","на"],["продаже","перекупам",("уже","g"),("сейчас","g")]],.1,.07)}
<div class="bgrid">
{bc('shield','Проверенный инструмент','Уже работает в 17 дилерских центрах',.4)}
{bc('bolt','Выгодные сделки каждый день','Торги идут ежедневно, сделки закрываются каждый день',.52)}
{bc('chart','Дополнительная прибыль','Автомобили продаются дороже, чем на внутреннем аукционе дилера',.64)}
{bc('clock','Экономия времени и затрат','Быстрая оборачиваемость и никаких затрат на маркетинг',.76)}
{bc('lock','Контроль и прозрачность','Все этапы сделки фиксируются в системе',.88)}
<div class="bc"><div class="last" style="--d:1s"><div><h4>DROPDEALER</h4><p class="t2">Больше конкуренции. Выше цена. Больше прибыли.</p></div></div></div>
</div></div></section>''')
S.append(f'''<section class="sl" id="s6"><div class="in">
<div class="eyebrow rv">Партнёры · дилерские центры на платформе</div>
{H([["Нас","рекомендуют",("дилеры","g")]],.1)}
<div class="lgrid">{logos}</div>
<div class="stats">
<div class="st rv" style="--d:1.1s"><b data-to="17">0</b><span>дилерских центров в 7 городах</span></div>
<div class="st y rv" style="--d:1.2s"><b data-to="2850" data-suf="+">0</b><span>проведено аукционов</span></div>
<div class="st rv" style="--d:1.3s"><b data-to="65" data-suf="%">0</b><span>проданных лотов</span></div>
</div></div></section>''')
S.append(f'''<section class="sl" id="s7"><div class="in tw">
<div><div class="eyebrow rv">Тарифы</div>
{H([["Стоимость"],[("наших","g"),("услуг","g")]],.1)}
<div class="pay u rv" style="--d:.5s">Дилер платит только<br>за состоявшиеся сделки</div>
<p class="tx rv" style="--d:.65s">Размер оплаты зависит от количества успешных сделок за месяц.</p>
<p class="res u rv" style="--d:.8s">Оплата за результат</p></div>
<div class="lad"><div class="lh rv" style="--d:.3s"><span>СДЕЛОК ЗА МЕСЯЦ</span><span>СТОИМОСТЬ В МЕСЯЦ</span></div>{lad}</div>
</div></section>''')
S.append(f'''<section class="sl dark" id="s8"><div class="in cta">
<div><div class="eyebrow rv" id="eb8">Готовы начать?</div>
{H([["Подключим"],["за",("30","g"),("минут.","g")]],.1)}
<div class="person rv" style="--d:.45s"><img src="{BORIS}" alt="Борис Мухин"><div><b>Борис Мухин</b><span>Бизнес-консультант практик · Собственник</span><small>Более 25 лет операционного управления в автобизнесе</small></div></div>
<div class="btns rv" style="--d:.7s"><a class="btn" href="tel:+79214088598">+7 921 408-85-98</a><button class="btn gh" id="copy">Скопировать номер</button></div>
<div class="links rv" style="--d:.8s"><a href="https://app.dropdealer.ru" target="_blank" rel="noopener"><small>ПРИЛОЖЕНИЕ</small>app.dropdealer.ru</a><a href="https://dropdealer.ru" target="_blank" rel="noopener"><small>САЙТ</small>dropdealer.ru</a><span><small>ПОЧТА</small>dropdealerspb@gmail.com</span></div>
<p class="sub sub2 rv" style="--d:.95s">Напишите или позвоните: менеджер создаст кабинет, обучит команду, и сегодня вы уже на торгах.</p>

</div>
<div class="orb rv" style="--d:.4s"><i></i><i></i><i></i><b><span data-to="30">0</span><small>МИНУТ</small></b></div>
</div></section>''')

# CSS для режима без JS (iOS Quick Look, предпросмотры): все слайды подряд, конечные состояния анимаций
_on=[l for l in open('css.txt').read().split('\n') if '.on ' in l]
_nj='\n'.join(l.replace('.on ','.sl ') for l in _on)
_nj=re.sub(r'(?<![\w#.\-])(-?\d*\.?\d+)u(?![\w\-])',lambda m:f'calc(var(--u)*{m.group(1)})',_nj)
NOJS='''html,body{height:auto!important;overflow:auto!important}body{display:block!important}
#app,#app.m,#app.land{--u:1cqw!important;position:static!important;width:100%!important;max-width:560px;margin:0 auto;height:auto!important;container-type:inline-size;overflow:visible!important}
#stage{position:static!important;perspective:none!important}
.sl{position:relative!important;inset:auto!important;visibility:visible!important;padding-top:calc(var(--u)*13)!important;padding-bottom:calc(var(--u)*12)!important}
.nav,.pgb,.hint,#fx,.tick,.topb,canvas.field{display:none!important}
.njn{background:#111214;color:#fff;font:500 14px/1.4 Onest,system-ui,sans-serif;padding:12px 16px;text-align:center}.njn a{color:#14D07E;font-weight:700}
'''+_nj
html=f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>DROPDEALER — презентация для дилеров</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700&family=Unbounded:wght@800;900&display=swap" rel="stylesheet">
<style>{css}</style><noscript><style>{NOJS}</style></noscript></head><body>
<noscript><div class="njn"><b>Версия без анимации.</b> Чтобы листать слайды с эффектами, откройте презентацию в браузере: <a href="https://nkmoigg-debug.github.io/Presentation/">nkmoigg-debug.github.io/Presentation</a></div></noscript>
<div id="app" class="m">
<div id="stage">{''.join(S)}</div>
<div id="fx"></div>
<header class="topb"><div class="logo"><s></s>DROPDEALER</div><div class="rt"><div class="sw"><button data-m="land">ПК</button><button data-m="m">ТЕЛЕФОН</button></div><div class="cnt"><b id="cn">01</b> / 0{len(S)}</div></div></header>
<nav class="nav">{''.join('<a></a>' for _ in S)}</nav>
<div class="pgb"><i id="pg"></i></div>
</div>
{LOTS_JS}<script>{js}</script></body></html>'''
def _c(m):
    n=int(m.group(2));suf=m.group(3) or ''
    return m.group(1)+f'{n:,}'.replace(',','\u00a0')+suf+'<'
html=re.sub(r'(data-to="(\d+)"(?: data-suf="([^"]*)")?[^>]*>)[^<]*<',_c,html)
open('index.html','w').write(html);print(len(html))

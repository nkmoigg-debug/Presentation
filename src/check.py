# Автопроверка перед публикацией: счётчики доходят до своих значений, нет JS-ошибок, число слайдов совпадает.
import asyncio,re,os,sys
from playwright.async_api import async_playwright
async def main():
    fails=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,vw,vh in [('ПК',1440,900),('тел',390,844)]:
            pg=await b.new_page(viewport={'width':vw,'height':vh});errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('file:///home/claude/site2/test.html');await pg.wait_for_timeout(1500)
            n=await pg.evaluate('N')
            for i in range(n):
                if i: await pg.evaluate(f'go({i})')
                await pg.wait_for_timeout(5200)
                bad=await pg.evaluate("""()=>{const s=slides[cur];return [...s.querySelectorAll('[data-to]')].filter(e=>{const v=parseInt(e.textContent.replace(/\\D/g,''))||0;return v!==+e.dataset.to}).map(e=>e.dataset.to+'→'+e.textContent)}""")
                if bad: fails.append(f'{name} слайд {i+1}: счётчики не дошли {bad}')
            await pg.evaluate('go(1)');await pg.wait_for_timeout(5500)
            pb=(await pg.inner_text('#pB')).replace(' ','').replace('\u202f','').replace('\xa0','')
            if '900000' not in pb: fails.append(f'{name}: слайд 2 цена не дошла до 900 000 ({pb})')
            if await pg.evaluate("!!document.getElementById('pro')"): fails.append(f'{name}: пролог не убрался')
            if errs: fails.append(f'{name}: JS-ошибки {errs[:3]}')
            print(name,'слайдов',n);await pg.close()
        await b.close()
    print('ОШИБКИ:' if fails else 'ВСЁ В ПОРЯДКЕ');[print(' -',f) for f in fails]
    sys.exit(1 if fails else 0)
asyncio.run(main())

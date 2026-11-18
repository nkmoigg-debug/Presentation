import json,sys,datetime
d=json.load(open(sys.argv[1]));items=d.get('items',d)
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
out=[{'t':x['title'],'c':x.get('city') or '','p':x.get('currentPrice') or x.get('startPrice'),'e':x['auctionEnd']} for x in items if x.get('auctionEnd') and x['auctionEnd']>now]
out.sort(key=lambda z:z['e'])
json.dump(out[:14],open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))

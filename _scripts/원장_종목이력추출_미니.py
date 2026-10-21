import duckdb, json, statistics, sys
c=duckdb.connect("/Users/benopenclaw/research-site/stable/warehouse/research.ro.duckdb",read_only=True)
T=sys.argv[2].split(",")
q=lambda s,p=(): c.execute(s,list(p)).fetchall()
out={}
for t in T:
    o={}
    # 1) 월별 목표가: 증권사별 그 달 최신 1건, 월 중앙값의 1/3–3배 밖은 버림(파싱 오류)
    rows=q("""select strftime(published_at,'%Y-%m') m, firm, target_price, published_at, opinion, title from reports
              where ticker=? and published_at>='2025-10-01' and target_price>0 and firm is not null order by published_at""",[t])
    bym={}
    for m,f,tp,d,op,ti in rows: bym.setdefault(m,{})[f]=(tp,str(d),op,ti)
    mon=[]
    for m in sorted(bym):
        v=[x[0] for x in bym[m].values()]; md=statistics.median(v)
        keep=[x for x in v if md/3<=x<=md*3]
        mon.append(dict(m=m,n=len(keep),med=statistics.median(keep),lo=min(keep),hi=max(keep),drop=len(v)-len(keep)))
    o["tp_monthly"]=mon
    # 2) 증권사별 목표가 변경 이력 → 큰 변경 상위
    seq={}
    for m,f,tp,d,op,ti in rows: seq.setdefault(f,[]).append((str(d),tp,op,ti))
    ch=[]
    for f,s in seq.items():
        for (d0,p0,_,_),(d1,p1,op,ti) in zip(s,s[1:]):
            if p0 and p1!=p0 and p0/3<=p1<=p0*3: ch.append(dict(date=d1,firm=f,prev=p0,tp=p1,pct=round((p1/p0-1)*100,1),title=ti,op=op))
    o["tp_changes"]=sorted(ch,key=lambda x:x["date"])
    # 3) DART 분기 실적(연결 우선, 억원)
    dq={}
    for pe,acc,v,fs in q("""select period_end, account, value, fs_div from dart_fin_quarterly where ticker=? and account in ('revenue','op_income')
                           and period_end>='2024-01-01' order by fs_div desc""",[t]):
        k=(str(pe),acc)
        if k not in dq or fs=='CFS': dq[k]=round(v/1e8)
    o["dart_q"]={f"{pe}|{a}":v for (pe,a),v in sorted(dq.items())}
    # 4) 네이버 컨센: 3Q26E·2026E·2027E 영업이익, 목표가 평균 — 10월 첫·마지막 스냅
    cons={}
    for sd,per,it,v in q("""select snap_date, period, item, value from naver_consensus_snap where ticker=? and is_estimate
                           and item in ('op_income','revenue') and period in ('2026Q3E','2026Q4E','2026E','2027E') order by snap_date""",[t]):
        cons.setdefault(f"{per}|{it}",{})[str(sd)]=v
    o["naver_cons"]={k:{"first":list(v.items())[0],"last":list(v.items())[-1]} for k,v in cons.items()}
    tg=q("select snap_date,target_avg,opinion_avg from naver_consensus_target where ticker=? order by snap_date",[t])
    o["naver_target"]={"first":(str(tg[0][0]),tg[0][1]),"last":(str(tg[-1][0]),tg[-1][1]),"opinion":tg[-1][2]} if tg else None
    # 5) 월말 종가
    pr=q("""select strftime(d,'%Y-%m') m, arg_max(close,d), max(d) from prices where symbol=? and d>='2025-09-01' group by 1 order by 1""",[t])
    o["px_monthly"]={m:v for m,v,_ in pr}
    out[t]=o
fx=q("""select period, value from macro_series where series_key='ECOS:731Y001:0000001' and period>='20250901' order by period""")
fxm={}
for p,v in fx: fxm[p[:6]]=(p,v)
out["_usdkrw_monthend"]=fxm
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False,indent=1,default=str)
print({t:(len(out[t]["tp_monthly"]),len(out[t]["dart_q"]),len(out[t]["naver_cons"])) for t in T})

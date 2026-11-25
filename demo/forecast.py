import json, math, random, statistics
from pathlib import Path

def classify(y):
    nz=[v for v in y if v>0]
    if not nz: return 'unknown', None, None
    adi=len(y)/len(nz); cv=(statistics.stdev(nz)/statistics.mean(nz))**2 if len(nz)>1 else 0
    return ('lumpy' if cv>=.49 else 'intermittent') if adi>=1.32 else ('erratic' if cv>=.49 else 'smooth'),adi,cv

def generate(seed=42):
    r=random.Random(seed); out={}
    for kind in ['smooth','erratic','intermittent','lumpy','unknown']:
        for i in range(6):
            out[f'{kind}-{i}']=[0 if kind=='unknown' or (kind in ['intermittent','lumpy'] and r.random()<.7) else r.choice([2,35]) if kind in ['erratic','lumpy'] else r.randint(9,15) for _ in range(180)]
    return out

def predict(history,kind):
    if kind=='unknown': return 0.
    if kind=='smooth': return statistics.mean(history[-7:])
    if kind=='erratic':
        threshold=statistics.median(history); high=[x for x in history if x>threshold]; low=[x for x in history if x<=threshold]; p=len(high)/len(history)
        return p*statistics.mean(high or [0])+(1-p)*statistics.mean(low or [0])
    nz=[x for x in history if x>0]; return len(nz)/len(history)*statistics.mean(nz or [0])

def metrics(rows,key):
    errors=[r[key]-r['actual'] for r in rows]; total=sum(r['actual'] for r in rows)
    return dict(MAE=statistics.mean(map(abs,errors)),RMSE=math.sqrt(statistics.mean(e*e for e in errors)),WAPE=sum(map(abs,errors))/total if total else None,bias=statistics.mean(errors))

def run():
    rows=[]; forecasts=[]; examples=[]
    for name,y in generate().items():
        for t in range(120,180):
            hist=y[:t]; kind,_,_=classify(hist); rows.append(dict(group=name,day=t,actual=y[t],prediction=predict(hist,kind),baseline=hist[-7]))
        kind,adi,cv=classify(y); future=[]; hist=y[:]
        for _ in range(14):
            v=predict(hist,kind); future.append(v); hist.append(v)
        forecasts.append(dict(group=name,route=kind,forecast=future)); examples.append(dict(group=name,route=kind,adi=adi,cv2=cv,history=y[-30:],forecast=future))
    return dict(scope='Synthetic reference implementation; statistical routing, not original XGBoost models',metrics=metrics(rows,'prediction'),baseline=metrics(rows,'baseline'),examples=examples,rows=rows,forecasts=forecasts)
if __name__=='__main__':
    p=Path(__file__).parent/'results.json'; p.write_text(json.dumps(run(),indent=2)); print(p)

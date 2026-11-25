"""Independent synthetic XGBoost reference; no enterprise connections."""
import json
from pathlib import Path
import numpy as np
from xgboost import XGBRegressor, XGBClassifier
from forecast import generate, classify, metrics

def features(y,t,g):
    return [g,t%7,t%30,y[t-1],y[t-7],np.mean(y[t-7:t]),np.mean(y[t-28:t])]

def run(output=None):
    series=list(generate().items()); routes={g:classify(y[:120])[0] for g,(_,y) in enumerate(series)}
    models={}; rows=[]; examples=[]; forecasts=[]
    def fit(cls,X,y,name):
        model=cls(n_estimators=60,max_depth=3,learning_rate=.08,n_jobs=1,random_state=42)
        model.fit(X,y)
        if output: model.save_model(output/name)
        return model
    for route in sorted(set(routes.values())):
        if route=='unknown': continue
        pairs=[(features(y,t,g),y[t]) for g,(_,y) in enumerate(series) if routes[g]==route for t in range(28,120)]
        X=np.array([a for a,b in pairs]); y=np.array([b for a,b in pairs]);
        if route=='smooth': models[route]=(fit(XGBRegressor,X,y,route+'.json'),)
        else:
            mask=y>=np.percentile(y[y>0],95) if route=='erratic' else y>0
            if len(set(mask))<2: models[route]=(fit(XGBRegressor,X,y,route+'.json'),); continue
            c=fit(XGBClassifier,X,mask.astype(int),route+'-classifier.json'); hi=fit(XGBRegressor,X[mask],y[mask],route+'-high.json'); lo=fit(XGBRegressor,X[~mask],y[~mask],route+'-low.json') if route=='erratic' else None
            models[route]=(c,hi,lo)
    def pred(route,x):
        if route=='unknown': return 0.
        a=models[route]; X=np.array([x]);
        if len(a)==1: return max(0.,float(a[0].predict(X)[0]))
        prob=float(a[0].predict_proba(X)[0,1]); return max(0.,prob*float(a[1].predict(X)[0])+(1-prob)*(float(a[2].predict(X)[0]) if a[2] is not None else 0.))
    for g,(name,y) in enumerate(series):
        route=routes[g]
        for t in range(120,180): rows.append(dict(group=name,day=t,actual=y[t],prediction=pred(route,features(y,t,g)),baseline=y[t-7]))
        hist=y[:]; future=[]
        for t in range(180,194):
            v=pred(route,features(hist,t,g)); hist.append(v); future.append(v)
        _,adi,cv=classify(y[:120]); examples.append(dict(group=name,route=route,adi=adi,cv2=cv,history=y[-30:],forecast=future)); forecasts.append(dict(group=name,route=route,forecast=future))
    return dict(scope='XGBoost synthetic reference; fixed training days 0–119; rolling one-step holdout days 120–179; recursive 14-day forecast using same fitted models',metrics=metrics(rows,'prediction'),baseline=metrics(rows,'baseline'),examples=examples,rows=rows,forecasts=forecasts,routes=routes)
if __name__=='__main__':
    p=Path(__file__).parent; out=p/'models'; out.mkdir(exist_ok=True); result=run(out); (p/'xgb-results.json').write_text(json.dumps(result,indent=2)); print(result['metrics'],result['baseline'])

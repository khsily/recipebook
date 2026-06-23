from __future__ import annotations
import hashlib,json,math,os,platform,random,re,sys,time
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from datasets import load_dataset
from rank_bm25 import BM25Okapi
from scipy.stats import wilcoxon
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

SEED=20260623
RRF_K=60
ONTO_W=.75
WORD=re.compile(r'[가-힣A-Za-z0-9]+')
ARTICLE=re.compile(r'제\s*\d+(?:의\d+)?\s*조(?:의\s*\d+)?')
STATUTE=re.compile(r'([가-힣A-Za-z· ]{2,30}법)\s*제\s*(\d+(?:의\d+)?)\s*조')
ONTO={
'loan':('civil_obligation',['대여','차용','대여금','차용금','금전소비대차','빌려준 돈','빚']),
'guarantee':('civil_obligation',['보증','연대보증','보증인','주채무','보증채무']),
'limitation':('civil_obligation',['소멸시효','시효완성','시효중단','제척기간']),
'setoff':('civil_obligation',['상계','자동채권','수동채권']),
'assignment':('civil_obligation',['채권양도','양수인','양도인','대항요건']),
'revocation':('civil_obligation',['사해행위','채권자취소권','원상회복','수익자','전득자']),
'contract':('civil',['계약','청약','승낙','해제','해지','위약금']),
'sale':('contract',['매매','매도인','매수인','매매대금','하자담보']),
'lease':('contract',['임대차','임대인','임차인','차임','보증금']),
'construction':('contract',['도급','수급인','도급인','공사대금','하도급']),
'property':('civil',['소유권','물권','점유','부동산','동산','인도']),
'registration':('property',['등기','소유권이전등기','말소등기','부기등기']),
'mortgage':('property',['저당권','근저당권','채권최고액','물상보증','담보권']),
'acquisitive_prescription':('property',['취득시효','점유취득시효','등기부취득시효']),
'tort':('civil',['불법행위','손해배상','과실상계','위자료','공동불법행위']),
'family':('civil',['혼인','이혼','친권','양육','상속','유류분','유언']),
'company':('commercial',['주식회사','대표이사','주주총회','이사회','주주']),
'civil_litigation':('procedure',['민사소송','원고','피고','소의 이익','청구']),
'res_judicata':('civil_litigation',['기판력','확정판결','변론종결','전소','후소','재소']),
'intervention':('civil_litigation',['보조참가','독립당사자참가','참가적 효력','공동소송']),
'appeal':('procedure',['항소','상고','상소','항소기간','불이익변경금지','이심']),
'provisional':('civil_litigation',['가압류','가처분','보전처분','강제집행']),
'evidence':('procedure',['증거','증명','증거능력','증명력','자백']),
'criminal_general':('criminal',['범죄','고의','과실','위법성','책임','구성요건']),
'complicity':('criminal_general',['공동정범','교사범','방조범','공범','간접정범']),
'attempt':('criminal_general',['미수','중지미수','불능미수','예비','음모']),
'mistake':('criminal_general',['착오','사실의 착오','법률의 착오']),
'defense':('criminal_general',['정당방위','긴급피난','자구행위']),
'property_crime':('criminal',['절도','강도','사기','횡령','배임']),
'violent_crime':('criminal',['폭행','상해','살인','협박','강제추행']),
'document_crime':('criminal',['문서위조','사문서위조','공문서위조','위조문서행사']),
'criminal_procedure':('procedure',['형사소송','수사','공소','피고인','피의자','검사']),
'warrant':('criminal_procedure',['영장','압수수색','체포','구속','긴급체포']),
'confession':('criminal_procedure',['자백','자백보강','진술거부권','피의자신문']),
'hearsay':('criminal_procedure',['전문법칙','전문증거','진술조서','증거동의']),
'administrative':('public',['행정','행정청','처분','허가','인가']),
'administrative_act':('administrative',['행정행위','처분성','공정력','불가쟁력','하자승계']),
'administrative_litigation':('administrative',['취소소송','무효확인소송','당사자소송','원고적격']),
'constitutional':('public',['헌법','기본권','위헌','헌법재판','법률유보']),
'constitutional_complaint':('constitutional',['헌법소원','권리보호이익','보충성','직접성']),
'labor':('social',['근로자','사용자','근로계약','해고','임금','퇴직금','노동조합']),
'tax':('public',['조세','과세','세금','납세','부가가치세','소득세'])}
REL={
'limitation':{'res_judicata','civil_obligation'},'res_judicata':{'limitation','appeal'},
'guarantee':{'loan','civil_obligation'},'revocation':{'registration','civil_obligation'},
'mortgage':{'registration','property','provisional'},'intervention':{'res_judicata','appeal'},
'lease':{'contract','registration'},'construction':{'contract','civil_obligation'},
'hearsay':{'evidence','criminal_procedure'},'confession':{'evidence','criminal_procedure'},
'warrant':{'evidence','criminal_procedure'},'administrative_litigation':{'administrative_act','constitutional'},
'constitutional_complaint':{'constitutional','administrative_litigation'}}
NORM=[(r'빌려\s*준\s*돈|빌린\s*돈|빚',' 대여금 채무 '),(r'보증을\s*선|보증인',' 연대보증 '),(r'집주인',' 임대인 '),(r'세입자',' 임차인 '),(r'등기를\s*지우',' 말소등기 '),(r'재판이\s*끝난|판결이\s*확정',' 확정판결 기판력 '),(r'기간이\s*지나',' 소멸시효 기간경과 ')]

def norm(x,rules=True):
 x=str(x or '').replace('\u3000',' ')
 if rules:
  for a,b in NORM:x=re.sub(a,b,x)
 return re.sub(r'\s+',' ',x).strip()
def tok(x):
 out=[]
 for t in WORD.findall(norm(x).lower()):
  out.append(t)
  if len(t)>=5 and re.search('[가-힣]',t):out += [t[i:i+3] for i in range(len(t)-2)]
 return out
def concepts(x,normal=True):
 t=norm(x,normal).lower();return {c for c,(_,a) in ONTO.items() if any(z.lower() in t for z in a)}
def ancestors(c):
 out=[];seen={c}
 while c in ONTO:
  p=ONTO[c][0]
  if not p or p in seen:break
  out.append(p);seen.add(p);c=p
 return out
def expand(cs,h=True,r=True):
 w={c:1. for c in cs}
 if h:
  for c in cs:
   for d,a in enumerate(ancestors(c),1):w[a]=max(w.get(a,0),.45/d)
 if r:
  for c in cs:
   for a in REL.get(c,set()):w[a]=max(w.get(a,0),.55)
 return w
def statutes(x):return {re.sub(r'\s+','',a)+'제'+b+'조' for a,b in STATUTE.findall(x)}
def parse_item(x):
 if isinstance(x,str):
  try:x=json.loads(x)
  except:return [('unknown',x)]
 return list(x.items()) if isinstance(x,dict) else []
def load():
 ds=load_dataset('lbox/kcl','kcl_mcqa',split='test');qs=[];docs={};gold=[]
 for qid,e in enumerate(ds):
  g=set()
  for raw in e.get('supporting_precedents') or []:
   for title,body in parse_item(raw):
    key=hashlib.sha1((norm(title)+'\n'+norm(body,False)).encode()).hexdigest()[:16]
    docs.setdefault(key,{'doc_id':key,'title':str(title),'content':str(body)});g.add(key)
  qs.append({'qid':qid,'meta':str(e.get('meta','')),'question':str(e.get('question','')),
   **{c:str(e.get(c,'')) for c in 'ABCDE'},'label':str(e.get('label','')),'n_gold':len(g)})
  gold.append(g)
 return pd.DataFrame(qs),pd.DataFrame(docs.values()).sort_values('doc_id').reset_index(drop=True),gold
def qtext(r,full=True):return r.question if not full else r.question+'\n선택지: '+' '.join(f'{c}. {r[c]}' for c in 'ABCDE')
def dtext(r):return r.title+'\n'+r.content
def ontology_scores(qs,ds,normal=True,h=True,r=True,s=True):
 qc=[concepts(x,normal) for x in qs];dc=[concepts(x,normal) for x in ds];qe=[expand(x,h,r) for x in qc];de=[expand(x,h,r) for x in dc]
 df=Counter();[df.update(x) for x in dc];n=len(ds);idf={c:math.log((n+1)/(df.get(c,0)+1))+1 for c in ONTO};default=math.log(n+1)+1
 qst=[statutes(x) for x in qs];dst=[statutes(x) for x in ds];out=np.zeros((len(qs),n),np.float32)
 for i,a in enumerate(qe):
  an=math.sqrt(sum((v*idf.get(k,default))**2 for k,v in a.items())) or 1
  for j,b in enumerate(de):
   common=set(a)&set(b)
   if common:
    bn=math.sqrt(sum((v*idf.get(k,default))**2 for k,v in b.items())) or 1
    out[i,j]=sum(a[k]*b[k]*idf.get(k,default)**2 for k in common)/(an*bn)
   if s and qst[i] and dst[j]:out[i,j]+=.35*len(qst[i]&dst[j])
 return out
def ranks(s):return np.argsort(-s,axis=1,kind='mergesort')
def bm25(qs,ds):
 b=BM25Okapi([tok(x) for x in ds],k1=1.5,b=.75);return np.vstack([b.get_scores(tok(q)) for q in qs]).astype('float32')
def char(qs,ds):
 v=TfidfVectorizer(analyzer='char',ngram_range=(2,5),sublinear_tf=True,norm='l2');d=v.fit_transform(ds);return (v.transform(qs)@d.T).toarray().astype('float32')
def dense(qs,ds,model):
 m=SentenceTransformer(model,device='cpu');q=m.encode(['query: '+x for x in qs],batch_size=32,normalize_embeddings=True,show_progress_bar=True);d=m.encode(['passage: '+x for x in ds],batch_size=32,normalize_embeddings=True,show_progress_bar=True);return np.asarray(q@d.T,dtype='float32')
def rrf(rs,ws,k=RRF_K):
 nq,nd=rs[0].shape;out=np.zeros((nq,nd),np.float32);rows=np.arange(nq)[:,None]
 for r,w in zip(rs,ws):
  inv=np.empty_like(r);inv[rows,r]=np.arange(nd)[None,:];out += w/(k+inv+1.)
 return out
def one_metric(r,g):
 if not g:return {x:np.nan for x in ['Recall@1','Recall@5','Recall@10','MRR@10','nDCG@10','MAP@10']}
 o={f'Recall@{k}':len(set(r[:k])&g)/len(g) for k in (1,5,10)};rr=ap=dcg=0.;hit=0
 for p,x in enumerate(r[:10],1):
  if x in g:
   hit+=1;rr=rr or 1/p;ap+=hit/p;dcg+=1/math.log2(p+1)
 ideal=sum(1/math.log2(i+1) for i in range(1,min(len(g),10)+1));o.update({'MRR@10':rr,'nDCG@10':dcg/ideal,'MAP@10':ap/min(len(g),10)});return o
def evaluate(methods,gold,docids):
 idx={d:i for i,d in enumerate(docids)};gs=[{idx[x] for x in g} for g in gold];summ=[];per=[]
 for name,rank in methods.items():
  rows=[]
  for qid,(r,g) in enumerate(zip(rank,gs)):
   m=one_metric(r,g);rows.append(m);per.append({'method':name,'qid':qid,**m,'top_doc':docids[int(r[0])]})
  f=pd.DataFrame(rows);summ.append({'method':name,'n_queries':f['MRR@10'].notna().sum(),**{c:f[c].mean() for c in f.columns}})
 return pd.DataFrame(summ),pd.DataFrame(per)
def bootstrap(a,b,n=10000):
 rng=np.random.default_rng(SEED);d=b-a;means=[]
 for _ in range(n//500):means.extend(d[rng.integers(0,len(d),(500,len(d)))].mean(1))
 means=np.array(means);return {'mean_difference':float(d.mean()),'ci_low':float(np.quantile(means,.025)),'ci_high':float(np.quantile(means,.975)),'p_bootstrap_two_sided':float(2*min((means<=0).mean(),(means>=0).mean()))}
def domain(meta,q):
 x=meta+' '+q
 if any(k in x for k in ['형사','형법','형사소송']):return '형사'
 if any(k in x for k in ['민사','민법','민사소송','상법']):return '민사'
 if any(k in x for k in ['헌법','행정']):return '공법'
 return '기타'
def drop_terms(x,seed,rate=.2):
 rng=random.Random(seed);aliases=sorted({z for _,a in ONTO.values() for z in a},key=len,reverse=True)
 for z in [z for z in aliases if z in x]:
  if rng.random()<rate:x=x.replace(z,' ')
 return norm(x,False)
def main():
 out=Path(os.getenv('RESULT_DIR','research/ontology_korean_qa/results'));out.mkdir(parents=True,exist_ok=True);model=os.getenv('MODEL_NAME','intfloat/multilingual-e5-small');start=time.time()
 qdf,ddf,gold=load();qs=[qtext(r) for _,r in qdf.iterrows()];qonly=[qtext(r,False) for _,r in qdf.iterrows()];ds=[dtext(r) for _,r in ddf.iterrows()];docids=ddf.doc_id.tolist();tim={}
 t=time.perf_counter();bs=bm25(qs,ds);tim['BM25_s']=time.perf_counter()-t
 t=time.perf_counter();cs=char(qs,ds);tim['Char_s']=time.perf_counter()-t
 t=time.perf_counter();es=dense(qs,ds,model);tim['E5_s']=time.perf_counter()-t
 t=time.perf_counter();oscore=ontology_scores(qs,ds);tim['Ontology_s']=time.perf_counter()-t
 br,cr,er,orr=map(ranks,[bs,cs,es,oscore]);hr=ranks(rrf([br,er],[1,1]));ohr=ranks(rrf([br,er,orr],[1,1,ONTO_W]))
 methods={'BM25':br,'CharTFIDF':cr,'Dense-E5':er,'RRF-Hybrid':hr,'Ontology-Hybrid':ohr};met,per=evaluate(methods,gold,docids);met.to_csv(out/'metrics_overall.csv',index=False)
 qmeta=qdf[['qid','meta','question','n_gold']].copy();qmeta['domain']=[domain(m,q) for m,q in zip(qmeta.meta,qmeta.question)];per=per.merge(qmeta,on='qid');titles=ddf.set_index('doc_id').title.to_dict();per['top_title']=per.top_doc.map(titles);per.to_csv(out/'per_query_metrics.csv',index=False);per.groupby(['method','domain'])[['Recall@1','Recall@5','Recall@10','MRR@10','nDCG@10','MAP@10']].mean().reset_index().to_csv(out/'metrics_by_domain.csv',index=False)
 abl={'Hybrid':hr}
 for name,opt in {'+Normalization':(True,False,False,False),'+Hierarchy':(True,True,False,False),'+Relations':(True,True,True,False),'Full(+Statute)':(True,True,True,True)}.items():
  rr=ranks(ontology_scores(qs,ds,*opt));abl[name]=ranks(rrf([br,er,rr],[1,1,ONTO_W]))
 evaluate(abl,gold,docids)[0].to_csv(out/'ablation.csv',index=False)
 sens=[]
 for k in [20,60,100]:
  for w in [.25,.5,.75,1.,1.5]:
   x=evaluate({'x':ranks(rrf([br,er,orr],[1,1,w],k))},gold,docids)[0].iloc[0].to_dict();x.update({'rrf_k':k,'ontology_weight':w});sens.append(x)
 pd.DataFrame(sens).drop(columns='method').to_csv(out/'sensitivity.csv',index=False)
 variants={'Full item':qs,'Question only':qonly,'Article masked':[ARTICLE.sub('[조문]',x) for x in qs]}
 for s in range(5):variants[f'Legal-term dropout s{s}']=[drop_terms(x,SEED+s) for x in qs]
 robust=[]
 for name,vq in variants.items():
  vb=ranks(bm25(vq,ds));ve=ranks(dense(vq,ds,model));vo=ranks(ontology_scores(vq,ds));vh=ranks(rrf([vb,ve],[1,1]));vho=ranks(rrf([vb,ve,vo],[1,1,ONTO_W]));x=evaluate({'RRF-Hybrid':vh,'Ontology-Hybrid':vho},gold,docids)[0];x.insert(0,'variant',name);robust.append(x)
 pd.concat(robust).to_csv(out/'robustness.csv',index=False)
 piv=per.pivot(index='qid',columns='method',values=['MRR@10','nDCG@10','Recall@5']);sig={}
 for m in ['MRR@10','nDCG@10','Recall@5']:
  a=piv[m]['RRF-Hybrid'].dropna().to_numpy();b=piv[m]['Ontology-Hybrid'].dropna().to_numpy();x=bootstrap(a,b);st,p=wilcoxon(b,a,zero_method='pratt');x.update({'wilcoxon_stat':float(st),'wilcoxon_p':float(p)});sig[m]=x
 (out/'significance.json').write_text(json.dumps(sig,ensure_ascii=False,indent=2))
 idx={d:i for i,d in enumerate(docids)};gs=[{idx[x] for x in g} for g in gold]
 def first(rank,g):
  for p,x in enumerate(rank,1):
   if x in g:return p
  return np.inf
 err=qmeta.copy();err['hybrid_rank']=[first(r,g) for r,g in zip(hr,gs)];err['ontology_rank']=[first(r,g) for r,g in zip(ohr,gs)];err['rr_gain']=np.where(np.isfinite(err.ontology_rank),1/err.ontology_rank,0)-np.where(np.isfinite(err.hybrid_rank),1/err.hybrid_rank,0);err.nlargest(15,'rr_gain').to_csv(out/'largest_gains.csv',index=False);err.nsmallest(15,'rr_gain').to_csv(out/'largest_losses.csv',index=False)
 prov={'dataset':'lbox/kcl','config':'kcl_mcqa','split':'test','n_questions':len(qdf),'n_unique_precedents':len(ddf),'n_question_precedent_links':sum(map(len,gold)),'n_questions_without_gold':sum(not g for g in gold),'corpus_sha256':hashlib.sha256('\n'.join(sorted(docids)).encode()).hexdigest()};(out/'dataset_provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2))
 desc={**prov,'mean_gold_per_question':float(np.mean(list(map(len,gold)))),'median_question_chars':float(np.median(list(map(len,qs)))),'median_precedent_chars':float(np.median(list(map(len,ds)))),'query_ontology_coverage':float(np.mean([bool(concepts(x)) for x in qs])),'document_ontology_coverage':float(np.mean([bool(concepts(x)) for x in ds])),'ontology_nodes':len(ONTO),'ontology_relation_edges':sum(map(len,REL.values()))};(out/'descriptive_statistics.json').write_text(json.dumps(desc,ensure_ascii=False,indent=2))
 meta={'seed':SEED,'rrf_k':RRF_K,'ontology_weight':ONTO_W,'dense_model':model,'python':sys.version,'platform':platform.platform(),'timings':tim,'elapsed_total_s':time.time()-start};(out/'run_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));print(met.to_string(index=False));print(json.dumps(prov,ensure_ascii=False))
if __name__=='__main__':main()

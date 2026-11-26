#!/usr/bin/env python3
"""SAE QNX local agent: fixed allowlist; no arbitrary shell."""
import argparse,json,os,platform,subprocess,sys,time,urllib.request,urllib.error
from pathlib import Path
ACTIONS={"inspect":[sys.executable,"sae_qnx_assurance.py","inspect"],"self-test":[sys.executable,"sae_qnx_assurance.py","self-test"],"unit-tests":[sys.executable,"-m","unittest","discover","-s","tests","-v"],"build-aarch64":[sys.executable,"sae_qnx_assurance.py","build","--arch","aarch64"],"build-x86_64":[sys.executable,"sae_qnx_assurance.py","build","--arch","x86_64"]}
ROOT=Path(__file__).resolve().parents[1];CONFIG=Path.home()/".sae-qnx-assurance"/"agent.json"
HEARTBEAT_INTERVAL=300
POLL_INTERVAL=10
def call(base,path,token=None,body=None):
 data=json.dumps(body or {}).encode();h={"Content-Type":"application/json","Accept":"application/json","User-Agent":"SAE-QNX-Assurance-Agent/0.4 (+https://qnx.profmanuelgago.pw)"}
 if token:h["Authorization"]="Bearer "+token
 req=urllib.request.Request(base.rstrip("/")+path,data=data,headers=h,method="POST")
 with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read().decode())
def pair(base,code):
 r=call(base,"/api/agent/pair",body={"code":code,"device":platform.node()});CONFIG.parent.mkdir(parents=True,exist_ok=True);CONFIG.write_text(json.dumps({"api_base":base,"token":r["token"]},indent=2),encoding="utf-8")
 try:os.chmod(CONFIG,0o600)
 except OSError:pass
 print("PAIRING_OK; token stored at",CONFIG,". Do not share it.")
def run():
 if not CONFIG.is_file():raise SystemExit("Not paired. Use: python agent/sae_qnx_agent.py pair --url https://qnx-agent.profmanuelgago.pw --code <pairing-code>")
 c=json.loads(CONFIG.read_text(encoding="utf-8"));base=c["api_base"];token=c["token"];print("SAE QNX agent active:",ROOT)
 last_heartbeat=0.0
 while True:
  try:
   now=time.monotonic()
   if now-last_heartbeat>=HEARTBEAT_INTERVAL:
    call(base,"/api/agent/heartbeat",token);last_heartbeat=now
   job=call(base,"/api/agent/poll",token).get("job")
   if not job:time.sleep(POLL_INTERVAL);continue
   action=job.get("action")
   if action not in ACTIONS:r={"id":job["id"],"ok":False,"exit_code":126,"output":"Action rejected"}
   else:
    p=subprocess.run(ACTIONS[action],cwd=ROOT,capture_output=True,text=True,timeout=300,shell=False);artifacts=[]
    names=[]
    if action=="inspect":names=["environment-report.json"]
    elif action=="build-aarch64":names=["environment-report.json","build-evidence-aarch64.json","qcc-build-aarch64.log"]
    elif action=="build-x86_64":names=["environment-report.json","build-evidence-x86_64.json","qcc-build-x86_64.log"]
    for name in names:
     f=ROOT/"evidence"/name
     if f.is_file():
      try:artifacts.append({"name":name,"content":f.read_text(encoding="utf-8")[-12000:]})
      except OSError:pass
    r={"id":job["id"],"action":action,"ok":p.returncode==0,"exit_code":p.returncode,"output":((p.stdout or "")+"\n"+(p.stderr or ""))[-12000:],"artifacts":artifacts}
   call(base,"/api/agent/result",token,r);print(action,r["ok"],r["exit_code"])
  except urllib.error.HTTPError as e:
   detail=e.read().decode(errors="replace")[:500];print("HTTP",e.code,detail)
   time.sleep(300 if e.code==429 else 30)
  except Exception as e:print(type(e).__name__,str(e));time.sleep(30)
def main():
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True);q=s.add_parser("pair");q.add_argument("--url",required=True);q.add_argument("--code",required=True);s.add_parser("run");a=p.parse_args()
 if a.cmd=="pair":pair(a.url,a.code)
 else:run()
if __name__=="__main__":main()

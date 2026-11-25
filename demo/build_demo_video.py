import asyncio, os, re, subprocess, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import imageio_ffmpeg

ROOT = Path(r"C:\Users\manue\qnx-work\sae-qnx-assurance-bridge")
OUTDIR = ROOT / "demo"
OUTDIR.mkdir(exist_ok=True)
RAW = OUTDIR / "qnx_demo_silent.mp4"
AUDIO = OUTDIR / "qnx_demo_voice_en.mp3"
WAV = OUTDIR / "qnx_demo_voice_en.wav"
FINAL = OUTDIR / "SAE_QNX_Assurance_Bridge_Demo_EN.mp4"
SCRIPT = OUTDIR / "VOICEOVER_SCRIPT_EN.txt"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W,H,FPS = 1280,720,24

paragraphs = [
"SAE QNX Assurance Bridge is a host-side validation tool for software targeting QNX SDP 8.0.",
"It starts by inspecting the installed SDK and checking the QNX qcc compiler components. Five automated host tests pass, followed by a command-line self-test. The inspected environment reports ready for build.",
"The tool compiles the same QNX-specific C probe for AArch64 and x86-64, using strict warning settings. Both outputs pass ELF64 architecture validation, and the evidence records build logs and SHA-256 hashes.",
"Next, the x86-64 probe is transferred into a running QNX 8.0.0 guest under QEMU. The guest identifies itself as QNX, and the probe executes inside the Neutrino environment.",
"The probe creates a message channel, attaches a client connection, sends a message, receives it on the server side, and replies. The live guest session reports qnx_msgsend equals one and an exit code of zero.",
"AArch64 cross-compilation is verified; AArch64 runtime execution is not yet tested. This tool supports engineering validation; it is not a functional-safety certification.",
"The public MIT-licensed repository includes source code, build logs, machine-readable evidence and repeatable runtime instructions. SAE QNX Assurance Bridge: reproducible checks, inspectable evidence, accountable engineering."
]
full_script = "\n\n".join(paragraphs)
SCRIPT.write_text(full_script, encoding="utf-8")

async def make_voice():
    communicate = edge_tts.Communicate(
        full_script, "en-US-AvaNeural",
        rate="-3%", volume="+0%", pitch="-1Hz"
    )
    await communicate.save(str(AUDIO))

asyncio.run(make_voice())

subprocess.run([FFMPEG, "-y", "-i", str(AUDIO), "-ac", "1", "-ar", "24000", str(WAV)],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
with wave.open(str(WAV), "rb") as wf:
    audio_duration = wf.getnframes() / float(wf.getframerate())
duration = audio_duration + 1.6
frames_total = int(duration * FPS)

font_dir = Path(r"C:\Windows\Fonts")
def font(name, size):
    candidates = [font_dir/name, font_dir/"segoeui.ttf", font_dir/"arial.ttf"]
    for f in candidates:
        if f.exists():
            return ImageFont.truetype(str(f), size=size)
    return ImageFont.load_default()

F_REG = font("segoeui.ttf", 24)
F_MED = font("segoeuib.ttf", 27)
F_TITLE = font("segoeuib.ttf", 56)
F_H1 = font("segoeuib.ttf", 38)
F_H2 = font("segoeuib.ttf", 28)
F_SMALL = font("segoeui.ttf", 18)
F_MONO = font("consola.ttf", 19)
F_MONO_SM = font("consola.ttf", 16)

BG1 = (11, 17, 26)
BG2 = (19, 35, 49)
STEEL = (125, 174, 204)
PALE = (226, 237, 244)
MUTED = (156, 177, 193)
RED = (191, 93, 96)
GREEN = (123, 190, 156)
PANEL = (17, 27, 39)
PANEL2 = (24, 39, 54)
BORDER = (54, 79, 99)

def rounded(draw, box, radius=18, fill=PANEL, outline=BORDER, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def fit_text(draw, text, fnt, max_width):
    words=text.split()
    lines=[]; line=""
    for word in words:
        test=(line+" "+word).strip()
        if draw.textbbox((0,0),test,font=fnt)[2] <= max_width:
            line=test
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    return lines

def multiline(draw, xy, text, fnt, fill, max_width, spacing=8):
    x,y=xy
    for line in fit_text(draw,text,fnt,max_width):
        draw.text((x,y),line,font=fnt,fill=fill)
        y += fnt.size + spacing
    return y

def background(scene):
    yy,xx=np.mgrid[0:H,0:W]
    t=(xx/W*0.55 + yy/H*0.45)
    arr=np.zeros((H,W,3),dtype=np.uint8)
    for k,(a,b) in enumerate(zip(BG1,BG2)):
        arr[:,:,k]=(a+(b-a)*t).astype(np.uint8)
    # Subtle diagonal grid and ambient glow
    cx,cy=int(W*(0.72 if scene%2 else 0.25)),int(H*0.34)
    glow=np.exp(-(((xx-cx)**2)/(2*(W*0.36)**2)+((yy-cy)**2)/(2*(H*0.55)**2)))
    for k,c in enumerate(STEEL):
        arr[:,:,k]=np.clip(arr[:,:,k].astype(float)+glow*c*0.10,0,255)
    im=Image.fromarray(arr,"RGB")
    d=ImageDraw.Draw(im,"RGBA")
    for x in range(-H,W,70):
        d.line((x,0,x+H,H),fill=(130,170,196,16),width=1)
    for y in range(60,H,70):
        d.line((0,y,W,y),fill=(130,170,196,10),width=1)
    return im

def header(d, kicker, page):
    d.text((64,38),kicker.upper(),font=F_SMALL,fill=STEEL)
    d.text((1110,40),f"DEMO  /  {page:02d}",font=F_SMALL,fill=MUTED)

def footer(d, page, caption):
    d.line((64,650,W-64,650),fill=BORDER,width=1)
    d.text((64,670),"SAE  ·  PROF. MANUEL GAGO FERNÁNDEZ",font=F_SMALL,fill=MUTED)
    d.text((W-64,670),"QNX 8.0  |  "+page,font=F_SMALL,fill=STEEL,anchor="ra")
    # Caption strip
    d.rounded_rectangle((64,590,W-64,632),radius=10,fill=(8,14,22,220),outline=(55,78,98,150),width=1)
    d.text((84,599),caption,font=F_SMALL,fill=PALE)

def terminal(d, box, title, lines, line_color=GREEN, fs=F_MONO):
    x1,y1,x2,y2=box
    rounded(d,box,16,PANEL,(61,88,108),2)
    d.rounded_rectangle((x1,y1,x2,y1+42),radius=16,fill=(29,45,60),outline=(61,88,108),width=1)
    d.rectangle((x1,y1+25,x2,y1+42),fill=(29,45,60))
    for i,c in enumerate((RED,(210,174,104),GREEN)):
        d.ellipse((x1+18+i*22,y1+15,x1+29+i*22,y1+26),fill=c)
    d.text((x1+105,y1+10),title,font=F_SMALL,fill=MUTED)
    y=y1+60
    for item in lines:
        if y+fs.size+6>y2-12: break
        if isinstance(item,tuple):
            text,color=item
        else:
            text,color=item,line_color
        d.text((x1+24,y),text,font=fs,fill=color)
        y+=fs.size+7

def scene_image(idx):
    im=background(idx); d=ImageDraw.Draw(im,"RGBA")
    if idx==0:
        header(d,"QNX 8.0  ·  Developer tooling",1)
        d.text((70,170),"SAE QNX",font=F_TITLE,fill=PALE)
        d.text((70,240),"ASSURANCE BRIDGE",font=F_TITLE,fill=STEEL)
        multiline(d,(74,330),"A host-side validation toolkit for reproducible QNX development checks.",F_H2,MUTED,650,10)
        rounded(d,(800,180,1160,500),28,(15,27,39,235),(70,108,133),2)
        # Original abstract architecture motif, not a QNX logo
        nodes=[(900,270),(1050,230),(1000,380),(850,430),(1100,430)]
        for a,b in [(0,1),(0,2),(0,3),(2,4),(1,4),(3,2)]:
            d.line((*nodes[a],*nodes[b]),fill=(112,165,195,180),width=4)
        for x,y in nodes:
            d.ellipse((x-18,y-18,x+18,y+18),fill=STEEL,outline=PALE,width=3)
        d.text((70,510),"BUILD  ·  VALIDATE  ·  TRACE",font=F_MED,fill=PALE)
        footer(d,"01","A reproducible validation workflow for software targeting QNX SDP 8.0.")
    elif idx==1:
        header(d,"Host-side verification",2)
        d.text((64,105),"Start with a measurable baseline.",font=F_H1,fill=PALE)
        terminal(d,(64,180,780,540),"POWERSHELL  /  HOST CHECKS",[
            ("PS> python -m unittest discover -s tests -v",STEEL),
            ("test_elf_machine ..................... ok",GREEN),
            ("test_sdk_inspection_is_explicit ...... ok",GREEN),
            ("test_sha256 .......................... ok",GREEN),
            ("test_stage_source_copies_from_unicode_path  ok",GREEN),
            ("test_target_mapping .................. ok",GREEN),
            ("Ran 5 tests in 0.095s",PALE),
            ("OK",GREEN),
            ("SELF_TEST_PASS",GREEN),
            ("SDK status: READY_FOR_BUILD",GREEN)
        ],fs=F_MONO_SM)
        rounded(d,(830,210,1200,500),22,PANEL2,BORDER,2)
        d.text((870,250),"5 / 5",font=F_TITLE,fill=GREEN)
        d.text((870,330),"AUTOMATED",font=F_MED,fill=PALE)
        d.text((870,370),"TESTS PASS",font=F_MED,fill=PALE)
        d.text((870,440),"Exit code 0",font=F_SMALL,fill=MUTED)
        footer(d,"02","The current Windows host run passed all five tests and the CLI self-test.")
    elif idx==2:
        header(d,"Cross-compilation and ELF validation",3)
        d.text((64,105),"One probe. Two target architectures.",font=F_H1,fill=PALE)
        cards=[(64,190,600,500,"AArch64","gcc_ntoaarch64le","ELF64  ·  machine 183","14,288 bytes",GREEN),
               (650,190,1186,500,"x86_64","gcc_ntox86_64","ELF64  ·  machine 62","14,016 bytes",GREEN)]
        for x1,y1,x2,y2,name,target,elf,size,col in cards:
            rounded(d,(x1,y1,x2,y2),22,PANEL,BORDER,2)
            d.text((x1+30,y1+26),name,font=F_TITLE,fill=STEEL)
            d.text((x1+32,y1+105),target,font=F_MONO,fill=MUTED)
            d.line((x1+30,y1+155,x2-30,y1+155),fill=BORDER,width=2)
            d.text((x1+32,y1+185),elf,font=F_H2,fill=PALE)
            d.text((x1+32,y1+232),size,font=F_MED,fill=col)
            d.text((x1+32,y1+275),"-Wall  -Wextra  -Werror",font=F_MONO_SM,fill=MUTED)
        d.text((64,535),"Both cross-builds passed. AArch64 runtime has not been tested.",font=F_MED,fill=PALE)
        footer(d,"03","The bridge validates ELF class and machine architecture; build success is not runtime proof.")
    elif idx==3:
        header(d,"QNX Neutrino runtime",4)
        d.text((64,100),"The probe runs inside a real QNX guest.",font=F_H1,fill=PALE)
        terminal(d,(64,165,1216,548),"QNX SERIAL CONSOLE  /  LIVE GUEST SESSION · 26 NOV 2026",[
            ("$ uname -a",STEEL),
            ("QNX qnxqemu 8.0.0 2026/06/05 x86pc x86_64",PALE),
            ("$ uname -m",STEEL),
            ("x86pc",PALE),
            ("$ /tmp/sae_qnx_probe",STEEL),
            ("SAE_QNX_PROBE_V2",GREEN),
            ("runtime_sysname=QNX   runtime_release=8.0.0",GREEN),
            ("runtime_machine=x86pc   runtime_qnx=1",GREEN),
            ("qnx_msgsend=1",GREEN),
            ("$ echo PROBE_EXIT_CODE=$?",STEEL),
            ("PROBE_EXIT_CODE=0",GREEN)
        ],fs=F_MONO_SM)
        footer(d,"04","Captured from the active QEMU guest session; output is from the actual target execution.")
    elif idx==4:
        header(d,"Native Neutrino message passing",5)
        d.text((64,105),"A concrete IPC round trip.",font=F_H1,fill=PALE)
        steps=[("01","ChannelCreate","Create server channel"),
               ("02","ConnectAttach","Attach client"),
               ("03","MsgSend","Send PING"),
               ("04","MsgReceive","Receive request"),
               ("05","MsgReply","Return PONG")]
        x=64; y=230; widths=[210,210,210,210,210]
        for i,(num,name,desc) in enumerate(steps):
            x=64+i*235
            rounded(d,(x,y,x+205,y+190),18,PANEL2,BORDER,2)
            d.text((x+18,y+16),num,font=F_SMALL,fill=STEEL)
            multiline(d,(x+18,y+58),name,F_MED,PALE,170,4)
            multiline(d,(x+18,y+122),desc,F_SMALL,MUTED,170,4)
            if i<4:
                d.line((x+205,y+95,x+232,y+95),fill=STEEL,width=4)
                d.polygon([(x+232,y+95),(x+221,y+87),(x+221,y+103)],fill=STEEL)
        rounded(d,(300,475,980,545),16,(17,47,42),GREEN,2)
        d.text((355,492),"IPC ROUND TRIP  ·  PASS  ·  EXIT CODE 0",font=F_MED,fill=GREEN)
        footer(d,"05","The runtime probe exercises QNX Neutrino APIs, not a simulated host-side substitute.")
    elif idx==5:
        header(d,"Evidence and engineering boundaries",6)
        d.text((64,100),"Evidence is inspectable, not asserted.",font=F_H1,fill=PALE)
        terminal(d,(64,175,710,520),"PUBLIC REPOSITORY  /  EVIDENCE",[
            ("src/sae_qnx_probe.c",STEEL),
            ("tests/test_bridge.py",PALE),
            ("evidence/qcc-build-aarch64.log",PALE),
            ("evidence/qcc-build-x86_64.log",PALE),
            ("evidence/build-evidence-*.json",PALE),
            ("evidence/qnx-live-session-20261126.txt",GREEN),
            ("evidence/manifest.json",PALE),
            ("LICENSE  ·  MIT",GREEN)
        ],fs=F_MONO_SM)
        rounded(d,(760,175,1216,520),20,PANEL2,BORDER,2)
        d.text((800,210),"VERIFIED",font=F_MED,fill=GREEN)
        d.text((800,260),"QNX 8.0.0 x86_64 runtime",font=F_SMALL,fill=PALE)
        d.text((800,315),"NOT TESTED",font=F_MED,fill=(230,190,125))
        d.text((800,365),"AArch64 runtime execution",font=F_SMALL,fill=PALE)
        d.text((800,425),"NOT A SAFETY CERTIFICATION",font=F_SMALL,fill=RED)
        footer(d,"06","AArch64 runtime remains untested. The tool is not an ISO 26262 or IEC 61508 certification.")
    else:
        header(d,"Open source · reproducible engineering",7)
        d.text((64,155),"SAE QNX",font=F_TITLE,fill=PALE)
        d.text((64,225),"ASSURANCE BRIDGE",font=F_TITLE,fill=STEEL)
        d.text((70,330),"Source code  ·  build logs  ·  runtime evidence",font=F_H2,fill=PALE)
        rounded(d,(64,405,1216,515),20,PANEL2,BORDER,2)
        d.text((95,440),"github.com/pergolessi9-star/sae-qnx-assurance-bridge",font=F_MED,fill=STEEL)
        d.text((70,555),"MIT LICENSE",font=F_MED,fill=GREEN)
        d.text((1210,555),"REPRODUCIBLE  /  INSPECTABLE  /  ACCOUNTABLE",font=F_SMALL,fill=MUTED,anchor="ra")
        footer(d,"07","SAE QNX Assurance Bridge  ·  Prof. Manuel Gago Fernández")
    return im.convert("RGB")

# Render scene stills
scenes=[scene_image(i) for i in range(7)]
weights=[max(1,len(p.split())) for p in paragraphs]
total=sum(weights)
durations=[audio_duration*w/total for w in weights]
durations[-1]+=1.6
# Ensure each scene has enough visual hold
durations=[max(6.0,d) for d in durations]
scale=duration/sum(durations)
durations=[d*scale for d in durations]
fourcc=cv2.VideoWriter_fourcc(*"mp4v")
writer=cv2.VideoWriter(str(RAW),fourcc,FPS,(W,H))
if not writer.isOpened():
    raise RuntimeError("OpenCV could not open MP4 writer")
prev=None
for i,(im,sec) in enumerate(zip(scenes,durations)):
    frame=np.array(im)[:,:,::-1].copy()
    n=max(1,int(sec*FPS))
    fade=12
    for j in range(n):
        cur=frame.copy()
        # bottom progress rail
        progress=(sum(durations[:i])+j/FPS)/duration
        cv2.rectangle(cur,(64,H-18),(W-64,H-12),(44,62,77),-1)
        cv2.rectangle(cur,(64,H-18),(64+int((W-128)*progress),H-12),(125,174,204),-1)
        if prev is not None and j<fade:
            alpha=(j+1)/fade
            cur=cv2.addWeighted(cur,alpha,prev,1-alpha,0)
        writer.write(cur)
    prev=frame
writer.release()

# Mux voice; H.264 + AAC for YouTube-compatible MP4.
cmd=[FFMPEG,"-y","-i",str(RAW),"-i",str(AUDIO),"-c:v","libx264","-preset","medium","-crf","21",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",str(FINAL)]
run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
if run.returncode != 0:
    # Fallback to MPEG-4 Part 2 if this ffmpeg build lacks libx264.
    cmd=[FFMPEG,"-y","-i",str(RAW),"-i",str(AUDIO),"-c:v","mpeg4","-q:v","4",
         "-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",str(FINAL)]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# Probe duration and file properties
probe=subprocess.run([FFMPEG,"-i",str(FINAL),"-f","null","-"],capture_output=True,text=True)
m=re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)",probe.stderr)
if m:
    actual=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
else:
    actual=duration
if actual >= 180:
    raise RuntimeError(f"Video exceeds 3 minutes: {actual:.2f}s")
print(f"VIDEO={FINAL}")
print(f"DURATION_SECONDS={actual:.2f}")
print(f"AUDIO_VOICE=en-US-AvaNeural (female neural English)")
print(f"VIDEO_BYTES={FINAL.stat().st_size}")
print(f"RESOLUTION={W}x{H} FPS={FPS}")
print(f"SCRIPT={SCRIPT}")

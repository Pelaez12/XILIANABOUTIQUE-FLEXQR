import sys,json,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'.audio-tools'))
from faster_whisper import WhisperModel
import numpy as np
r=Path(__file__).resolve().parent
model=WhisperModel('small',device='cpu',compute_type='int8',download_root=str(r/'modelos-audio'))
results=[]
for hour in ['12.07.25','12.09.43','12.10.26','12.11.53','12.12.11']:
 f=Path('C:/Users/USER/Downloads')/f'WhatsApp Ptt 2026-10-11 at {hour} AM.ogg'
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-f','s16le','-ac','1','-ar','16000','pipe:1'])
 audio=np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
 segments,info=model.transcribe(audio,language='es',beam_size=5,vad_filter=True)
 text=' '.join(s.text.strip() for s in segments)
 results.append({'archivo':f.name,'texto':text});print(f.name, text,flush=True)
 (r/'feedback-audios-2026-10-11.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')

import pysubs2
import subprocess, re, json
from os import listdir

def run(cmd):
    return str(subprocess.check_output(cmd))

def formatTime(t): # t in millisecs, returns in format 00:01:02.500
    return '{0:02d}:{1:02d}:{2:02d}.{3:03d}'.format(t//(1000*60*60), (t//(1000*60))%60, (t//(1000))%60, t%1000)

data={}

for serie in listdir('./series'):
    data[serie]=[]
    run(["rm", "-rf", "temp"])
    run(["mkdir", "-p", "temp/utt/test/aac"])
    for video in listdir('./series/'+serie):
        filename='./series/'+serie+'/'+video
        tracks=run(["mkvmerge",  "--identify", filename])
        subtracks=re.findall(r'Track ID ([0-9]*): subtitles.*', tracks)
        audiotracks=re.findall(r'Track ID ([0-9]*): audio.*', tracks)
        if subtracks and audiotracks:
            run(["mkvextract",  filename, "tracks", audiotracks[0]+":temp/audio"])
            run(["mkvextract",  filename, "tracks", subtracks[0]+":temp/subs"])
            subs = pysubs2.load("temp/subs", encoding="utf-8")
            for line in subs:
                audioFilename=str(len(data[serie]))
                run(["mkdir", "-p", "temp/utt/test/aac/"+audioFilename+"/01dfn2spqyE"])
                run(["ffmpeg", "-loglevel", "quiet", "-i", "temp/audio", "-ss",  formatTime(line.start), "-to", formatTime(line.end), "-ar", "16000", "temp/utt/test/aac/"+audioFilename+"/01dfn2spqyE/"+audioFilename+".m4a"])
                data[serie].append({
                    'text':line.text,
                    'speaker':None
                    })
    run(["bash", "kaldi.sh"]) # Compute xvectors using Kaldi

    for line in open("temp/xvectors.txt", "r").readlines():
        audioFilename,vector=re.findall(r'([A-z0-9]*)  \[([^\]]*)\]', line)[0]
        data[serie][int(audioFilename)]["xvector"] = list(map(float, vector.strip().split(' ')))

open("data.json", "w+").write(json.dumps(data))


    #Apply clustering
    #Save all data
    #Get user input on chosen waifu
    #Train seq2seq nn

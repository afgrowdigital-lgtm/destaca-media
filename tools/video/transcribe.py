#!/usr/bin/env python3
"""Transcreve um vídeo (pt) com tempos por palavra -> JSON para o edit-video.js.

Uso: python3 tools/video/transcribe.py <video> <saida.json>

Na primeira execução descarrega o modelo Whisper small (CTranslate2 int8) a partir
do npm (o Hugging Face está bloqueado no ambiente) para ~/.cache/destaca-whisper.
Depois de gerar o JSON, REVÊ o texto: corrige grafia PT-PT, nomes (Destaca, Google)
e pontuação. Os tempos ficam; só se muda o campo "w".
"""
import hashlib, json, os, subprocess, sys

MODEL = os.path.expanduser("~/.cache/destaca-whisper")
PKG = "@skillninja/shortmovie-telop-model-p{}"


def ensure_model():
    if os.path.exists(os.path.join(MODEL, "model.bin")):
        return
    tmp = MODEL + "-npm"
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["npm", "i", "--ignore-scripts", "--silent", "--prefix", tmp]
                   + [PKG.format(i) for i in range(4)], check=True)
    base = os.path.join(tmp, "node_modules", "@skillninja", "shortmovie-telop-model-p{}")
    os.makedirs(MODEL, exist_ok=True)
    h = hashlib.sha256()
    with open(os.path.join(MODEL, "model.bin"), "wb") as out:
        for i in range(4):
            with open(os.path.join(base.format(i), f"model.bin.part{i}"), "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    out.write(chunk); h.update(chunk)
    expected = open(os.path.join(base.format(0), "model.sha256")).read().split()[0]
    if h.hexdigest() != expected:
        os.remove(os.path.join(MODEL, "model.bin"))
        sys.exit("checksum do modelo não confere")
    for f in ["config.json", "tokenizer.json", "vocabulary.json", "preprocessor_config.json"]:
        with open(os.path.join(base.format(0), f), "rb") as a, open(os.path.join(MODEL, f), "wb") as b:
            b.write(a.read())


def main(video, out):
    try:
        import faster_whisper  # noqa
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages",
                        "faster-whisper"], check=True)
    import numpy as np
    from faster_whisper import WhisperModel
    ensure_model()
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], check=True, capture_output=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, language="pt", word_timestamps=True,
                               initial_prompt="Português de Portugal. Destaca, Google, Instagram, site.")
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)}
             for s in segs for w in s.words if w.word.strip()]
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"words": words}, f, ensure_ascii=False, indent=1)
    print(" ".join(w["w"] for w in words))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])

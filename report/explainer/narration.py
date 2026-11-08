"""Generate narration clips for diageo_put_video.py with Chatterbox TTS.

Run with the separate venv (keeps PyTorch out of the global Python):
    ~/.venvs/chatterbox/bin/python report/explainer/narration.py
Writes report/explainer/audio/<scene>.wav. The video script reads these.
"""
from pathlib import Path

NARRATION = {
    "intro": "This is the Diageo put. It is a six billion euro debt that L.V.M.H. does not call debt.",
    "ownership": (
        "Diageo owns thirty-four percent of Moët Hennessy. L.V.M.H. owns the rest, and consolidates all of it. "
        "A contract from nineteen ninety-four gives Diageo a put option. "
        "Diageo can force L.V.M.H. to buy its stake, with six months' notice. "
        "The price is eighty percent of fair value. "
        "The accounting standard says: record this promise as a liability."
    ),
    "bookkeeping": (
        "First, L.V.M.H. removes Diageo's minority interest. "
        "Then it puts the difference into goodwill. "
        "Each year, the fair value changes. Where does the change go? "
        "L.V.M.H. puts it into goodwill. Not into profit. "
        "From twenty twenty-one to twenty twenty-five, the plug fell by almost nine billion euros. "
        "Profit did not change at all."
    ),
    "history": (
        "Here is the put, year by year. "
        "The blue part is Diageo's share of book equity. It stays flat. "
        "The orange part is the goodwill plug. It almost disappears."
    ),
    "fair_value": (
        "We can work backwards to the value that L.V.M.H. puts on Moët Hennessy. "
        "It fell from forty-seven billion euros to seventeen billion. "
        "That is a thirty billion euro fall, with no charge in the income statement. "
        "The cause is real. Cognac demand fell in the United States and in China."
    ),
    "net_debt": (
        "Is it material? Yes. "
        "Reported net debt is six point nine billion euros. "
        "Add the put, and net debt almost doubles, to thirteen point two billion. "
        "Diageo can ask for cash in six months. A buyer must treat it as debt."
    ),
    "profit": (
        "In September twenty twenty-six, the I.A.S.B. tentatively decided that these changes must go to profit or loss. "
        "If that rule applied before, profit would move a lot. "
        "Minus twenty percent in twenty twenty-one. Plus thirty-five percent in twenty twenty-four."
    ),
    "what_to_do": (
        "So, what should we do? Do not stop the deal. Change the price. "
        "Add the put to net debt. "
        "Use five to six billion euros as the minimum cost to own all of Moët Hennessy. "
        "Get the nineteen ninety-four agreement, and check the change of control terms. "
        "Value the drinks business with our own model. "
        "And remove put changes from covenants and earn-outs."
    ),
}

if __name__ == "__main__":
    import torch
    import torchaudio as ta
    from chatterbox.tts import ChatterboxTTS

    out = Path(__file__).parent / "audio"
    out.mkdir(exist_ok=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    # Chatterbox checkpoints were saved on CUDA; map them to the local device.
    _load = torch.load
    torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": torch.device(device)})
    model = ChatterboxTTS.from_pretrained(device=device)
    torch.manual_seed(7)
    for key, text in NARRATION.items():
        wav = model.generate(text, exaggeration=0.45, cfg_weight=0.45)
        ta.save(str(out / f"{key}.wav"), wav, model.sr, encoding="PCM_S", bits_per_sample=16)
        print(key, round(wav.shape[-1] / model.sr, 1), "s")

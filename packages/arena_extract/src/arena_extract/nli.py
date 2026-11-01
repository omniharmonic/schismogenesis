"""NLI entailment gate (08 §4.8). Needs the `nli` extra; runs on local hardware."""

from typing import Any


class NLIGate:
    MODEL = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"

    def __init__(self, entail_min: float = 0.80, contra_max: float = 0.50) -> None:
        import torch  # pyright: ignore[reportMissingImports]
        from transformers import (  # pyright: ignore[reportMissingImports]
            AutoModelForSequenceClassification,
            AutoTokenizer,
        )

        self.torch: Any = torch
        self.tok = AutoTokenizer.from_pretrained(self.MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL).eval()
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.model.to(self.device)
        labels = {v.lower(): k for k, v in self.model.config.id2label.items()}
        self.i_ent, self.i_con = labels["entailment"], labels["contradiction"]
        self.entail_min, self.contra_max = entail_min, contra_max

    def score(self, pairs: list[tuple[str, str]], batch_size: int = 16) -> list[dict[str, Any]]:
        out = []
        with self.torch.inference_mode():
            for k in range(0, len(pairs), batch_size):
                premises, hypotheses = zip(*pairs[k : k + batch_size], strict=True)
                encoded = self.tok(
                    list(premises), list(hypotheses), truncation="only_first", max_length=512,
                    padding=True, return_tensors="pt",
                ).to(self.device)  # fmt: skip
                for probabilities in self.model(**encoded).logits.softmax(-1).cpu():
                    ent, con = float(probabilities[self.i_ent]), float(probabilities[self.i_con])
                    label = (
                        "contradiction" if con >= self.contra_max
                        else "entailment" if ent >= self.entail_min
                        else "neutral"
                    )  # fmt: skip
                    out.append({"label": label, "entail": ent, "contra": con})
        return out

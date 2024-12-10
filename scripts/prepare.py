from collections.abc import Iterable
import json
from pathlib import Path
import random

from spacy.lang.en import English
from spacy.ml import Doc, Span
from spacy.tokens import DocBin
import typer


def prepare(
    raw_dataset_path: Path,
    train_dataset_path: Path,
    dev_dataset_path: Path,
    is_ner: bool = False,
    spans_key: str = 'sc',
    dev_ratio: float = 0.2,
    random_seed: int = 0,
) -> None:
    random.seed(random_seed)
    with open(raw_dataset_path) as raw_dataset:
        documents = tokenize_and_annotate(raw_dataset, is_ner, spans_key)
    dev_dataset_size = int(len(documents) * dev_ratio)
    random.shuffle(documents)
    DocBin(docs=documents[:dev_dataset_size]).to_disk(dev_dataset_path)
    DocBin(docs=documents[dev_dataset_size:]).to_disk(train_dataset_path)


def tokenize_and_annotate(raw_dataset: Iterable[str], is_ner: bool, spans_key: str) -> list[Doc]:
    documents = []
    nlp = English()
    for line in raw_dataset:
        entry = json.loads(line)
        doc = nlp.make_doc(entry['content'])
        entities = extract_entities(entry['annotation'])
        spans = build_spans(doc, entities)
        if is_ner:
            doc.ents = list(discard_overlapping_spans(spans))
        else:  # spancat
            doc.spans[spans_key] = list(spans)
        documents.append(doc)
    return documents


def extract_entities(annotations: Iterable[dict]) -> Iterable[dict]:
    return (
        {'label': label, **point}
        for annotation in annotations
        if (label := (annotation['label'] and annotation['label'][0]))
        if label != 'UNKNOWN'
        for point in annotation['points']
    )


def build_spans(doc: Doc, entities: Iterable[dict]) -> Iterable[Span]:
    return filter(None, (
        # mitigate inconsistencies:
        doc.char_span(entity['start'], entity['end'] + 1, entity['label'])
        or doc.char_span(entity['start'], entity['start'] + len(entity['text']) + 1, entity['label'])
        for entity in entities
    ))


def discard_overlapping_spans(spans: Iterable[Span]) -> Iterable[Span]:
    non_overlapping_spans: list[Span] = []
    for span in sorted(spans, key=len):
        if not any((
            span.start <= shorter_span.start <= span.end
            or span.start <= shorter_span.end <= span.end
            for shorter_span in non_overlapping_spans
        )):
            non_overlapping_spans.append(span)
    return non_overlapping_spans


if __name__ == '__main__':
    typer.run(prepare)

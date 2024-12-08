from collections.abc import Iterable
import json
from pathlib import Path
import random

from spacy.lang.en import English
from spacy.ml import Doc, Span
from spacy.tokens import DocBin
import typer

random.seed(0)


def prepare(
    raw_dataset_path: Path,
    training_dataset_path: Path,
    evaluation_dataset_path: Path,
    evaluation_ratio: float = 0.2,
) -> None:
    with open(raw_dataset_path) as raw_dataset:
        documents = tokenize_and_annotate(raw_dataset)
    evaluation_dataset_size = int(len(documents) * evaluation_ratio)
    random.shuffle(documents)
    DocBin(docs=documents[:evaluation_dataset_size]).to_disk(evaluation_dataset_path)
    DocBin(docs=documents[evaluation_dataset_size:]).to_disk(training_dataset_path)


def tokenize_and_annotate(raw_dataset: Iterable[str]) -> list[Doc]:
    documents = []
    nlp = English()
    for line in raw_dataset:
        entry = json.loads(line)
        doc = nlp.make_doc(entry['content'])
        entities = extract_entities(entry['annotation'])
        doc.ents = build_spans(doc, entities)
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


def build_spans(doc: Doc, entities: Iterable[dict]) -> list[Span]:
    return filter_spans([
        # mitigate inconsistencies:
        doc.char_span(entity['start'], entity['end'] + 1, entity['label'])
        or doc.char_span(entity['start'], entity['start'] + len(entity['text']) + 1, entity['label'])
        or doc.char_span(entity['end'] - len(entity['text']), entity['end'] + 1, entity['label'])
        for entity in entities
    ])


def filter_spans(spans: Iterable[Span | None]) -> list[Span]:
    # see https://github.com/explosion/spaCy/discussions/9993
    non_overlapping_spans: list[Span] = []
    for span in sorted(filter(None, spans), key=len):
        if not any([
            span.start <= shorter_span.start <= span.end
            or span.start <= shorter_span.end <= span.end
            for shorter_span in non_overlapping_spans
        ]):
            non_overlapping_spans.append(span)
    return non_overlapping_spans


if __name__ == '__main__':
    typer.run(prepare)

<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Resume Named Entity Recognition

An exploration project for the [Resume Entities for NER](https://www.kaggle.com/datasets/dataturks/resume-entities-for-ner) dataset.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `prepare_ner` | Prepare the train and dev datasets for NER |
| `prepare_spancat` | Prepare the train and dev datasets for SpanCat |
| `train_scratch_ner` | Train the scratch model for NER |
| `train_pretrained_sm_ner` | Train the pretrained small model for NER |
| `train_pretrained_md_ner` | Train the pretrained medium model for NER |
| `train_pretrained_lg_ner` | Train the pretrained large model for NER |
| `train_pretrained_trf_ner` | Train the pretrained transformer model for NER |
| `evaluate_scratch_ner` | Evaluate the scratch model for NER |
| `evaluate_pretrained_sm_ner` | Evaluate the pretrained small model for NER |
| `evaluate_pretrained_md_ner` | Evaluate the pretrained medium model for NER |
| `evaluate_pretrained_lg_ner` | Evaluate the pretrained large model for NER |
| `evaluate_pretrained_trf_ner` | Evaluate the pretrained transformer model for NER |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `prepare_ner` &rarr; `prepare_spancat` &rarr; `train_scratch_ner` &rarr; `train_pretrained_sm_ner` &rarr; `train_pretrained_md_ner` &rarr; `train_pretrained_lg_ner` &rarr; `train_pretrained_trf_ner` &rarr; `evaluate_scratch_ner` &rarr; `evaluate_pretrained_sm_ner` &rarr; `evaluate_pretrained_md_ner` &rarr; `evaluate_pretrained_lg_ner` &rarr; `evaluate_pretrained_trf_ner` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [`assets/dataset.jsonl`](assets/dataset.jsonl) | Local | Raw dataset from [Resume Entities for NER](https://www.kaggle.com/datasets/dataturks/resume-entities-for-ner) |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->

## Results

I successfully trained NER models:
- From scratch
- From [a small pre-trained from the SpaCy team](https://huggingface.co/spacy/en_core_web_sm)
- From [a medium pre-trained from the SpaCy team](https://huggingface.co/spacy/en_core_web_md)

These three models led me to a gorgeous accuracy of... 0%!

So I tried going bigger, by training [a large pre-trained from the SpaCy team](https://huggingface.co/spacy/en_core_web_lg),
as well as [their pre-trained transformer model](https://huggingface.co/spacy/en_core_web_trf).
However, the training processes crash during initialization, supposedly because my laptop does not have enough RAM...

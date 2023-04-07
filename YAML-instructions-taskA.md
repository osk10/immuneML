# YAML - Task A

The YAML specification defines which analysis should be performed by immuneML. It is defined under three main keywords:

- `definitions` - describing the settings of `datasets`, `encodings`, `ml_methods`, `preprocessing_sequences`, `reports`, `simulations` and other components
- `instructions` - describing the parameters of the analysis that will be performed and which of the analysis components (defined under `definitions`) will be used for this
- `output` - describing how to format the results of the analysis

The overall structure of the YAML specification is the following:

```yaml
definitions: # mandatory keyword
  datasets: # mandatory keyword
    my_dataset_1: # user-defined name of the dataset
      ... 
  encodings: # optional keyword - present if encodings are used
    my_encoding_1: # user-defined name of the encoding
      ... 
  ml_methods: # optional keyword - present if ML methods are used
    my_ml_method_1: # user-defined name of the ML method
			...
  preprocessing_sequences: # optional keyword - present if preprocessing sequences are used
    my_preprocessing: # user-defined name of the preprocessing sequence
			...
  reports: # optional keyword - present if reports are used
    my_report_1:
      ... 
instructions: # mandatory keyword - at least one instruction has to be specified
  my_instruction_1: # user-defined name of the instruction
    ... 
output: # how to present the result after running (the only valid option now)
  format: HTML
```

## Full example of YAML-specification

YAML-file example:

```yaml
definitions:
  datasets:
    my_dataset: # user-defined dataset name
      format: AIRR
      params:
        is_repertoire: true # we are importing a repertoire dataset
        path: /path/to/repertoires # path to the folder containing the repertoire .tsv files
        metadata_file: /path/to/metadata.csv

  encodings:
    my_kmer_frequency: # user-defined encoding name
      KmerFrequency: # encoding type
        k: 3 # encoding parameters

  ml_methods:
    my_method: SVM # user-defined ML model name: ML model type (no user-specified parameters)

  reports:
    my_coefficients: Coefficients # user-defined report name: report type (no user-specified parameters)

instructions:
  my_training_instruction: # user-defined instruction name
    type: TrainMLModel

    dataset: my_dataset # use the same dataset name as in definitions
    labels:
      - signal_disease # use a label available in the metadata.csv file

    settings: # which combinations of ML settings to run
      - encoding: my_kmer_frequency
        ml_method: my_method # ml_method named my_method, defined in the definiton-section

    assessment: # parameters in the assessment (outer) cross-validation loop
      reports: # plot the coefficients for the trained model
        models:
          - my_coefficients
      split_strategy: random # how to split the data - here: split randomly
      split_count: 1 # how many times (here once - just to train and test)
      training_percentage: 0.7 # use 70% of the data for training

    selection: # parameters in the selection (inner) cross-validation loop
      split_strategy: random
      split_count: 1
      training_percentage: 1 # use all data for training

    optimization_metric: balanced_accuracy # the metric to optimize during nested cross-validation when comparing multiple models
    metrics: # other metrics to compute for reference
      - auc
      - precision
      - recall

    number_of_processes: 4 # processes for parallelization
```
# YAML - Task B

The YAML specification defines which analysis should be performed by immuneML. It is defined under four main keywords:

- `definitions` - describing the settings of `datasets`, `encodings`, `ml_methods`, `preprocessing_sequences`, `reports`, `simulations` and other components
- `instructions` - describing the parameters of the analysis that will be performed and which of the analysis components (defined under `definitions`) will be used for this
- `output` - describing how to format the results of the analysis
- `tools` - describing the tools that should be used in the analysis.

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
tools: # optional keyword - present if tools are used
	my_ml_tool: # user-defined name of the tool
		type: MLMethodTool # type of tool (the only valid option now)
		params: # optional keyword - present if the tool requires params
		
```

## Defining a tool

Tools are defined under the “tool”-section. The name of the tool must be used to define that it will be used in the other sections of the YAML specification (see instructions and example below)

Instructions on how to specify tools in YAML specification:

1. Create a new key in the tool-section with an optional name.
    1. Add `path` to the location of the tool and connection script
    2. Add `type`, which is type of tool. Only valid option is `MLMethodTool`
    3. Optional: add `params`
2. In the definition-section
    1. Use the name of the tool and `MLMethodTool` to define that a tool will be used
3. In the instructions-section
    1. Use the name of the tool wherever the defined tool will be used

Simplified example: 

```yaml
definitions:
  ml_methods: 
    my_ml_tool: MLMethodTool # name of tool: MLMethodTool

instructions:
  settings:
    ml_method: my_ml_tool # ml_method: name of tool

tool:
  my_ml_tool: # user-defined name of the tool
    path: /path/to/tool/main.py # path to the connection script
    type: MLMethodTool # type of tool
    params: # optional parameters
```

## Full example of YAML-specification

YAML-file example with the use of tool. 

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
    my_method: MLMethodTool # tool-named my_method, defined in the tool-section

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
        ml_method: my_method # tool-named my_method, defined in the tool-section

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
tools:
  my_method: # user-defined tool-name. Use this name in the rest of the YAML-file where tool should be used
    path: /path/to/tool/main.py # path to the connection script
    type: MLMethodTool # type of the tool
```
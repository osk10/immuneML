# YAML - Task A
**For more in depth documentation:**
* https://docs.immuneml.uio.no/latest/specification.html?highlight=datasetexport#datasetexport
* https://docs.immuneml.uio.no/latest/tutorials/how_to_generate_a_random_repertoire_dataset.html?highlight=randomsequencedataset
* https://docs.immuneml.uio.no/latest/specification.html

The YAML specification defines which analysis should be performed by immuneML. It is defined under four main keywords:

- `definitions` - describing the settings of `datasets`, `encodings`, `ml_methods`, `preprocessing_sequences`, `reports`, `simulations` and other components
- `instructions` - describing the parameters of the analysis that will be performed and which of the analysis components (defined under `definitions`) will be used for this
- `output` - describing how to format the results of the analysis
- `tools` - describes the external tools that should be used 

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
      path: # path to the connection script / executable
      type: PreprocessorTool # type of tool (only PreprocessorTool and MLMethodTool is valid)
      params: # optional keyword - present if the tool requires params
```

## Full example of YAML-specification running preprocessing

YAML-file example with the use of a PreprocessorTool. This example shows how a user can create 
a RandomSequenceDataset, specify a preprocessor and define the instruction DatasetExport. 

```yaml
definitions:
  datasets:
    my_dataset:
      format: RandomSequenceDataset
      params:
        sequence_count: 5 # number of random sequences to generate
        length_probabilities:
          14: 0.8 # 80% of all generated sequences for all sequences will have length 14
          15: 0.2 # 20% of all generated sequences across all sequences will have length 15

  preprocessing_sequences: 
    my_preprocessing_seq: # User-defined name of the preprocessing sequence (may contain one or more preprocessings)
      - my_preprocessing_tool: ToolPreprocessor

  reports:
    simple_overview: SimpleDatasetOverview


instructions:
  my_dataset_export_instruction: # user-defined instruction name
    type: DatasetExport # which instruction to execute
    datasets: # list of datasets to export
    - my_dataset
    preprocessing_sequence: my_preprocessing_seq
    export_formats: # list of formats to export the datasets to
    - AIRR

tools:
  my_preprocessing_tool: # User defined tool name 
    type: PreprocessorTool # Type of tool 
    path: path/to/tool/script # Path to a file located in tool that immuneML communicates with
    params: # Optional parameters. Parameters are defined by the tools
      param_name1: value 

```
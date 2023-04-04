# Tool interface 

The tool interface is a new feature that enables the use of tools outside immuneML. 

For development, this feature allows developers to not have to work directly with immuneML source code 
when extending it. The motivation of the interface is to encapsulate immuneML. 


# YAML specification
## Structure

In immuneML, the yaml file is structured into three sections:

```yaml 
defintions: # describing the settings of datasets, encodings, ml_methods, preprocessing_sequences, reports, simulations and other components,

instructions: # describing the parameters of the analysis that will be performed and which of the analysis components (defined under definitions) will be used for this

output: # describing how to format the results of the analysis (currently, only HTML output is supported).
```


With the tool interface, we introduce a new section, giving the yaml file the new structure:

```yaml 
defintions:

instructions:

output:

tools:    
```

## Defining a tool
When defining a tool, you have to define your tool under the 'tool' section.
The tool also has to be included both in the definitions section and instructions

This section shows what is required to enter when defining a ML method tool. For further instructions 
on how to fill in the rest of the YAML file, refer to the 
[immuneML documentation](https://docs.immuneml.uio.no/latest/specification.html). 

```yaml
definitons:
  ml_methods: 
    my_ml_method: MLMethodTool #

instructions:
  settings:
    ml_method: my_ml_tool # Refer to ml method through the name of your tool 

tool:
  my_ml_tool: # Name of your tool
    path: "path to tool script"
    type: MLMethodTool
    params: # Optional parameters. These are defined by the tool

```

#!/usr/bin/env nextflow
params.source = "model.slim"

process hyperparameters {
    publishDir "./", mode: 'copy', saveAs: {"${params.config.split(".yaml")[0]}_parameters.csv"}
    input:
    path config
    output:
    path "parameters.csv"

    script:
    """
    parameters.py $config > parameters.csv
    """
}

process cli {
    input:
    path infile
    output:
    path "commands.txt"

    script:
    """
    cli_commands.py $infile > commands.txt
    """
}

process slim {
    // The tag should be the seed. For that, we need to parse the seed from the command
    // slim ... -s 1234 ...
    tag "s${command.split('-s ')[1].split(' ')[0]}"
    time '40min'
    errorStrategy 'ignore'
    input:
    tuple path(source), val(command)
    output:
    path "*.csv"

    script:
    """
    $command < $source > s${command.split('-s ')[1].split(' ')[0]}.csv 2> s${command.split('-s ')[1].split(' ')[0]}.log
    """
}

process analysis {
    tag "${input.baseName}"
    errorStrategy 'ignore'
    input:
    path input
    output:
    path "*_bin.csv"

    script:
    """
    analysis.py $input > ${input.baseName}_bin.csv
    """
}

process combineSimulations {
    publishDir "./", mode: 'copy', saveAs: {"${params.config.split(".yaml")[0]}_sims.csv"}
    output:
    input:
    path infiles
    output:
    path "*.csv"

    script:
    """
    combine.py $infiles > simulations.csv
    """
}

process plot {
    container 'rocker/tidyverse:latest'
    publishDir "./", mode: 'copy', saveAs: {"${params.config.split(".yaml")[0]}.pdf"}
    input:
    path data
    output:
    path "figure.pdf"

    script:
    """
    plot.R $data figure.pdf
    """
}

workflow {
    config = file("${params.config}")
    theta = hyperparameters(config)
    source = file("${params.source}")
    inputs = cli(theta)
         .splitText()
         .map {it -> [source, it.trim()]}
    output =  inputs | slim | analysis
    // First value is the theta, then the result of results
    theta.mix(output) | collect | combineSimulations | plot
}


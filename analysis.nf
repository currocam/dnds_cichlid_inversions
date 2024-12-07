#!/usr/bin/env nextflow
params.source = "model.slim"

process hyperparameters {
    publishDir "results", mode: 'copy'
    output:
    path "parameters.csv"

    script:
    """
    parameters.py > parameters.csv
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
    time '20min'
    errorStrategy 'ignore'
    fair true // Maintain the order of different simulations
    input:
    tuple path(source), val(command)
    output:
    path "*.vcf"

    script:
    """
    $command < $source > s${command.split('-s ')[1].split(' ')[0]}.vcf
    """
}

process analysis {
    tag "${vcf.baseName}"
    fair true // Maintain the order of different simulations
    input:
    path vcf
    output:
    path "*.csv"

    script:
    """
    analysis.py $vcf > ${vcf.baseName}.csv
    """
}

process combineSimulations {
    publishDir "results", mode: 'copy'
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
    publishDir "results", mode: 'copy'
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
    theta = hyperparameters()
    source = file("${params.source}")
    inputs = cli(theta)
         .splitText()
         .map {it -> [source, it.trim()]}
    results = inputs | slim | analysis
    // First value is the theta, then the result of results
    theta.mix(results) | collect | combineSimulations | plot
}


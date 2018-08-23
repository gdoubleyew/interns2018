import os
import glob
import toml
import argparse
import numpy as np
import pandas as pd


def parse_toml(configFile):
    if os.path.isfile(configFile):
        with open(configFile) as f:
            config = toml.load(f)
    else:
        raise FileNotFoundError(configFile + ' doesn\'t exist.')
    if config['transformations'] is None:
        raise ValueError("Config file requires a 'transformations' section")
    if config['transformations']['insert_header'] is None:
        raise ValueError("Config file requires a 'insert_header' command")
    return config


def transform(config, file, outputDir):
    # read in data file
    df = pd.read_csv(file, sep="\,|\s+|\t", engine='python', dtype=object)

    # insert headers row
    headers = config['transformations']['insert_header']
    assert headers is not None
    if len(headers) != len(df.columns):
        raise ValueError("Number of headers ({}) doesn't match number of columns ({}) for file {}".
                         format(len(headers), len(df.columns), file))
    df = pd.DataFrame(np.insert(df.values, 0, values=headers, axis=0), columns=headers)

    # reorder columns
    if config['transformations']['reorder_columns'] is not None:
        ordered_headers = [headers[i] for i in config['transformations']['reorder_columns']]
    else:
        # By default, keep all columns if 'reorder_columns' is empty
        ordered_headers = headers[:]
    df = df[ordered_headers]

    # search and replace text
    if config['transformations']['search_replace_cells'] is not None:
        df.replace(config['transformations']['search_replace_cells'], inplace=True)

    # write resulting data to a new output file
    outputFile = os.path.join(outputDir, os.path.basename(os.path.splitext(file)[0]) + '.tsv')
    df.to_csv(outputFile, index=False, sep='\t')
    return


def main():
    describe = 'Generate tab seperated files from whitespace separated or comma separated files'
    parser = argparse.ArgumentParser(description=describe)
    parser.add_argument('-c', '--configFile', default='config.toml', help='Configuration file to use')
    parser.add_argument('-i', '--inputDir', default='data/', help='Directory containing input TSV files')
    parser.add_argument('-o', '--outputDir', default='output/', help='Directory to write TSV results')

    args = parser.parse_args()

    config = parse_toml(args.configFile)
    if not os.path.exists(args.outputDir):
        os.makedirs(args.outputDir)

    errorCount = 0
    for file in glob.glob(os.path.join(os.path.dirname(args.inputDir), '*.txt')):
        try:
            transform(config, file, args.outputDir)
        except Exception as err:
            errorCount += 1
            print("Error performing transformations for file {}: {}".format(file, err))

    if errorCount == 0:
        print("Transformations were successful. See TSV files in directory {}".format(args.outputDir))
    else:
        print("Errors were encountered")


if __name__ == "__main__":
    main()

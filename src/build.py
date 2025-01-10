import parse_pcap
import build_markov
import tomllib
import glob
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    for tag in data['build']['tags']:
        print(tag)
        dir = "../pcap/types_dst/" + data['build'][tag]
        only_pcap = dir + "*.pcap"
        pcaps = glob.glob(only_pcap) #get pcap files

        out_file = data['build']['out_dir'] + "out_" + tag #output file for parsed pcap
        with open(out_file, 'w') as out:
            out.write("TAG: {}\n".format(tag))

        for f in pcaps:
            parse_pcap.parse_file(f, out_file) #parse pcap files

    for tag in data['build']['tags']: # for every malware build a Markov chain
        out_file = data['build']['out_dir'] + "out_" + tag #output file for transition matrix
        result = build_markov.markov(out_file)

        result_file = data['build']['result_dir'] + "result_" + tag
        #print(result)
        with open(result_file, 'w') as out:
            json.dump(result, out) #save transition matrix

if __name__ == '__main__':
    main()

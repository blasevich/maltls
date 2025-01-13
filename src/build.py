import parse_pcap
import build_markov
import tomllib
import glob
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    #for pcap_directory in data['build']['dirs']:
    for tag in data['build']['tags']:
        print("BUILD - parsing pcap files for {}".format(tag))
        dir = "../pcap/dst/" + data['build'][tag] #dirs = ["../pcap/dst/", "../pcap/src_dst/"]
        only_pcap = dir + "*.pcap"
        pcaps = glob.glob(only_pcap) #get pcap files

        out_file = data['build']['out_dir'] + "out_" + tag #output file for parsed pcap
        with open(out_file, 'w') as out:
            out.write("TAG: {}\n".format(tag))

        for f in pcaps:
            parse_pcap.parse_file(f, out_file) #parse pcap files

    for tag in data['build']['tags']: # for every malware build a Markov chain
        print("BUILD - creating Markov chain for {}".format(tag))
        out_file = data['build']['out_dir'] + "out_" + tag #output file for transition matrix
        result = build_markov.markov(out_file)

        result_file = data['build']['result_dir'] + "result_" + tag
        #print(result)
        with open(result_file, 'w') as out:
            json.dump(result, out) #save transition matrix

if __name__ == '__main__':
    print("BUILD - starting...")
    main()
    print("BUILD - done.")
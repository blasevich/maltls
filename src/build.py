import parse_pcap
import build_markov
import tomllib
import glob
import json
import argparse

def main(parse):
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    if parse:
        #for pcap_directory in data['build']['dirs']:
        for tag in data['build']['tags']:
            print("BUILD - parsing pcap files for {}".format(tag))

            dir = "../pcap/dst/" + data['build'][tag]
            ###dir = "../pcap/src_dst/" + data['build'][tag] #dirs = ["../pcap/dst/", "../pcap/src_dst/"]

            only_pcap = dir + "*.pcap"
            pcaps = glob.glob(only_pcap) #get pcap files

            out_file = data['build']['out_dir'] + "out_" + tag #output file for parsed pcap
            with open(out_file, 'w') as out:
                out.write("TAG: {}\n".format(tag))

            flows = 0 #number of flows
            for f in pcaps:
                flows = flows + parse_pcap.parse_file(f, out_file) #parse pcap files
            print("number of {} flows: {}\n".format(tag, flows))
                
    for tag in data['build']['tags']: # for every malware build a Markov chain
        print("BUILD - creating Markov chain for {}".format(tag))
        out_file = data['build']['out_dir'] + "out_" + tag #output file for transition matrix
        result = build_markov.markov(out_file)

        result_file = data['build']['result_dir'] + "result_" + tag
        #print(result)
        with open(result_file, 'w') as out:
            json.dump(result, out) #save transition matrix

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--buildonly", help="only build the model, do not parse files", action="store_true")
    args = parser.parse_args()

    parse_files = True

    if args.buildonly:
        parse_files = False        

    print("BUILD - starting...")
    main(parse_files)
    print("BUILD - done.")

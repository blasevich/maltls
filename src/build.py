import parse_pcap
import build_markov
import tomllib
import glob
import json
import argparse

def main(parse, mode, server_only):

    if server_only:
        sub_dir = mode + "/dst/"
    else:
        sub_dir = mode + "/src_dst/"

    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    if parse:
        for tag in data['build']['tags']:
            print("BUILD - parsing pcap files for {}".format(tag))

            if server_only:
                dir = "../pcap/dst/" + data['build'][tag]
            else:
                dir = "../pcap/src_dst/" + data['build'][tag]

            only_pcap = dir + "*.pcap"
            pcaps = glob.glob(only_pcap) #get pcap files

            out_file = data['build']['out_dir'] + sub_dir + "out_" + tag #output file for parsed pcap
            with open(out_file, 'w') as out:
                out.write("TAG: {}\n".format(tag))

            flows = 0 #number of flows
            for f in pcaps:
                flows = flows + parse_pcap.parse_file(f, out_file, mode) #parse pcap files
            print("number of {} flows: {}\n".format(tag, flows))
                
    for tag in data['build']['tags']: # for every malware build a Markov chain
        print("BUILD - creating Markov chain for {}".format(tag))
        out_file = data['build']['out_dir'] + sub_dir + "out_" + tag #output file for transition matrix
        result = build_markov.markov(out_file)

        result_file = data['build']['results_dir'] + sub_dir + "result_" + tag
        #print(result)
        with open(result_file, 'w') as out:
            json.dump(result, out) #save transition matrix

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--buildonly", action="store_true", help="only build the model, do not parse files")
    parser.add_argument("mode", choices=['type', 'length'], help="choose parse mode")
    parser.add_argument("--serveronly", action="store_true", help="only consider packets coming from server")
    args = parser.parse_args()

    parse_files = True
    server_only = False

    if args.buildonly:
        parse_files = False

    if args.serveronly:
        server_only = True

    print("BUILD - starting...")

    print(" server only: {}".format(server_only))
    print(" mode: {}".format(args.mode))

    main(parse_files, args.mode, server_only)

    print("BUILD - done.")

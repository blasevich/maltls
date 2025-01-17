import get_probability
import parse_pcap
import tomllib
import glob
import json
import argparse

def main(parse, mode, server_only):

    MAX = ['apply']['max_length']
    MIN = ['apply']['min_length']

    if server_only:
        sub_dir = mode + "/dst/"
    else:
        sub_dir = mode + "/src_dst/"

    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    D = {}

    for _tag in data['apply']["tags"]:

        if server_only:
            dir = "../pcap/dst/" + data['apply'][_tag] #where to find pcap files
        else:
            dir = "../pcap/src_dst/" + data['apply'][_tag]

        only_pcap = dir + "*.pcap"
        pcaps = glob.glob(only_pcap)

        result_dir = data['apply']['results_dir'] + sub_dir

        #parse pcap
        for f in pcaps:
            name = f.split("/")[-1].split(".")[0]
            #print(name)
            file_out = data['apply']['out_dir'] + sub_dir + "parsed_" + name # will contain parsed pcap

            if parse:
                with open(file_out, 'w') as out:
                    out.write("TAG: {}\n".format(name))
                parse_pcap.parse_file(f, file_out, mode)

            D[name] = {}

            result_file = result_dir + "result_" + name
            with open(result_file, 'w') as result:
                result.write("{}\n".format(name))

                for tag in data['apply']["tags"]:
                    if tag != "none": #test !
                        result.write("{}\n".format(tag))
                        markov = data['build']['results_dir'] + sub_dir + "result_" + tag #retrieve transition matrix
                        with open(markov, 'r') as f:
                            M = json.load(f)
                    
                        with open(file_out, 'r') as fo:
                            for s in fo.readlines():
                                if not s.startswith('stream') and not s.startswith('TAG') and not s.startswith('\n'):
                                    x = s.split()
                                    l = len(x)
                                    if l>=MIN and l<=MAX: # if len sequence <min or >max => dont consider this flow
                                        p = get_probability.prob(M[0], M[1], M[2], x)
                                        print("{}: {}".format(x, p))
                                        result.write("{} {}\n".format(x, p)) #write tls sequence + probability

                                        D[name][stream_number]["sequence"] = x
                                        D[name][stream_number][tag] = p
                                elif s.startswith('stream'):
                                    print("{}".format(s), end=" ")
                                    result.write("{}".format(s))

                                    x = s.split(':')
                                    stream_number = x[1].strip()
                                    if stream_number not in D[name].keys():
                                        D[name][stream_number] = {}

    #print(D)
    result_file = data['apply']['results_dir'] + sub_dir + "out"
    with open(result_file, 'w') as out:
            json.dump(D, out)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--applyonly", action="store_true", help="only apply the model, do not parse files")
    parser.add_argument("mode", choices=['type', 'length'], help="choose parse mode")
    parser.add_argument("--serveronly", action="store_true", help="only consider packets coming from server")
    args = parser.parse_args()

    parse_files = True
    server_only = False

    if args.applyonly:
        parse_files = False

    if args.serveronly:
        server_only = True

    print("APPLY - starting...")

    print(" server only: {}".format(server_only))
    print(" mode: {}".format(args.mode))

    main(parse_files, args.mode, server_only)

    print("APPLY - done.")

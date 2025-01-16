import get_probability
import parse_pcap
import tomllib
import glob
import json
import argparse

def main(parse):
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    D = {}

    for _tag in data['apply']["tags"]:

        dir = "../pcap/dst/" + data['apply'][_tag] #where to find pcap files
        ###dir = "../pcap/src_dst/" + data['apply'][_tag] ### dirs = ["../pcap/dst/", "../pcap/src_dst/"]

        only_pcap = dir + "*.pcap"
        pcaps = glob.glob(only_pcap)

        result_dir = data['apply']['results_dir']

        #parse pcap
        for f in pcaps:
            name = f.split("/")[-1].split(".")[0]
            #print(name)
            file_out = data['apply']['out_dir'] + "parsed_" + name # will contain parsed pcap

            if parse:
                with open(file_out, 'w') as out:
                    out.write("TAG: {}\n".format(name))
                parse_pcap.parse_file(f, file_out)

            D[name] = {}

            result_file = result_dir + "result_" + name
            with open(result_file, 'w') as result:
                result.write("{}\n".format(name))

                for tag in data['apply']["tags"]:
                    if tag != "none": #test !
                        result.write("{}\n".format(tag))
                        markov = data['build']['result_dir'] + "result_" + tag #retrieve transition matrix
                        with open(markov, 'r') as f:
                            M = json.load(f)
                    
                        with open(file_out, 'r') as fo:
                            for s in fo.readlines():
                                if not s.startswith('stream') and not s.startswith('TAG') and not s.startswith('\n'):
                                    x = s.split()
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
    result_file = data['apply']['results_file']
    with open(result_file, 'w') as out:
            json.dump(D, out)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--applyonly", help="only apply the model, do not parse files", action="store_true")
    args = parser.parse_args()

    parse_files = True

    if args.applyonly:
        parse_files = False

    print("APPLY - starting...")        
    main(parse_files)
    print("APPLY - done.")

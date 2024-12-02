import get_probability
import parse_pcap
import tomllib
import glob
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    #get pcap from config file *OK*
    dir = data['apply']['dir'] #where to find pcap files
    only_pcap = dir + "*.pcap" #dir + "/" + "*.pcap"
    pcaps = glob.glob(only_pcap)

    result_dir = data['apply']['results_out']

    #parse pcap
    filter = "tls.handshake.type eq 1"
    for f in pcaps:
        #print("\n{}".format(f))
        name = f.split("/")[-1].split(".")[0]
        #print(name)
        file_out = data['apply']['out_dir'] + "parsed_" + name ### will contain parsed pcap
        with open(file_out, 'w') as out:
            out.write("TAG: {}\n".format(name))
        parse_pcap.parse_file(f, file_out, filter)

        result_file = result_dir + "result_" + name
        with open(result_file, 'w') as result:
            result.write("{}\n".format(name))
            for tag in data['apply']["tags"]:
                result.write("{}\n".format(tag))
                #retrieve transition matrix
                markov = data['build']['result_dir'] + "result_" + tag
                with open(markov, 'r') as f:
                    M = json.load(f)
                
                with open(file_out, 'r') as fo:
                    for s in fo.readlines():
                        if not s.startswith('stream') and not s.startswith('TAG') and not s.startswith('\n'):
                            x = s.split()
                            p = get_probability.prob(M[0], M[1], M[2], x)
                            print("{}: {}".format(x, p))
                            result.write("{} {}\n".format(x, p)) #write tls sequence + probability
                        elif s.startswith('stream'):
                            print("{}".format(s), end=" ")
                            result.write("{}".format(s))

if __name__ == '__main__':
    main()

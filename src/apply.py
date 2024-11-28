import get_probability
import parse_pcap
import tomllib
import glob
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    dir = data['apply']['dir']
    only_pcap = dir + "*.pcap" #dir + "/" + "*.pcap"
    pcaps = glob.glob(only_pcap)

    #get pcap > from config file? *OK*

    filter = "tls.handshake.type eq 1"
    #filter = 'tls.handshake.type eq 1 and not (tls.handshake.extensions_server_name matches ".*.microsoft.com|.*.msedge.net|.*.xboxlive.com|.*.bing.com|.*.live.com|.*.windows.com")'
    file_out = "test"

    with open(file_out, 'w') as out:
            out.write("TAG: {}\n".format(file_out))
    #parse pcap
    for f in pcaps:
        print(f)
        parse_pcap.parse_file(f, file_out, filter)

    #retrieve transition matrix > from where build_markov has saved it? *ok*
        for tag in data['apply']["tags"]:
            #print(tag)
            markov = "result_" + tag
            with open(markov, 'r') as f:
                M = json.load(f)

            with open(file_out, 'r') as fo:
                for s in fo.readlines():
    #call get probability
                    if not s.startswith('stream') and not s.startswith('TAG') and not s.startswith('\n'):
                        x = s.split()
                        p = get_probability.prob(M[0], M[1], M[2], x)
                        print(x)
                        print(p)
                    else:
                        print(s, end=" ")

if __name__ == '__main__':
    main()
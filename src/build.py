import parse_pcap
import build_markov
import tomllib
import glob
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    #out_dir = data['build']['']

    #get pcaps > from config file ?? *OK*
    #parse pcaps > parse_pcap ? *OK*
    filter = 'tls.handshake.type eq 1 and not (tls.handshake.extensions_server_name matches ".*.microsoft.com|.*.msedge.net|.*.xboxlive.com|.*.bing.com|.*.live.com|.*.windows.com")' ### check !!!

    for tag in data['build']['tags']:
        print(tag)
        dir = data['build'][tag]
        #print(dir)
        only_pcap = dir + "*.pcap" #dir + "/" + "*.pcap"
        pcaps = glob.glob(only_pcap)

        #handle tag here: create, write to out file...

        out_file = "out_" + tag
        with open(out_file, 'w') as out:
            out.write("TAG: {}\n".format(tag))

        for f in pcaps:
            parse_pcap.parse_file(f, out_file, filter)

    #build transition matrix > build_markov *ok*
    #save transition matrix to file *ok*
    for tag in data['build']['tags']:
        out_file = "out_" + tag
        result = build_markov.markov(out_file)

        result_file = "result_" + tag
        #print(result)
        with open(result_file, 'w') as out:
            json.dump(result, out)


if __name__ == '__main__':
    main()

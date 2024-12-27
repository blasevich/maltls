import parse_pcap
import build_markov
import tomllib
import glob
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    #get pcaps from config file *OK*
    #parse pcaps *OK*
    #filter = 'tls.handshake.type eq 1'

    for tag in data['build']['tags']:
        print(tag)
        dir = data['build'][tag]
        only_pcap = dir + "*.pcap" #dir + "/" + "*.pcap"
        pcaps = glob.glob(only_pcap)

        out_file = data['build']['out_dir'] + "out_" + tag #parsed pcap
        with open(out_file, 'w') as out:
            out.write("TAG: {}\n".format(tag))

        for f in pcaps:
            parse_pcap.parse_file(f, out_file)

    #build transition matrix *ok*
    #save transition matrix to file *ok*
    for tag in data['build']['tags']:
        out_file = data['build']['out_dir'] + "out_" + tag #transition matrix
        result = build_markov.markov(out_file)

        result_file = data['build']['result_dir'] + "result_" + tag
        #print(result)
        with open(result_file, 'w') as out:
            json.dump(result, out)


if __name__ == '__main__':
    main()

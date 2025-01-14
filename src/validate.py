import tomllib
import json

D = {}

def find_tag(str, tags): # find a specific tag in a string
    found = 0
    i = 0
    while not found and i<len(tags):
        if tags[i] in str:
            found = 1
            tag = tags[i]
        i += 1

    return tag

def fun(tag, dict, file, out, threshold):
    sequences = 0

    for stream in dict:
        #print(stream)
        D[tag]['num_sequences'] += 1 # keep track of the number of tls content type sequences

        dict[stream].pop('sequence')
        sequences += 1

        print(dict[stream])
        m = max(zip(dict[stream].values(), dict[stream].keys()))
        print(m)

        if m[0] <= threshold:
            print("classified as: NONE.", end=" ")
            out.write("{} {} {} {} ".format(file, stream, dict[stream], "NONE"))
            if "NONE" in file:
                print("OK")
                out.write("OK\n")
            else:
                print("NOPE")
                out.write("NOPE\n")
        else:
            print("classified as: {}.".format(m[1]), end=" ")
            out.write("{} {} {} {} ".format(file, stream, dict[stream], m[1])) 
            #20211013_dridex 3 {'dridex': 0.057692307692307696, 'trickbot': 0.05589827058997696} dridex OK
            if m[1] in file:
                print("OK")
                D[tag]['true'] += 1
                out.write("OK\n")
            else:
                print("NOPE")
                D[tag]['false'] += 1
                out.write("NOPE\n")

    return sequences

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)
    tags = data['validate']["tags"]

    for tag in tags:
        D[tag] = {}
        D[tag]['true'] = 0
        D[tag]['false'] = 0
        D[tag]['num_sequences'] = 0
    
    #retrieve apply results
    apply_results = data['apply']['results_file']
    with open(apply_results, 'r') as f:
        R = json.load(f)

    results_file_all = data['validate']['results_file_all']
    threshold = data['threshold']

    sequences = 0 #double check number of sequences

    with open(results_file_all, 'w') as out:
        for file in R:
            print(file)
            sequences = sequences + fun(find_tag(file, tags), R[file], file, out, threshold)

    print(D)
    print("\nnumber of sequences: {}".format(sequences))

    results_file_dict = data['validate']['results_file_dict']
    with open(results_file_dict, 'w') as out:
        json.dump(D, out)
            

if __name__ == '__main__':
    main()

import tomllib
import json
import argparse

D = {}

def find_tag(str, tags): # find a specific tag in a string
    found = False
    i = 0
    l = len(tags)
    while not found and i<l:
        if tags[i] in str:
            found = True
            tag = tags[i]
        i += 1

    return tag

def fun(tag, dict, file, out, threshold, max_length, min_length):
    sequences = 0
    actual_sequences = 0

    for stream in dict:
        #print(stream)
        if 'sequence' in dict[stream].keys():
            length = len(dict[stream]['sequence'])
            sequences += 1

            if length>=min_length and length<=max_length: # if len sequence <min or >max => dont consider this flow
                D[tag]['num_sequences'] += 1
                actual_sequences += 1
                #print(dict[stream]['sequence'])
                dict[stream].pop('sequence')

                #print(dict[stream])
                m = max(zip(dict[stream].values(), dict[stream].keys()))
                #print(m)

                if m[0] <= threshold:
                    #print("classified as: none.", end=" ")
                    out.write("{} {} {} {} ".format(file, stream, dict[stream], "none"))
                    if "none" in file:
                        #print("OK")
                        out.write("OK\n")
                        D[tag]['true'] += 1
                    else:
                        #print("NOPE")
                        D[tag]['false'] += 1
                        out.write("NOPE\n")
                else:
                    #print("classified as: {}.".format(m[1]), end=" ")
                    out.write("{} {} {} {} ".format(file, stream, dict[stream], m[1])) 
                    if m[1] in file:
                        #print("OK")
                        D[tag]['true'] += 1
                        out.write("OK\n")
                    else:
                        #print("NOPE")
                        D[tag]['false'] += 1
                        out.write("NOPE\n")

    return actual_sequences

def main(mode, server_only, *args):
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
    # apply_results = data['apply']['results_file']
    if server_only:
        apply_results = data['apply']['results_dir'] + mode + "/dst/" + "out"
        sub_dir = mode + "/dst/"
    else:
        apply_results = data['apply']['results_dir'] + mode + "/src_dst/" + "out"
        sub_dir = mode + "/src_dst/"

    with open(apply_results, 'r') as f:
        R = json.load(f)

    results_file_all = data['validate']['results_dir'] + sub_dir + "validate_out_all"
    threshold = data['validate']['threshold']

    if args:
        MAX = args[0]
        MIN = args[0]
    else:
        MAX = data['validate']['max_length']
        MIN = data['validate']['min_length']

    sequences = 0 #double check number of sequences

    with open(results_file_all, 'w') as out:
        for file in R:
            #print("{}".format(file), end=" ")
            sequences = sequences + fun(find_tag(file, tags), R[file], file, out, threshold, MAX, MIN)

    print(" result: {}".format(D))
    print(" number of sequences: {}".format(sequences))

    #(micro F1 score) %(TP/(TP+1/2(FP+FN))), FP==FN==F => (TP/(TP+F))
    recall_mean = 0
    all_true = 0
    all_false = 0
    for tag in tags:
        recall = D[tag]['true']/(D[tag]['true'] + D[tag]['false'])
        recall_mean = recall_mean + recall

        all_true = all_true + D[tag]['true']
        all_false = all_false + D[tag]['false']

    micro_f1 = all_true/(all_true + all_false)
    recall_mean = recall_mean/5

    print("recall mean: {}, micro F1 score: {}".format(recall_mean, micro_f1))

    results_file_dict = data['validate']['results_dir'] + sub_dir + "validate_out_dict"
    with open(results_file_dict, 'w') as out:
        json.dump(D, out)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveronly", action="store_true", help="only consider packets coming from server")
    parser.add_argument("mode", choices=['type', 'length'], help="choose parse mode")
    parser.add_argument('-l','--length', type=int, help="flow length")
    args = parser.parse_args()

    server_only = False
    if args.serveronly:
        server_only = True

    print("VALIDATE - starting...")
    print(" server only: {}".format(server_only))
    print(" mode: {}".format(args.mode))
    
    if args.length:
        print(" length: {}".format(args.length))
        main(args.mode, server_only, args.length)
    else:
        main(args.mode, server_only)
    
    print("VALIDATE - done")

import tomllib
import json

D = {}

def find_tag(str, tags):
    found = 0
    i = 0
    while not found and i<len(tags):
        if tags[i] in str:
            found = 1
            tag = tags[i]
        i += 1

    return tag

def fun(tag, dict, file):
    for stream in dict:
        print(stream)
        D[tag]['num_sequences'] += 1

        dict[stream].pop('sequence')
        print(dict[stream].items())
        m = max(zip(dict[stream].values(), dict[stream].keys()))
        print(m)

        if m[1] in file:
            print("OK")
            D[tag]['true'] += 1
        else:
            print("NOPE")
            D[tag]['false'] += 1

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)
    tags = data['apply']["tags"]

    for tag in tags:
        D[tag] = {}
        D[tag]['true'] = 0
        D[tag]['false'] = 0
        D[tag]['num_sequences'] = 0
    
    #retrieve apply results
    apply_results = data['apply']['results_file']
    with open(apply_results, 'r') as f:
        R = json.load(f)

    for file in R:
        print(file)
        fun(find_tag(file, tags), R[file], file)

    print(D)

    results_file = data['validate']['results_file']
    with open(results_file, 'w') as out:
        json.dump(D, out)
            

if __name__ == '__main__':
    main()

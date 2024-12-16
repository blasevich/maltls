import tomllib
import json

def main():
    config_file = "../maltls.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)
    tags = data['apply']["tags"]
    
    #retrieve apply results
    apply_results = data['apply']['results_file']
    with open(apply_results, 'r') as f:
        R = json.load(f)

    true = 0
    false = 0

    for file in R:
        print(file)
        for stream in R[file]:
            print(stream)
            for tag in tags:
                print("{}: {}".format(tag, R[file][stream][tag]))
            R[file][stream].pop("sequence")
            m = max(zip(R[file][stream].values(), R[file][stream].keys()))
            print(m)
            if m[1] in file:
                print("OK")
                true += 1
            else:
                print("NOPE")
                false += 1
            
    print("true: {}, false: {}".format(true, false))


if __name__ == '__main__':
    main()


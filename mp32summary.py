import openai
import subprocess
import argparse
import json

# create an argument parser object
parser = argparse.ArgumentParser(description='Simple converter mp3/mp4 (Japanese) to summary')

# add arguments
parser.add_argument('input_mp', type=str, help='mp3 or mp4 in Japanese')
#parser.add_argument('out_json', type=str, help='output file (json)')

# parse the arguments
args = parser.parse_args()

# access the arguments
#print('arg1:', args.input_mp)
#print('arg2:', args.out_json)


#command = f"assemblyai transcribe {args.input_mp} --language_code ja --json > {args.out_json}"
command = ["assemblyai", "transcribe", args.input_mp, "--language_code", "ja", "--json"]
json_str = subprocess.run(command, capture_output=True)
#json_open = open(args.out_json, 'r')
json_load = json.loads(json_str.stdout)
print("mp3 to text (by assemblyai 1.17):")
print(json_load["text"])
print()

print("Summary (by chatGPT3.5):")
res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "以下の日本語の誤字脱字や句読点を推測して修正して、重要な点を箇条書きにして要約して下さい。修正後の文章は表示しないでください。\n\n" + json_load["text"]}
    ]
)

print(res["choices"][0]["message"]["content"])




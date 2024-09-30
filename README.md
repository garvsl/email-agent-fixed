# email-agent

goes through unread emails and prepares draft replies based on the history and prompt.

can do for incoming emails dynamically if time function is implemented.

run locally via llama-3b quantized to 4_k_M.

edit prompt as desired.

can finetune on emails instead of prompt based, which would have better accurcy.

setup u need to setup google oauth in order to gain access to ur account then insert ur email and access_token in main.py then u can download the model and quantize it or get it straight from hf, change app.py and response.py to ensure they have that model path correct then run llama-cpp-python server and run teh main.py

u could streamline this and have it all in one file for ease and if desired

# How to run

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt `

open a terminal

`python3 -m llama_cpp.server --model ./meta-llama-3_2-1B-instruct-Q8_0.gguf  --n
_gpu_layers 1`

open a seperate terminal

`source venv/bin/activate`

open main.py file and put access_token and email in

python3 main.py

# SETUP access token google oauth

You'll need to have registered with Google as an OAuth
application and obtained an OAuth client ID and client secret.
See https://developers.google.com/identity/protocols/OAuth2 for instructions on
registering and for documentation of the APIs invoked by this code.

NOTE: The OAuth2 OOB flow isn't a thing anymore. You will need to set the
application type to "Web application" and then add https://oauth2.dance/ as an
authorised redirect URI. This is necessary for seeing the authorisation code on
a page in your browser.

1. The first mode is used to generate and authorize an OAuth2 token, the
   first step in logging in via OAuth2.

python3 -m oauth2 --user=xxx@gmail.com \
 --client_id=1038[...].apps.googleusercontent.com \
 --client_secret=VWFn8LIKAMC-MsjBMhJeOplZ \
 --generate_oauth2_token

The script will converse with Google and generate an oauth request
token, then present you with a URL you should visit in your browser to
authorize the token. Once you get the verification code from the Google
website, enter it into the script to get your OAuth access token. The output
from this command will contain the access token, a refresh token, and some
metadata about the tokens. The access token can be used until it expires, and
the refresh token lasts indefinitely, so you should record these values for
reuse.

Put this access token in main.py along with emal

# SETUP for llama3.2 3b instruct

## env

`python3 -m venv venv
source venv/bin/activate` (or activate.fish)

## pytorch/hf installation

`pip install transformers 'transformers[torch]' tiktoken blobfile sentencepiece`

## llama-cpp-python installation (used as api/server)

### Set these before pip installing llama-cpp-python

- config based on mac os

`export CMAKE_ARGS="-DLLAMA_METAL=on"`

`export FORCE_CMAKE=1`

pip install -U llama-cpp-python --no-cache-dir

pip install 'llama-cpp-python[server]'

## download model

### option 1 easier: download model from hf

https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

git clone it after approval

### option 2: download model via site

https://llama.meta.com/llama-downloads/

#### convert to hf

- as llama is used we are converting based on that
- change python version dependent
- change model params dependent
- change input dir dependent

#### read the file in hf/transformers as needed

ensure latest version of transformers with llama 3.2 support is there

`python3 ./venv/lib/python3.12/site-packages/transformers/models/llama/convert_llama_weights_to_hf.py --input_dir ./Meta-Llama-3.2-3B-Instruct/ --model_size 3B --output_dir Llama-3.2-3B-Instruct --llama_version 3.2 --instruct`

## download llama.cpp

`git clone https://github.com/ggerganov/llama.cpp.git`

## build llama.cpp

`brew install make` if needed

`make -C llama.cpp/`

## convert to gguf

##### change filenames as needd

`python3 ./llama.cpp/convert_hf_to_gguf.py ./Llama-3.2-3B-Instruct --outtype f32 --outfile meta-llama-3_2-3B-instruct.gguf`

## Quantize (if desired)

#### make model smaller in exchange for accuracy loss, changes bit type

##### Using Q4_K_M below

`./llama.cpp/llama-quantize meta-llama-3_2-3B-instruct.gguf meta-llama-3_2-3B-instruct-Q4_K_M.gguf Q4_K_M`

## llama.cpp python server

remove gpu if using cpu

`export MODEL=''` enter model (i.e. meta-llama-3_2-3B-instruct.gguf)

in one terminal run to get server

`python3 -m llama_cpp.server --model $MODEL  --n_gpu_layers 1  `

in another terminal run to prompt the model

`python3 app.py`

instead of ^ run altogethr via

`python3 main.py`

## for performacne use conda for macos instead of venv

`brew install wget`

`wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
`

`bash Miniforge3-MacOSX-arm64.sh`

### create conda environemtn

conda create -n llama python=3.12.3

conda activate llama

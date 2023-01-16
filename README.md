# MyQ Lambda

A web app that uses AWS lambda to open/close a MyQ garage door opener.

## Setup up deps for Lambda
We need to create a Lambda "Layer" to house all the dependencies. 

Create a requirements.txt file with:
```requirements.txt
aiohttp
multidict
pymyq
```

Then combine it together in a folder:
```
pip3 install -r requirements.txt --target=/Users/musson/Downloads/lambdamyq_deps/package.zip
```

Make sure you have the contents in a "python" folder.

Compress it into package.zip.

Then upload this AWS Lambda under "Layers". Add this layer to the function.
mkdir deployment
cp -R src/* deployment/
pip install -t ./deployment/ -r requirements.txt
cd deployment
7z a ../SeleniumScraper.zip *
aws lambda update-function-code --function-name arn:aws:lambda:us-east-1:667043222635:function:webscraper-lambda  --zip-file fileb://SeleniumScraper.zip
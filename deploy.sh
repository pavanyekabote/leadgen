mkdir deployment
cp -R src/* deployment/
pip install -t ./deployment/ -r requirements.txt
cd deployment
7z a ../SeleniumScraper *

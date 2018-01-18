# coding=utf-8


from flask import Flask, request
from flask import render_template
from requestium import Session, Keys


app = Flask(__name__)

s = Session(webdriver_path='./../chromedriver/chromedriver.exe', browser='chrome', default_timeout=15)

def get_content(url):
    s.driver.get(url)
    try:
        return s.driver.find_element_by_tag_name('html').text
    except BaseException as ex:
        return s.driver.page_source

@app.route("/",  methods=['POST'])
def home():
    if request.method == 'POST':
        print(request.data.decode('utf-8'))
        return get_content(request.data.decode('utf-8'))
    else:
        return "no url specified"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10032)
    pass
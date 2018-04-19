from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/<string:index>/', methods=['GET','POST'])
def my_form_post(index):
    return render_template('%s.html' % index)

if __name__ == "__main__":
    app.run(debug=True)
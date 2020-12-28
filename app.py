from pyimagesearch.covid_simulation import SingleCovidSimulator
from flask import Response
from flask import Flask
from flask import render_template
import cv2
import os

outputFrame = None
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")
def generate():
	global outputFrame
	cs = SingleCovidSimulator(rVals=(1.1, 1.4))
	while True:
		outputFrame = cs.read().copy()
		cs.update()
		if outputFrame is None:
			continue
		else:
			ret, buffer = cv2.imencode('.jpg', outputFrame)
			frame = buffer.tobytes()
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True,host='0.0.0.0', port=port)
	# app.run()
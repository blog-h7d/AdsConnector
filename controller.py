import quart

app = quart.Quart(__name__)
app.secret_key = "AppForPyADS_ChangeForUsage"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

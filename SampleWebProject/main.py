from Website import create_app
app = create_app()

if __name__ == '__main__':
    #only if we run the main.py then the application will run
    app.run(debug=True)
    #it will run the webserver
    # debug=true means everytime you change the python code its going to automatically rerun the webservice

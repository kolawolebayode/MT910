python3 -m venv mtvenv
activate() {
    . mtvenv/bin/activate
    echo "installing requirements to virtual environment"
    pip3 install -r requirements.txt
    #python manage.py migrate

    #python manage.py qcluster
    

}
activate
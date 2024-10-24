from app import create_app

app = create_app()

if __name__ == "__main__":
    # Enable debug mode
    app.run(host='0.0.0.0', port=8094, debug=True)

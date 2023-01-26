from src.web import create_app
from pathlib import Path

#referencia a la carpeta con los estilos , sin importar el SO,
#puede haber otras maneras tambien
static_folder = Path(__file__).parent.joinpath("public")

app = create_app(static_folder=static_folder)

def main():
    app.run()
    
if __name__ == "__main__":
    main()

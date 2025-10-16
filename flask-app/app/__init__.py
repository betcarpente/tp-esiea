from flask import Flask

def create_app():
    try:
        app = Flask(__name__)
        print("Flask initialisé avec succès")

        try:
            from .routes import main
            app.register_blueprint(main)
            print("Routes enregistrées avec succès")

        except Exception as e:
            print(f"Erreur lors de l'import ou de l'enregistrement des routes : {e}")
            raise

        print("🚀 Application Flask prête à être lancée")
        return app

    except Exception as e:
        print(f"❌ Erreur critique lors de la création de l'application Flask : {e}")
        raise

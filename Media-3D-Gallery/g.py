from gradio_client import Client

try:
    client = Client("http://192.168.1.107:9991/")
    # Intenta ver qué "endpoints" o funciones están disponibles.
    # Esto podría no funcionar directamente así, depende de cómo Gradio expone esto.
    # A menudo, necesitas saber el nombre de la función o el fn_index.
    print(client.view_api(all_endpoints=True)) # Esto intenta mostrar la estructura de la API
except Exception as e:
    print(f"Error conectando o viendo la API: {e}")
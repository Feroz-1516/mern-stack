import requests
from flask import jsonify
from config import BASE_URL

def delete_button(blog_id, on_delete):
    def handle_delete():
        try:
            # Send a delete request to your backend
            response = requests.delete(f"{BASE_URL}/api/blogs/{blog_id}")
            response.raise_for_status()
            # Call the on_delete callback to update the UI
            on_delete()
            return jsonify({"message": "Blog deleted successfully"}), 200
        except requests.RequestException as error:
            print(f"Error deleting blog: {error}")
            return jsonify({"error": "Failed to delete blog"}), 500

    return {
        "type": "button",
        "props": {
            "onClick": handle_delete,
            "children": "Delete"
        }
    }

# Export the delete_button function
__all__ = ['delete_button']
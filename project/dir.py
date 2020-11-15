import os
from flask import Blueprint, session, jsonify

dir = Blueprint('dir', __name__)




@dir.route('/changeFolder', methods=['POST'])
def change_folder(folder_path):
    user_root_folder = session["root_folder"]
    if os.path.isdir(folder_path):
        os.chdir(folder_path)
        current_working_directory = os.getcwd()
        if user_root_folder not in current_working_directory:
            return jsonify({"error": "Chodi nahi. Aukkat me reh"})
        return jsonify({"message": "bandta magya"})

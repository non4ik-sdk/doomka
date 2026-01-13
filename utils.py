import sys, os

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", None)
        exe_dir = os.path.dirname(sys.executable)

        if base_path:
            full_path = os.path.join(base_path, relative_path)
            if os.path.exists(full_path):
                return full_path

        full_path = os.path.join(exe_dir, relative_path)
        if os.path.exists(full_path):
            return full_path

        internal_path = os.path.join(exe_dir, "_internal", relative_path)
        if os.path.exists(internal_path):
            return internal_path

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, relative_path)
    if os.path.exists(full_path):
        return full_path

    full_path = os.path.join(os.getcwd(), relative_path)
    if os.path.exists(full_path):
        return full_path

    raise FileNotFoundError(f"RESOURCE '{relative_path}' NOT FOUND")

import os
import re

def update_nav_menu(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Buscar el patrón donde agregar el nuevo enlace
    pattern = r'(<li class="nav-item me-2">\s*<a class="nav-link nav-link-underline" style="color: black;"\s*href="{{ url_for\(\'contactos\'\) }}">Contactos</a>\s*</li>)'
    
    # El nuevo enlace a agregar
    new_link = '''<li class="nav-item me-2">
                                <a class="nav-link nav-link-underline" style="color: black;"
                                    href="{{ url_for('contactos') }}">Contactos</a>
                            </li>
                            {% if current_user.is_authenticated %}
                            <li class="nav-item me-2">
                                <a class="nav-link nav-link-underline" style="color: black;"
                                    href="{{ url_for('subir_archivo') }}">Subir Archivo</a>
                            </li>
                            {% endif %}'''

    # Reemplazar el patrón con el nuevo enlace
    new_content = re.sub(pattern, new_link, content)

    # Agregar los scripts de notificación antes del cierre del body
    scripts_pattern = r'(</body>)'
    scripts_content = '''
    <!-- Scripts de notificación de carga -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/upload-notification.css') }}">
    <script src="{{ url_for('static', filename='js/upload-handler.js') }}"></script>
    </body>'''
    
    new_content = re.sub(scripts_pattern, scripts_content, new_content)

    # Guardar los cambios
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def main():
    templates_dir = 'templates'
    html_files = [
        'carrito.html', 'tipopago.html', 'tipoentrega.html', 'textiles.html',
        'terminos.html', 'retablos.html', 'registrate.html', 'productodetalle.html',
        'preguntas.html', 'politicas.html', 'nosotros.html', 'mispedidos.html',
        'legales.html', 'joyeria.html', 'detalle_pedido.html', 'contactos.html',
        'ceramica.html', 'cambios.html', 'index.html'
    ]

    for html_file in html_files:
        file_path = os.path.join(templates_dir, html_file)
        if os.path.exists(file_path):
            try:
                update_nav_menu(file_path)
                print(f"Actualizado: {html_file}")
            except Exception as e:
                print(f"Error al actualizar {html_file}: {str(e)}")

if __name__ == "__main__":
    main() 
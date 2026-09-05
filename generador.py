import os
import glob
from google import genai

# Conectar con tu llave secreta usando el nuevo sistema
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

mathjax_config = """
<script>
  MathJax = { tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

# Abrir tu página principal
with open("index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

# Buscar borradores
for archivo_txt in glob.glob("borradores/*.txt"):
    with open(archivo_txt, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    nombre_base = os.path.basename(archivo_txt).replace(".txt", "")
    nombre_html = nombre_base + ".html"
    
    prompt = f"""
    Eres un desarrollador web experto. Convierte este borrador de una clase de matemáticas en un archivo HTML completo, semántico y atractivo. 
    Usa MathJax para las fórmulas. Devuelve SOLO el código HTML.
    Borrador:
    {contenido}
    """
    
    # Generar clase con el modelo PRO actualizado
    respuesta = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
    )
    
    html = respuesta.text.strip().removeprefix("```html").removesuffix("```")
    
    if "</head>" in html:
        html = html.replace("</head>", mathjax_config + "\n</head>")
    
    # 1. Guardar la clase HTML
    with open(nombre_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    # 2. Crear y pegar la tarjeta en el index.html
    titulo_limpio = nombre_base.replace("-", " ").capitalize()
    nueva_tarjeta = f'''
                    <div class="topic-card">
                        <div class="topic-category">Nueva Clase</div>
                        <h3>{titulo_limpio}</h3>
                        <p>Generada con IA a partir de tus apuntes.</p>
                        <a href="{nombre_html}" class="topic-link">Ver lección ➔</a>
                    </div>
                    <!-- NUEVA_PILDORA -->'''
    
    if "<!-- NUEVA_PILDORA -->" in index_html:
        index_html = index_html.replace("<!-- NUEVA_PILDORA -->", nueva_tarjeta)
        
    # 3. Borrar el archivo de texto
    os.remove(archivo_txt)

# 4. Guardar cambios en el index
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
